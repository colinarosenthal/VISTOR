"""  
VISTOR Real Fetchers  
  
Concrete network fetchers implementing the SourceResolver fetcher contract:  
  
    fetch(provider: str, reference: str) -> FetchResult  
  
Each fetcher downloads to a temp path, verifies, probes technical metadata,  
fingerprints the asset, then moves it into place. Import guarded so the  
headless test suite still runs without requests / yt-dlp installed.  
"""  
  
from metadata.services.fetchers.base_fetcher import BaseFetcher  
from metadata.services.fetchers.internet_archive_fetcher import InternetArchiveFetcher  
from metadata.services.fetchers.youtube_fetcher import YouTubeFetcher  
from metadata.services.fetchers.http_fetcher import HttpFetcher  
from metadata.services.fetchers.provider_registry import ProviderRegistry  
from metadata.services.fetchers.real_fetcher import RealFetcher  
from metadata.services.fetchers.metadata_probe import MetadataProbe  

from metadata.services.source_resolver import SourceResolver, FetchResult  
from metadata.services.media_ingestor import MediaIngestor  
  
__all__ = [  
    "MetadataLibrary",  
    "MetadataLoader",  
    "MetadataValidator",  
    "MetadataSearch",  
    "MetadataSerializer",  
    "SourceResolver",  
    "FetchResult",  
    "MediaIngestor",  
]