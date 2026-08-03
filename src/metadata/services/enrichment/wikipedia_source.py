"""  
VISTOR Wikipedia Authoritative Source  
  
Free, keyless general-purpose fallback. There is no catalog API for  
commercials, station IDs, promos, infomercials, or ambient loops, so a  
Wikipedia page summary is the best available free description for those types  
and for any title the domain sources miss. Network import is lazy.  
  
Docs: https://en.wikipedia.org/api/rest_v1/  
"""  
  
from urllib.parse import quote  
  
from core.logger import Logger
from metadata.services.enrichment.authoritative_source import AuthoritativeSource 
  
_BASE = "https://en.wikipedia.org/api/rest_v1/page/summary"  
  
  
class WikipediaSource(AuthoritativeSource):  
    """Best-effort description lookup. Never raises to the caller."""  
  
    def __init__(self, timeout=10):  
        self.timeout = timeout  
  
    # Handles nothing exclusively; used only as the router's fallback.  
    def handles(self, media_type):  
        return False  
  
    def lookup(self, title, year=None, media_type=None):  
        import requests  # lazy  
  
        try:  
            resp = requests.get(  
                f"{_BASE}/{quote(title)}",  
                headers={"User-Agent": "VISTOR/0.6"},  
                timeout=self.timeout,  
            )  
            if resp.status_code == 404:  
                Logger.warning(f"Wikipedia: no page for '{title}'.")  
                return None  
            resp.raise_for_status()  
            data = resp.json()  
        except Exception as exc:  # noqa: BLE001 - best effort  
            Logger.warning(f"Wikipedia lookup for '{title}' failed: {exc!r}.")  
            return None  
  
        extract = data.get("extract", "") or ""  
        if not extract:  
            return None  
  
        return {  
            "title": data.get("title", title),  
            "release_year": 0,  
            "runtime_minutes": 0,  
            "description": extract,  
            # Preserve the caller's intended type; Wikipedia can't classify.  
            "media_type": media_type or "",  
            "genres": [],  
            "cast": [],  
            "crew": [],  
            "studios": [],  
            "poster_url": (data.get("thumbnail") or {}).get("source", ""),  
        }