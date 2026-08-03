"""  
VISTOR Composite Authoritative Source  
  
Chains several AuthoritativeSource backends in ranked reliability order and  
presents them to MetadataEnricher as a single source. lookup() tries each  
backend in order (respecting an optional handles(media_type) hook), merges the  
normalized dicts with EARLIER backends winning per field, and skips any backend  
that returns None or raises. The candidate helpers (search_candidates /  
lookup_by_id / lookup_tv_chain) are forwarded to the first backend that  
implements them (only TMDBSource does today), so the web ingest "did you  
mean...?" picker keeps working unchanged.  
"""  
  
from core.logger import Logger  
  
from metadata.services.enrichment.authoritative_source import AuthoritativeSource  
  
# Values treated as "empty" so a later backend may fill them.  
_EMPTY = (None, "", 0, [], {})  
  
  
class CompositeSource(AuthoritativeSource):  
    def __init__(self, backends=None):  
        self.backends = list(backends or [])  
  
    def lookup(self, title, year=None, media_type=None):  
        merged = {}  
        for backend in self.backends:  
            handles = getattr(backend, "handles", None)  
            if callable(handles) and not handles(media_type):  
                continue  
            try:  
                result = backend.lookup(title, year=year, media_type=media_type)  
            except Exception as exc:  # noqa: BLE001 - never fail the caller  
                Logger.warning(  
                    f"{type(backend).__name__}.lookup failed: {exc!r}."  
                )  
                continue  
            if not result:  
                continue  
            # Earlier backends win: only fill fields still empty in `merged`.  
            for key, value in result.items():  
                if value in _EMPTY:  
                    continue  
                if merged.get(key) in _EMPTY:  
                    merged[key] = value  
        return merged or None  
  
    # --- forwarded candidate helpers (first backend that implements them) ---  
    def _first_with(self, name):  
        for backend in self.backends:  
            if hasattr(backend, name):  
                return backend  
        return None  
  
    def search_candidates(self, title, media_type=None, limit=8):  
        backend = self._first_with("search_candidates")  
        if not backend:  
            return []  
        return backend.search_candidates(title, media_type=media_type, limit=limit)  
  
    def lookup_by_id(self, external_id, media_type=None):  
        backend = self._first_with("lookup_by_id")  
        if not backend:  
            return None  
        return backend.lookup_by_id(external_id, media_type=media_type)  
  
    def lookup_tv_chain(self, title, year=None):  
        backend = self._first_with("lookup_tv_chain")  
        if not backend:  
            return None  
        return backend.lookup_tv_chain(title, year=year)