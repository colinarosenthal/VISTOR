"""
VISTOR Metadata Enricher

Refines a record dict (as produced by RecordBuilder) against an authoritative
source. Fill semantics preserve the ingestion precedence:

    overrides > authoritative > classified/scraped > default

A field is overwritten when the current value is empty/zero/absent OR when it
is flagged `provisional` (a scrape/classifier best-guess). An explicit caller
override is NEVER overwritten. The enricher is a no-op when the source returns
None (offline / no API key / no match), so the pipeline degrades gracefully.
"""

from core.logger import Logger


class MetadataEnricher:
    """Fill/correct gaps in a media record from an AuthoritativeSource."""

    def __init__(self, source=None):
        if source is None:
            # Default authoritative backend. Offline-safe: with no
            # TMDB_API_KEY, its lookup() returns None and enrich() is a no-op.
            from metadata.services.enrichment.tmdb_source import TMDBSource
            source = TMDBSource()
        self.source = source

    def enrich(self, record, provisional=None):
        """Return `record` with missing/provisional fields filled from the source."""

        provisional = provisional or set()

        title = record.get("title", "")
        if not title or title.strip().lower() == "untitled":
            # No real title to search on. TMDB's blind results[0] would match a
            # wrong movie for the "Untitled" placeholder, so skip enrichment.
            return record

        # Only constrain the search by year when the year is an explicit
        # override. A provisional (scraped) year - e.g. a YouTube upload date -
        # would wrongly filter out the true release, so drop it from the query.
        search_year = record.get("release_year") or None
        if "release_year" in provisional:
            search_year = None

        result = self.source.lookup(
            title,
            year=search_year,
            media_type=record.get("type"),
        )
        if not result:
            return record

        self._fill(record, "title", result.get("title"), provisional)
        self._fill(record, "release_year", result.get("release_year"), provisional)
        self._fill(record, "runtime_minutes", result.get("runtime_minutes"), provisional)
        self._fill(record, "description", result.get("description"), provisional)
        self._fill(record, "type", result.get("media_type"), provisional)
        self._fill(record, "music_genre", result.get("music_genre"), provisional)

        # Genres: replace when empty OR still a provisional classifier guess.
        if result.get("genres") and (
            not record.get("genres") or "genres" in provisional
        ):
            record["genres"] = list(result["genres"])

        # Carry authoritative credits/studios straight through (raw lists).
        for key in ("cast", "crew", "studios"):
            if result.get(key) and not record.get(key):
                record[key] = list(result[key])

        Logger.info(f"Enriched '{title}' from authoritative source.")
        return record

    @staticmethod
    def _fill(record, key, value, provisional):
        """Set record[key] if the current value is empty/zero OR provisional."""

        if value in (None, "", 0):
            return
        if not record.get(key) or key in provisional:
            record[key] = value
