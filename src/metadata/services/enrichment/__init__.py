"""  
VISTOR Authoritative Enrichment  
  
Refines a scraped/best-guess media record against an external authoritative  
catalog to close the classification gap. Every backend implements:  
  
    lookup(title, year=None, media_type=None) -> dict | None  
  
Backends are offline-safe: with no network/key they return None, so enrich()  
becomes a no-op and the smoke test runs offline with no keys configured.  
"""  
  
from metadata.services.enrichment.authoritative_source import AuthoritativeSource  
from metadata.services.enrichment.tmdb_source import TMDBSource  
from metadata.services.enrichment.musicbrainz_source import MusicBrainzSource  
from metadata.services.enrichment.composite_source import CompositeSource  
from metadata.services.enrichment.metadata_enricher import MetadataEnricher  
  
  
def default_source():  
    """Ranked authoritative chain: TMDB (movies/TV) then MusicBrainz (music).  
    Both are offline-safe no-ops without network/keys, so the smoke test is  
    unaffected."""  
    return CompositeSource([TMDBSource(), MusicBrainzSource()])  
  
  
__all__ = [  
    "AuthoritativeSource",  
    "TMDBSource",  
    "MusicBrainzSource",  
    "CompositeSource",  
    "MetadataEnricher",  
    "default_source",  
]