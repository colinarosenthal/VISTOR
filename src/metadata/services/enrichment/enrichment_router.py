"""
VISTOR Enrichment Router

Dispatches lookup(title, year, media_type) to the ONE free backend that owns
that media type, then returns the shared dict shape every source emits. This
replaces CompositeSource: instead of running every backend and merging
(which let TMDB overwrite MusicBrainz for music), exactly one backend runs.

    Film / TV        -> TMDBSource
    Music            -> MusicBrainzSource
    Sports           -> SportsSource   (TheSportsDB, module: sports_source)
    Everything else  -> WikipediaSource (generic fallback)

The candidate helpers (search_candidates / lookup_by_id / lookup_tv_chain)
are forwarded to TMDBSource so the web ingest "did you mean...?" picker and
the TV-episode chain keep working unchanged.

All backend imports are lazy so the headless smoke test keeps running offline
with no keys, and a missing/failing backend degrades to None rather than
raising.
"""

from core.logger import Logger

# media_type buckets -------------------------------------------------------
_FILM_TV = {"Movie", "Episode", "TVShow", "TV_SHOW"}
_MUSIC = {"MusicVideo", "Concert", "Song", "MUSIC_VIDEO"}
_SPORTS = {"SportsEvent", "SportsTalk", "SPORTS_EVENT", "SPORTS_TALK"}


class EnrichmentRouter:
    """Route an enrichment lookup to the media-type-appropriate backend."""

    def __init__(self, tmdb=None, music=None, sports=None, fallback=None):
        # Lazily construct defaults so importing this module never pulls in
        # network libraries or requires any keys.
        if tmdb is None:
            from metadata.services.enrichment.tmdb_source import TMDBSource
            tmdb = TMDBSource()
        if music is None:
            from metadata.services.enrichment.musicbrainz_source import (
                MusicBrainzSource,
            )
            music = MusicBrainzSource()
        if sports is None:
            from metadata.services.enrichment.sports_source import SportsSource
            sports = SportsSource()
        if fallback is None:
            from metadata.services.enrichment.wikipedia_source import (
                WikipediaSource,
            )
            fallback = WikipediaSource()

        self.tmdb = tmdb
        self.music = music
        self.sports = sports
        self.fallback = fallback

    def _backend_for(self, media_type):
        # Empty/unknown type => TMDB. In the RecordBuilder pipeline the
        # classifier runs AFTER enrichment, so a plain YouTube drop reaches
        # here with type "" and must still hit the film/TV backend rather
        # than the generic Wikipedia fallback.
        if not media_type or media_type in _FILM_TV:
            return self.tmdb
        if media_type in _MUSIC:
            return self.music
        if media_type in _SPORTS:
            return self.sports
        return self.fallback

    def lookup(self, title, year=None, media_type=None):
        backend = self._backend_for(media_type)
        try:
            return backend.lookup(title, year=year, media_type=media_type)
        except Exception as exc:  # noqa: BLE001 - routing is best-effort
            Logger.warning(
                f"Enrichment backend {type(backend).__name__} failed for "
                f"'{title}': {exc!r}."
            )
            return None

    # --- candidate helpers (always TMDB; powers the web picker / TV chain) --
    def search_candidates(self, title, media_type=None, limit=8):
        if not hasattr(self.tmdb, "search_candidates"):
            return []
        return self.tmdb.search_candidates(title, media_type=media_type, limit=limit)

    def lookup_by_id(self, external_id, media_type=None):
        if not hasattr(self.tmdb, "lookup_by_id"):
            return None
        return self.tmdb.lookup_by_id(external_id, media_type=media_type)

    def lookup_tv_chain(self, title, year=None):
        if not hasattr(self.tmdb, "lookup_tv_chain"):
            return None
        return self.tmdb.lookup_tv_chain(title, year=year)
