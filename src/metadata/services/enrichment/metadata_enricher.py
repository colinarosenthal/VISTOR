"""  
VISTOR Metadata Enricher  
  
Refines a record dict (as produced by RecordBuilder) against an authoritative  
source. Fill-if-missing semantics preserve the ingestion precedence:  
  
    overrides > authoritative > classified/scraped > default  
  
A field is only overwritten when the current value is empty/zero/absent, so an  
explicit --type/--genres flag or a confident scrape is never clobbered. The  
enricher is a no-op when the source returns None (offline / no API key / no  
match), so the pipeline degrades gracefully.  
"""  
  
from core.logger import Logger  
  
  
class MetadataEnricher:  
    """Fill gaps in a media record from an AuthoritativeSource."""  
  
    def __init__(self, source=None):  
        if source is None:  
            # Default authoritative backend. Offline-safe: with no  
            # TMDB_API_KEY, its lookup() returns None and enrich() is a no-op.  
            from metadata.services.enrichment.tmdb_source import TMDBSource  
            source = TMDBSource()  
        self.source = source
  
    def enrich(self, record):  
        """Return `record` with missing descriptive fields filled from the source."""  
  
        title = record.get("title", "")  
        if not title:  
            return record  
  
        result = self.source.lookup(  
            title,  
            year=record.get("release_year") or None,  
            media_type=record.get("type"),  
        )  
        if not result:  
            return record  
  
        self._fill(record, "title", result.get("title"))  
        self._fill(record, "release_year", result.get("release_year"))  
        self._fill(record, "runtime_minutes", result.get("runtime_minutes"))  
        self._fill(record, "description", result.get("description"))  
        self._fill(record, "type", result.get("media_type"))  
  
        # Genres: only add authoritative names that aren't already present.  
        if not record.get("genres") and result.get("genres"):  
            record["genres"] = list(result["genres"])  
  
        Logger.info(f"Enriched '{title}' from authoritative source.")  
        return record  
  
    @staticmethod  
    def _fill(record, key, value):  
        """Set record[key] only if the current value is empty/zero/absent."""  
  
        if value in (None, "", 0):  
            return  
        if not record.get(key):  
            record[key] = value