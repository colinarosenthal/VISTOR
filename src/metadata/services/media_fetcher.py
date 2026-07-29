"""  
VISTOR Media Fetcher  
  
Provider-agnostic fetch dispatcher. Sources are provider-tagged  
(internet_archive, youtube, smithsonian, ...), and each provider is  
handled by a pluggable backend. This satisfies the fetcher interface  
SourceResolver expects: fetch(provider, reference) -> FetchResult.  
  
Backends are registered by provider name so new archives can be added  
without touching the resolver or acquisition loop. A backend must expose:  
  
    fetch(reference: str) -> FetchResult  
"""  
  
from core.logger import Logger  
from metadata.services.source_resolver import FetchResult  
  
  
class MediaFetcher:  
    """Dispatches a fetch to the backend registered for its provider."""  
  
    def __init__(self):  
        self._backends = {}  
  
    def register(self, provider: str, backend):  
        """Register a per-provider backend exposing fetch(reference)."""  
  
        self._backends[provider] = backend  
  
    def fetch(self, provider: str, reference: str):  
        """Route a fetch to the matching backend, or fail cleanly."""  
  
        backend = self._backends.get(provider)  
  
        if backend is None:  
            Logger.warning(  
                f"No backend registered for provider '{provider}'."  
            )  
            return FetchResult.failure(  
                status_code=501,  
                detail=f"unsupported provider '{provider}'",  
            )  
  
        return backend.fetch(reference)