"""    
VISTOR Authoritative Enrichment    
    
Refines a scraped/best-guess media record against external authoritative    
catalogs to close the classification gap. Every backend implements:    
    
    lookup(title, year=None, media_type=None) -> dict | None    
    
A None result means "no confident match"; the caller keeps its existing    
best-guess values. EnrichmentRouter dispatches by media_type across several    
free backends (TMDB, MusicBrainz, TheSportsDB, Wikipedia). All network imports    
are lazy so the headless smoke test keeps running offline with no keys.    
"""    
  
from metadata.services.enrichment.authoritative_source import AuthoritativeSource  
from metadata.services.enrichment.tmdb_source import TMDBSource  
from metadata.services.enrichment.musicbrainz_source import MusicBrainzSource  
from metadata.services.enrichment.sports_source import SportsSource
from metadata.services.enrichment.wikipedia_source import WikipediaSource  
from metadata.services.enrichment.enrichment_router import EnrichmentRouter  
from metadata.services.enrichment.metadata_enricher import MetadataEnricher  
  
__all__ = [  
    "AuthoritativeSource",  
    "TMDBSource",  
    "MusicBrainzSource",  
    "SportsSource",  
    "WikipediaSource",  
    "EnrichmentRouter",  
    "MetadataEnricher",  
]