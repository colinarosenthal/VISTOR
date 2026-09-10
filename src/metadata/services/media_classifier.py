"""
VISTOR Media Classifier

Deterministic, offline best-guess classification of a scraped info-dict
(as returned by MediaDescriber) into:

    - a VISTOR media type string ("Movie", "MusicVideo", "Commercial", "Episode")
    - a list of genre names drawn ONLY from the controlled Genre vocabulary

DETECTION MODEL (hybrid signal scoring)
---------------------------------------
Instead of a first-match if-ladder, every available signal (provider category,
duration, title/tag keywords, channel shape, Internet Archive mediatype /
collection / subject, "artist - track" title shape) casts a WEIGHTED VOTE for a
type. The highest-scoring type above a confidence floor wins; ties or an
all-zero board return None so RecordBuilder falls back to its default/override.

This mirrors how professional pipelines decide: surface many cheap signals,
score them, pick the winner. The one signal metadata cannot give -- the decoded
audio itself -- is deferred to the download stage via refine_with_audio(), an
AcoustID/Chromaprint hook that is a no-op until real media + acoustid exist.

No network, no heavy deps. Guesses are logged so the user knows to verify.
"""

from core.logger import Logger

# The controlled Genre vocabulary (must match MetadataPopulation.create_genres()).
_CONTROLLED_GENRES = {
    "Action", "Adventure", "Animation", "Comedy", "Drama", "Documentary",
    "Horror", "Science Fiction", "Fantasy", "Reality", "Sports", "News", "Music",
}

_CATEGORY_TO_GENRES = {
    "music": ["Music"],
    "film & animation": ["Animation"],
    "sports": ["Sports"],
    "news & politics": ["News"],
    "comedy": ["Comedy"],
    "entertainment": [],
    "gaming": [],
    "howto & style": ["Documentary"],
    "education": ["Documentary"],
    "science & technology": ["Documentary", "Science Fiction"],
    "people & blogs": [],
    "travel & events": ["Adventure"],
}

_KEYWORD_TO_GENRES = {
    "horror": "Horror", "sci-fi": "Science Fiction",
    "science fiction": "Science Fiction", "fantasy": "Fantasy",
    "documentary": "Documentary", "comedy": "Comedy", "action": "Action",
    "adventure": "Adventure", "drama": "Drama", "anime": "Animation",
    "animated": "Animation", "cartoon": "Animation", "reality": "Reality",
    "concert": "Music", "music video": "Music", "official video": "Music",
    "news": "News", "sports": "Sports",
}

# Duration thresholds (seconds).
_MUSIC_VIDEO_MAX_SECONDS = 15 * 60
_COMMERCIAL_MAX_SECONDS = 3 * 60
_MOVIE_MIN_SECONDS = 70 * 60

# Title/tag keyword signals that vote for a specific type, with weights.
_MUSIC_KEYWORDS = (
    ("official video", 3), ("music video", 3), ("official music video", 4),
    ("lyric video", 3), ("official audio", 2), ("vevo", 2), ("mtv", 1),
    ("live performance", 1), ("concert", 1),
)
_COMMERCIAL_KEYWORDS = (
    ("commercial", 3), ("advertisement", 3), ("advert", 2), ("tv spot", 3),
    ("promo", 1),
)
_EPISODE_KEYWORDS = (
    ("episode", 2), ("season", 2), ("s0", 1), ("e0", 1), ("pilot", 1),
)

# Confidence floor: a winning type must clear this to be trusted.
_MIN_CONFIDENCE = 2


class ContentProfile:
    """Normalized bag of detection signals, provider-agnostic."""

    def __init__(self, scraped):
        scraped = scraped or {}
        self.title = (scraped.get("title") or "").lower()
        self.duration = scraped.get("duration") or 0
        self.categories = [c.lower() for c in (scraped.get("categories") or [])]
        self.tags = [t.lower() for t in (scraped.get("tags") or [])]
        self.channel = (scraped.get("channel") or "").lower()
        # Internet Archive signals.
        self.mediatype = (scraped.get("mediatype") or "").lower()
        self.collection = [c.lower() for c in (scraped.get("collection") or [])]
        self.subject = [s.lower() for s in (scraped.get("subject") or [])]
        self.text = " ".join([self.title, *self.tags, *self.subject]).lower()

    @property
    def is_music_bucket(self):
        """True if any provider bucket screams 'music' (category/collection/subject)."""
        if "music" in self.categories:
            return True
        blob = " ".join(self.collection + self.subject)
        return any(k in blob for k in ("music", "musicbrainz", "78rpm", "album"))

    @property
    def looks_like_artist_track(self):
        """'Artist - Track' shape (common to music-video titles).

        When the duration is KNOWN it must be short enough to be a song. But
        Internet Archive items frequently expose no duration at all, so a
        missing duration must NOT veto the shape -- otherwise a music item like
        'The Buggles - Video Killed The Radio Star' loses this vote and the
        weak archive `mediatype=movies` +1 ties it into an undecidable board.
        """
        if " - " not in self.title:
            return False
        if self.duration:
            return self.duration <= _MUSIC_VIDEO_MAX_SECONDS
        # Duration unknown (common for Archive items): allow the shape.
        return True


class TypeScorer:
    """Runs every extractor, tallies weighted votes per media type."""

    def score(self, profile):
        scores = {"Movie": 0, "MusicVideo": 0, "Commercial": 0, "Episode": 0}
        reasons = {}

        def vote(mtype, weight, reason):
            if weight <= 0:
                return
            scores[mtype] += weight
            reasons.setdefault(mtype, []).append(f"{reason} (+{weight})")

        # --- MusicVideo signals ---------------------------------------
        if profile.is_music_bucket:
            vote("MusicVideo", 3, "music bucket (category/collection/subject)")
        for kw, w in _MUSIC_KEYWORDS:
            if kw in profile.text:
                vote("MusicVideo", w, f"keyword '{kw}'")
        if profile.channel.endswith("vevo") or "- topic" in profile.channel:
            vote("MusicVideo", 3, "music channel shape")
        if profile.looks_like_artist_track:
            vote("MusicVideo", 2, "'artist - track' short title")
        if (
            profile.duration
            and profile.duration <= _MUSIC_VIDEO_MAX_SECONDS
            and profile.is_music_bucket
        ):
            vote("MusicVideo", 2, "music bucket + short duration")

        # --- Movie signals --------------------------------------------
        if "film & animation" in profile.categories:
            vote("Movie", 2, "category=Film & Animation")
        if profile.duration and profile.duration >= _MOVIE_MIN_SECONDS:
            vote("Movie", 3, "duration >= 70min")
        if profile.mediatype == "movies" and not profile.is_music_bucket:
            # Archive gives 'movies' to almost everything, so it's only a weak
            # nudge -- an 'artist - track' shape or a music bucket out-votes it.
            vote("Movie", 1, "archive mediatype=movies")

        # --- Commercial signals ---------------------------------------
        for kw, w in _COMMERCIAL_KEYWORDS:
            if kw in profile.text:
                vote("Commercial", w, f"keyword '{kw}'")
        if (
            profile.duration
            and profile.duration <= _COMMERCIAL_MAX_SECONDS
            and any(k in profile.text for k, _ in _COMMERCIAL_KEYWORDS)
        ):
            vote("Commercial", 2, "ad keyword + very short")

        # --- Episode signals ------------------------------------------
        for kw, w in _EPISODE_KEYWORDS:
            if kw in profile.text:
                vote("Episode", w, f"keyword '{kw}'")

        return scores, reasons


class MediaClassifier:
    """Best-guess (type, genres) from a scraped info-dict. Never raises."""

    def __init__(self):
        self._scorer = TypeScorer()

    def classify_type(self, scraped):
        """Return a loader media-type string or None if undecidable."""
        profile = ContentProfile(scraped)
        scores, reasons = self._scorer.score(profile)

        winner = max(scores, key=scores.get)
        top = scores[winner]

        # No confident signal, or a tie between the top two -> undecidable.
        ranked = sorted(scores.values(), reverse=True)
        tied = len(ranked) > 1 and ranked[0] == ranked[1] and ranked[0] > 0
        if top < _MIN_CONFIDENCE or tied:
            Logger.info(
                f"Classifier undecided (scores={scores}); "
                f"deferring to default/override."
            )
            return None

        why = "; ".join(reasons.get(winner, []))
        Logger.info(
            f"Classified type '{winner}' [score {top}] ({why}); verify if wrong."
        )
        return winner

    def classify_genres(self, scraped):
        """Return de-duplicated controlled Genre names, possibly empty."""
        scraped = scraped or {}
        found = []

        for category in (scraped.get("categories") or []):
            for name in _CATEGORY_TO_GENRES.get(category.lower(), []):
                found.append(name)

        text = self._searchable_text(scraped)
        for keyword, name in _KEYWORD_TO_GENRES.items():
            if keyword in text:
                found.append(name)

        result = []
        for name in found:
            if name in _CONTROLLED_GENRES and name not in result:
                result.append(name)

        if result:
            Logger.info(f"Classified genres (verify): {result}")
        return result

    # ------------------------------------------------------------------
    # Deferred: content-based audio refinement (AcoustID / Chromaprint)
    # ------------------------------------------------------------------

    def refine_with_audio(self, record, audio_path):
        """
        DOWNLOAD-STAGE HOOK. Once media is on disk, compute a Chromaprint
        fingerprint and query AcoustID -> MusicBrainz. A confident recording
        match is the strongest possible "this is music" signal and can promote
        a mis-typed Movie to MusicVideo and seed the MBID for enrichment.

        Offline-safe no-op today: if the `acoustid` package or an API key is
        absent, the record is returned unchanged so tests never touch the
        network. Wire the real call here when the download pipeline lands.
        """
        try:
            import acoustid  # type: ignore[import-not-found]  # noqa: F401 - optional, download-stage only
        except ImportError:
            return record
        # Intentionally not implemented until the download pipeline exists.
        return record

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _searchable_text(self, scraped):
        parts = [scraped.get("title") or ""]
        parts.extend(scraped.get("tags") or [])
        parts.extend(scraped.get("subject") or [])
        return " ".join(parts).lower()
