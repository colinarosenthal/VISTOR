"""  
VISTOR Authoritative Enrichment  
  
Refines a scraped/best-guess media record against an external authoritative  
catalog (e.g. TMDB) to close the classification gap. Every backend implements:  
  
    lookup(title, year=None, media_type=None) -> dict | None  
  
A None result means "no confident match"; the caller keeps its existing  
best-guess values. All network imports are lazy so the headless smoke test  
keeps running offline with no API key configured.  
"""  
  
from metadata.services.enrichment.authoritative_source import AuthoritativeSource  
from metadata.services.enrichment.tmdb_source import TMDBSource  
from metadata.services.enrichment.metadata_enricher import MetadataEnricher  
  
__all__ = ["AuthoritativeSource", "TMDBSource", "MetadataEnricher"]