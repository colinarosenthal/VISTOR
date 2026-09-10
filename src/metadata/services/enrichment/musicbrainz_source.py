"""
VISTOR MusicBrainz Authoritative Source

Free, keyless lookup for music recordings via the MusicBrainz web service
(https://musicbrainz.org/ws/2/). Enriches MusicVideo records that TMDB
structurally cannot match. Returns the real first-release year, a controlled
MusicGenre name derived from MusicBrainz genres/tags, and — via the free,
keyless lyrics.ovh API — the song's LYRICS as the record description.

The recording search/detail often reports a LATER release date (a re-issue /
remaster / live recording) than when the song originally came out, because a
YouTube title maps to whichever recording MusicBrainz scores highest, not the
1996 studio original. To pin the TRUE original year we additionally search the
RELEASE-GROUP endpoint:

    release-group?query=artist:"Jamiroquai" AND releasegroup:"Virtual Insanity"

and take the MINIMUM first-release-date across the returned release-groups,
PREFERRING original-release primary types (Single / Album / EP) over
compilations / live albums / soundtracks that merely re-issue the song years
later. The original "Virtual Insanity" release-group is dated 1996, so this
surfaces the true original year regardless of which recording the title maps
to. The recording detail (release-groups) is kept as a secondary source, and
the earliest non-zero of all of them wins.

Genre is taken from the ARTIST's genres/tags FIRST, where styles like funk /
acid jazz actually live. A specific recording or release is often tagged with
a noisy one-off style (e.g. a compilation tagged "reggae"), so the artist is
the more reliable source of the act's real style; the recording/detail tags
are only a fallback when the artist carries none.

LYRICS: once MusicBrainz has resolved a clean (artist, track), we query
lyrics.ovh (https://api.lyrics.ovh/v1/<artist>/<track>) for the full lyric
text and return it as `description` so the preview caption shows the lyrics
and nothing else. fetch_lyrics() is a standalone public method so the future
"turn on captions" feature can reuse the exact same provider without going
through the whole lookup path. No key required; a 404 (no lyrics) or any
network error degrades to an empty string, leaving the caller's existing
description untouched.

When the download-stage AcoustID refiner has already CONFIRMED a recording via
its audio fingerprint, it calls lookup_by_recording_mbid() directly: no title
guessing, just an authoritative detail-fetch of that exact recording for the
canonical year (via its release-groups), the artist's genre, and the lyrics.

MusicBrainz throttles to ~1 request/second and returns 503 when exceeded, so
we space requests out and retry on 503. A single lookup fires several
sequential requests (recording search, release-group search, artist, recording
detail), so the spacing MUST stay at or above ~1s per request or the later
calls 503 and silently drop the genre/year. The release-group call in
particular is what pins the ORIGINAL year, so a lone 503 there previously let
the year regress to a later re-issue; _get() now retries a 503 up to twice.
Every network failure is swallowed and degrades to whatever we already have
(offline-safe: the smoke test never hits the network because `requests` is
imported lazily).
"""

import re
import time
from urllib.parse import quote

from core.logger import Logger

_BASE = "https://musicbrainz.org/ws/2"
_LYRICS_BASE = "https://api.lyrics.ovh/v1"  # free, keyless lyric text provider
_UA = "VISTOR/0.6 ( https://github.com/colinarosenthal/VISTOR )"
# Seconds between requests. MusicBrainz asks for ~1/sec; because a single
# lookup makes 4+ sequential calls, 1.1s was too tight under network jitter and
# the tail calls (artist genre, release-group year) 503'd. 2.0s clears that.
_MIN_INTERVAL = 2.0

# How many times _get() retries a 503 before giving up. A single retry left the
# release-group call (which pins the ORIGINAL year) vulnerable to one unlucky
# rate-limit, which is what let the Buggles year regress from 1979 to 1998.
_MAX_503_RETRIES = 3

# Release-group primary types that represent an ORIGINAL release of a song, as
# opposed to a later compilation / live album / soundtrack that re-issues it.
# We prefer the earliest date among THESE before falling back to any type.
_ORIGINAL_RG_TYPES = {"single", "album", "ep"}

# Strip common YouTube title noise (parenthesized) before parsing artist/track.
_TITLE_NOISE = re.compile(
    r"\((official\s*(music\s*)?video|official\s*audio|lyric[s]?\s*video|"
    r"audio|hd|4k|remaster(ed)?(\s*\d{4})?)\)",
    re.IGNORECASE,
)

# Bare trailing noise tokens (NO parentheses) that Archive / YouTube titles
# tack on, e.g. "... MTV", "... HD", "... Official Video". These break the
# MusicBrainz query if left on the track name, so we peel them off the END of
# the title repeatedly before splitting into (artist, track).
_TRAILING_NOISE = re.compile(
    r"[\s\-]+("
    r"official\s*(music\s*)?video|official\s*audio|lyric[s]?\s*video|"
    r"music\s*video|full\s*video|mtv|vevo|hd|hq|4k|remaster(ed)?(\s*\d{4})?"
    r")\s*$",
    re.IGNORECASE,
)


# MusicBrainz free-text genre/tag -> VISTOR controlled MusicGenre name.
# Only names that exist in MetadataPopulation.create_music_genres() may appear
# on the right; anything unmapped is dropped so we never invent a genre.
_TAG_TO_MUSIC_GENRE = {
    # --- Rock + sub-genres ------------------------------------------
    "rock": "Rock",
    "alternative rock": "Alternative Rock",
    "alternative": "Alternative Rock",
    "alt-rock": "Alternative Rock",
    "classic rock": "Classic Rock",
    "hard rock": "Hard Rock",
    "glam rock": "Glam Rock",
    "glam": "Glam Rock",
    "progressive rock": "Progressive Rock",
    "prog rock": "Progressive Rock",
    "prog": "Progressive Rock",
    "punk rock": "Punk Rock",
    "punk": "Punk Rock",
    "post-punk": "Punk Rock",
    "pop punk": "Punk Rock",
    "indie rock": "Indie Rock",
    "indie": "Indie Rock",
    "grunge": "Grunge",
    "pop rock": "Pop Rock",

    # --- Metal + sub-genres -----------------------------------------
    "metal": "Metal",
    "heavy metal": "Heavy Metal",
    "thrash metal": "Thrash Metal",
    "thrash": "Thrash Metal",
    "death metal": "Death Metal",
    "black metal": "Black Metal",
    "doom metal": "Doom Metal",
    "doom": "Doom Metal",
    "nu metal": "Nu Metal",
    "nu-metal": "Nu Metal",
    "power metal": "Power Metal",

    # --- Pop + sub-genres -------------------------------------------
    "pop": "Pop",
    "teen pop": "Teen Pop",
    "dance pop": "Dance Pop",
    "dance-pop": "Dance Pop",
    "synth pop": "Synth Pop",
    "synth-pop": "Synth Pop",
    "synthpop": "Synth Pop",
    "new wave": "Synth Pop",   # Buggles-era synth new wave
    "bubblegum pop": "Bubblegum Pop",
    "bubblegum": "Bubblegum Pop",

    # --- Hip Hop + sub-genres ---------------------------------------
    "hip hop": "Hip Hop",
    "hip-hop": "Hip Hop",
    "rap": "Hip Hop",
    "east coast hip hop": "East Coast Hip Hop",
    "west coast hip hop": "West Coast Hip Hop",
    "gangsta rap": "Gangsta Rap",
    "alternative hip hop": "Alternative Hip Hop",
    "trap": "Trap",

    # --- Electronic + sub-genres ------------------------------------
    "electronic": "Electronic",
    "electronica": "Electronic",
    "edm": "Electronic",
    "dance": "Electronic",
    "house": "House",
    "techno": "Techno",
    "trance": "Trance",
    "drum and bass": "Drum and Bass",
    "drum & bass": "Drum and Bass",
    "dnb": "Drum and Bass",
    "ambient": "Ambient",
    "synthwave": "Synthwave",

    # --- Standalone genres ------------------------------------------
    "jazz": "Jazz",
    "acid jazz": "Jazz",
    "funk": "Jazz",              # no Funk in the catalog; nearest controlled
    "soul": "Jazz",             # no Soul in the catalog; nearest controlled
    "classical": "Classical",
    "orchestral": "Classical",
    "country": "Country",
    "blues": "Blues",
    "rhythm and blues": "Blues",  # nearest controlled (no R&B genre)
    "r&b": "Blues",             # nearest controlled (no R&B genre)
    "folk": "Folk",
    "reggae": "Reggae",
    "ska": "Reggae",            # nearest controlled
    "latin": "Latin",
    "world": "World",
}

class MusicBrainzSource:
    """Best-effort music lookup. Never raises to the caller."""

    def __init__(self, timeout=10):
        self.timeout = timeout
        self._last_request = 0.0

    # Only used for MusicVideo; the composite router respects this hook.
    def handles(self, media_type):
        return media_type in (None, "", "MusicVideo")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def lookup(self, title, year=None, media_type=None):
        try:
            import requests  # lazy: keeps the offline smoke test network-free
        except ImportError:
            Logger.warning("requests not installed; skipping MusicBrainz.")
            return None

        artist, track = self._split(title)
        query = self._build_query(artist, track)
        if not query:
            return None

        search = self._get(
            requests,
            f"{_BASE}/recording",
            {"query": query, "fmt": "json", "limit": 5},
        )
        if not search:
            return None

        recordings = search.get("recordings") or []
        if not recordings:
            Logger.info(f"MusicBrainz: no recording match for '{title}'.")
            return None

        # Don't blindly take recordings[0]. Prefer a high-score match that
        # already carries a first-release-date; that skips live/cover/
        # compilation recordings whose date is empty and would yield year 0.
        recording = self._pick_recording(recordings, artist)
        mbid = recording.get("id")

        # Year seed from the SEARCH result. This is often a re-issue year
        # (e.g. 1999 for a 1996 song), so we treat it only as an upper bound
        # and let the release-group search below pull it back to the original.
        rec_year = self._year_from(recording.get("first-release-date"))

        # GENRE: prefer the ARTIST's genres/tags FIRST. Styles like funk /
        # acid jazz live on the artist; a specific recording/release is often
        # tagged with a noisy one-off style (this is what produced the wrong
        # "reggae" for Jamiroquai). Fall back to the recording's own tags only
        # if the artist carries none.
        music_genre = self._artist_genre(requests, recording)
        if not music_genre:
            music_genre = self._map_first(
                (recording.get("genres") or []) + (recording.get("tags") or [])
            )

        # PRIMARY year source: the RELEASE-GROUP search. The original release
        # group ("Virtual Insanity" / "Travelling Without Moving") is dated to
        # the song's true debut year, independent of which recording the
        # YouTube title mapped to. Take the EARLIEST across all returned
        # release-groups, preferring original-release primary types.
        rg_year = self._release_group_year(requests, artist, track)
        rec_year = self._min_year(rec_year, rg_year)

        # SECONDARY: detail-fetch the recording INCLUDING release-groups, in
        # case the release-group search missed (odd punctuation, etc.). Also
        # used to fill genre if neither the artist nor the search carried one.
        if mbid:
            detail = self._get(
                requests,
                f"{_BASE}/recording/{mbid}",
                {"fmt": "json", "inc": "genres+tags+releases+release-groups"},
            )
            if detail:
                detail_year = self._earliest_year(detail)
                rec_year = self._min_year(rec_year, detail_year)
                if not music_genre:
                    music_genre = self._map_first(
                        (detail.get("genres") or []) + (detail.get("tags") or [])
                    )

        # LYRICS: use the recording's CANONICAL artist/track when available
        # (cleaner than the noisy parsed title), fall back to the parsed pair.
        canon_artist, canon_track = self._recording_artist_track(recording)
        lyrics = self.fetch_lyrics(canon_artist or artist, canon_track or track)
        # lyrics.ovh is spelling-sensitive; if the canonical pair 404s, retry
        # with the parsed (artist, track) from the title before giving up.
        if not lyrics and (canon_artist, canon_track) != (artist, track):
            lyrics = self.fetch_lyrics(artist, track)

        Logger.info(
            f"MusicBrainz matched '{title}' -> "
            f"{rec_year or '?'} (genre={music_genre or '?'}, "
            f"lyrics={'yes' if lyrics else 'no'})."
        )

        return {
            "release_year": rec_year,
            "media_type": "MusicVideo",
            "genres": ["Music"],        # broad controlled Genre stays "Music"
            "music_genre": music_genre,  # specific style rides along
            "description": lyrics,       # lyric text becomes the caption
        }

    # ------------------------------------------------------------------
    # Definitive path: AcoustID has already CONFIRMED the recording MBID
    # ------------------------------------------------------------------
    def lookup_by_recording_mbid(self, mbid):
        """Authoritative enrichment for a recording MBID confirmed by the
        download-stage AcoustID audio fingerprint.

        Skips all title guessing: detail-fetch the exact recording (with
        release-groups for the canonical original year), read the artist's
        genre, and fetch the lyrics. Returns the same dict shape as lookup(),
        or None on failure so the caller keeps whatever the title-search
        already produced."""
        if not mbid:
            return None

        try:
            import requests  # lazy: keeps the offline smoke test network-free
        except ImportError:
            Logger.warning("requests not installed; skipping MusicBrainz.")
            return None

        detail = self._get(
            requests,
            f"{_BASE}/recording/{mbid}",
            {
                "fmt": "json",
                "inc": "artist-credits+genres+tags+releases+release-groups",
            },
        )
        if not detail:
            return None

        rec_year = self._earliest_year(detail)

        # Artist genre first (funk/acid jazz live there), recording tags next.
        music_genre = self._artist_genre(requests, detail)
        if not music_genre:
            music_genre = self._map_first(
                (detail.get("genres") or []) + (detail.get("tags") or [])
            )

        canon_artist, canon_track = self._recording_artist_track(detail)
        lyrics = self.fetch_lyrics(canon_artist, canon_track)

        Logger.info(
            f"MusicBrainz confirmed recording {mbid} -> "
            f"{rec_year or '?'} (genre={music_genre or '?'}, "
            f"lyrics={'yes' if lyrics else 'no'})."
        )

        return {
            "release_year": rec_year,
            "media_type": "MusicVideo",
            "genres": ["Music"],
            "music_genre": music_genre,
            "description": lyrics,
        }

    # ------------------------------------------------------------------
    # Lyrics provider (free, keyless). Standalone so the future captions
    # feature can call it directly with a known (artist, track).
    # ------------------------------------------------------------------
    def fetch_lyrics(self, artist, track):
        """Return the full lyric text for (artist, track), or "" on any miss.

        Backed by lyrics.ovh (no API key). A 404 means "no lyrics for this
        song"; that and every network/parse error degrade to "" so the caller
        keeps whatever description it already had. Reusable by the captions
        feature: MusicBrainzSource().fetch_lyrics("The Buggles",
        "Video Killed the Radio Star")."""
        if not artist or not track:
            return ""

        try:
            import requests  # lazy: keeps the offline smoke test network-free
        except ImportError:
            return ""

        url = f"{_LYRICS_BASE}/{quote(artist)}/{quote(track)}"
        try:
            resp = requests.get(
                url,
                headers={"User-Agent": _UA, "Accept": "application/json"},
                timeout=self.timeout,
            )
        except Exception as exc:  # noqa: BLE001 - lyrics are best-effort
            Logger.warning(f"lyrics.ovh request failed: {exc!r}.")
            return ""

        if resp.status_code == 404:
            Logger.info(f"lyrics.ovh: no lyrics for '{artist} - {track}'.")
            return ""
        if resp.status_code != 200:
            Logger.warning(f"lyrics.ovh HTTP {resp.status_code} for {url}.")
            return ""

        try:
            data = resp.json()
        except Exception as exc:  # noqa: BLE001
            Logger.warning(f"lyrics.ovh bad JSON: {exc!r}.")
            return ""

        lyrics = (data.get("lyrics") or "").strip()
        if not lyrics:
            return ""

        # Normalize line endings and collapse 3+ blank lines to a single gap.
        lyrics = lyrics.replace("\r\n", "\n").replace("\r", "\n")
        lyrics = re.sub(r"\n{3,}", "\n\n", lyrics).strip()
        return lyrics

    # ------------------------------------------------------------------
    # Release-group search: the canonical "originally released" year
    # ------------------------------------------------------------------
    def _release_group_year(self, requests, artist, track):
        """Search the release-group endpoint and return the year of the
        ORIGINAL release of the song.

        Query: artist:"<artist>" AND releasegroup:"<track>". Among the
        credited groups we PREFER the earliest first-release-date whose
        primary-type is an original release (Single / Album / EP), so a later
        compilation / live album / soundtrack that re-issues the song can't
        win even if the true original single is missing a date. Only when no
        original-type group carries a date do we fall back to the earliest of
        ANY type."""
        if not track:
            return 0

        # Query on the release-group TITLE only; the artist-credit filter in
        # the loop below (which is more forgiving of MB's artist indexing than
        # a Lucene artist: clause) keeps only groups credited to the artist.
        query = f'releasegroup:"{track}"'

        data = self._get(
            requests,
            f"{_BASE}/release-group",
            {"query": query, "fmt": "json", "limit": 25},
        )
        if not data:
            return 0

        groups = data.get("release-groups") or []

        # DIAGNOSTIC: surface what the release-group search actually returned
        # (title / primary-type / date) so a wrong year can be traced to a
        # later compilation vs. the original single. Trim once confirmed.
        if groups:
            Logger.info(
                "MB release-group candidates: "
                + "; ".join(
                    f"{(rg.get('title') or '?')}"
                    f"[{(rg.get('primary-type') or '?')}]"
                    f"={(rg.get('first-release-date') or '?')}"
                    for rg in groups[:10]
                )
            )

        artist_l = (artist or "").lower()
        best_original = ""   # earliest date among Single/Album/EP
        best_any = ""        # earliest date among ANY type (fallback)

        for rg in groups:
            # If we know the artist, keep only groups credited to them so a
            # same-named song by another artist can't drag the year.
            if artist_l:
                credited = False
                for credit in rg.get("artist-credit") or []:
                    name = ((credit or {}).get("artist") or {}).get("name", "")
                    if artist_l in name.lower():
                        credited = True
                        break
                if not credited:
                    continue

            date = rg.get("first-release-date") or ""
            if not date:
                continue

            if not best_any or date < best_any:
                best_any = date

            ptype = (rg.get("primary-type") or "").lower()
            if ptype in _ORIGINAL_RG_TYPES:
                if not best_original or date < best_original:
                    best_original = date

        # Prefer the original-release year; only fall back to the earliest of
        # any type when no Single/Album/EP group carried a usable date.
        return self._year_from(best_original or best_any)

    # ------------------------------------------------------------------
    # HTTP with rate-limit spacing + retries on 503
    # ------------------------------------------------------------------
    def _get(self, requests, url, params):
        # attempt 0 is the first try; up to _MAX_503_RETRIES additional tries
        # follow it, each backing off harder, so a transient rate-limit on the
        # year-pinning release-group call no longer drops it to None.
        for attempt in range(_MAX_503_RETRIES + 1):
            wait = _MIN_INTERVAL - (time.time() - self._last_request)
            if wait > 0:
                time.sleep(wait)
            try:
                resp = requests.get(
                    url,
                    params=params,
                    headers={"User-Agent": _UA, "Accept": "application/json"},
                    timeout=self.timeout,
                )
            except Exception as exc:  # noqa: BLE001 - never fail the caller
                Logger.warning(f"MusicBrainz request failed: {exc!r}.")
                return None
            finally:
                self._last_request = time.time()

            if resp.status_code == 503 and attempt < _MAX_503_RETRIES:
                # Back off harder than the normal spacing before each retry;
                # a 503 means we're already over the per-second budget. Scale
                # the wait with the attempt so repeated 503s progressively
                # ease off (2x, then 3x the base interval).
                Logger.warning(
                    f"MusicBrainz 503 (rate limited); "
                    f"retry {attempt + 1}/{_MAX_503_RETRIES}."
                )
                time.sleep(_MIN_INTERVAL * (attempt + 2))
                continue
            if resp.status_code != 200:
                Logger.warning(f"MusicBrainz HTTP {resp.status_code} for {url}.")
                return None
            try:
                return resp.json()
            except Exception as exc:  # noqa: BLE001
                Logger.warning(f"MusicBrainz bad JSON: {exc!r}.")
                return None
        return None

    def _artist_genre(self, requests, recording):
        credits = recording.get("artist-credit") or []
        if not credits:
            return ""
        artist = (credits[0] or {}).get("artist") or {}
        mbid = artist.get("id")
        if not mbid:
            return ""
        data = self._get(
            requests,
            f"{_BASE}/artist/{mbid}",
            {"fmt": "json", "inc": "genres+tags"},
        )
        if not data:
            return ""
        return self._map_first(
            (data.get("genres") or []) + (data.get("tags") or [])
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _pick_recording(self, recordings, artist):
        """Choose the best candidate rather than blindly recordings[0].

        Order of preference:
          1. matches the parsed artist AND has a first-release-date
          2. has a first-release-date (any artist)
          3. matches the parsed artist
          4. the top text-score hit (recordings[0])
        Within each tier the earliest first-release-date wins, so the ORIGINAL
        studio recording beats later live/compilation re-releases.
        """
        artist_l = (artist or "").lower()

        def artist_matches(rec):
            if not artist_l:
                return False
            for credit in rec.get("artist-credit") or []:
                name = ((credit or {}).get("artist") or {}).get("name", "")
                if artist_l in name.lower():
                    return True
            return False

        def has_date(rec):
            return bool(rec.get("first-release-date"))

        def date_key(rec):
            # Empty dates sort last so real dates are preferred.
            return rec.get("first-release-date") or "9999"

        for predicate in (
            lambda r: artist_matches(r) and has_date(r),
            has_date,
            artist_matches,
        ):
            matches = [r for r in recordings if predicate(r)]
            if matches:
                return sorted(matches, key=date_key)[0]

        return recordings[0]

    @staticmethod
    def _recording_artist_track(recording):
        """(artist_name, track_title) from a recording/detail dict.

        Uses MusicBrainz's canonical names, which are cleaner than the parsed
        YouTube/Archive title and give lyrics.ovh its best shot at a match."""
        track = recording.get("title") or ""
        artist = ""
        credits = recording.get("artist-credit") or []
        if credits:
            artist = ((credits[0] or {}).get("artist") or {}).get("name", "")
        return artist, track

    @staticmethod
    def _earliest_year(detail):
        """Earliest year across the recording's first-release-date, every
        release date, and every release-group first-release-date. The
        release-group value is the canonical 'originally released' year."""
        candidates = []

        if detail.get("first-release-date"):
            candidates.append(detail["first-release-date"])

        for rel in detail.get("releases") or []:
            if rel.get("date"):
                candidates.append(rel["date"])
            rg = rel.get("release-group") or {}
            if rg.get("first-release-date"):
                candidates.append(rg["first-release-date"])

        best = ""
        for date in candidates:
            if date and (not best or date < best):
                best = date
        return MusicBrainzSource._year_from(best)

    @staticmethod
    def _min_year(a, b):
        """Earliest non-zero year of the two, or 0 if both are empty."""
        years = [y for y in (a, b) if y]
        return min(years) if years else 0

    @staticmethod
    def _split(title):
        """Parse 'Artist - Track (Official Video) MTV' into (artist, track).

        First strip parenthesized noise, then peel bare trailing noise tokens
        (MTV / HD / Official Video with no parentheses) off the END repeatedly
        so 'The Buggles - Video Killed The Radio Star MTV' searches as
        'Video Killed The Radio Star' rather than dragging 'MTV' into the query.
        """
        cleaned = _TITLE_NOISE.sub("", title or "")

        # Peel bare trailing noise tokens until none remain (handles "... MTV HD").
        prev = None
        while prev != cleaned:
            prev = cleaned
            cleaned = _TRAILING_NOISE.sub("", cleaned).strip()

        cleaned = re.sub(r"\s{2,}", " ", cleaned).strip(" -")
        if " - " in cleaned:
            artist, track = cleaned.split(" - ", 1)
            return artist.strip(), track.strip()
        return "", cleaned

    @staticmethod
    def _build_query(artist, track):
        if track and artist:
            return f'recording:"{track}" AND artist:"{artist}"'
        if track:
            return f'recording:"{track}"'
        return ""

    @staticmethod
    def _map_first(items):
        """Highest-count genre/tag that maps to a controlled MusicGenre."""
        for item in sorted(
            items or [], key=lambda t: t.get("count", 0), reverse=True
        ):
            mapped = _TAG_TO_MUSIC_GENRE.get((item.get("name") or "").lower())
            if mapped:
                return mapped
        return ""

    @staticmethod
    def _year_from(date):
        if date and len(date) >= 4 and date[:4].isdigit():
            return int(date[:4])
        return 0
