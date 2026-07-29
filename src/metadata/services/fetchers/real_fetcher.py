"""  
VISTOR Real Fetcher  
  
Production fetcher passed to SourceResolver. Routes each (provider,  
reference) to the right provider fetcher via the registry, and forwards  
the target MediaAsset so technical metadata + fingerprint get populated.  
"""  
  
from metadata.services.source_resolver import FetchResult  
from metadata.services.fetchers.provider_registry import ProviderRegistry  
  
  
class RealFetcher:  
    """Implements fetch(provider, reference) -> FetchResult by delegation."""  
  
    def __init__(self, registry=None, media_root="Media"):  
        self.registry = registry or ProviderRegistry(media_root=media_root)  
        # The asset currently being resolved. Set via bind() so fetchers  
        # can populate its technical fields on success.  
        self._asset = None  
  
    def bind(self, asset):  
        """Tell the fetcher which asset the next fetch(es) belong to."""  
  
        self._asset = asset  
  
    def fetch(self, provider, reference):  
        fetcher = self.registry.get(provider)  
        fetcher.current_asset = self._asset  
        try:  
            return fetcher.fetch(provider, reference)  
        finally:  
            fetcher.current_asset = None