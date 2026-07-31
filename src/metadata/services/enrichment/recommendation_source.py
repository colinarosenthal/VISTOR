"""  
VISTOR Recommendation Source  
  
Wraps TMDB's /recommendations endpoint so the ingest UI can suggest  
"you might also add..." titles based on a title the operator just  
previewed or committed. Best-effort and offline-safe: with no  
TMDB_API_KEY (or on any failure) recommend() returns an empty list,  
exactly like TMDBSource's other methods.  
  
Return shape matches TMDBSource.search_candidates() so the same UI  
chip renderer and /choose flow can consume it unchanged:  
  
    [  
        {  
            "tmdb_id": int,  
            "title": str,  
            "release_year": int,  
            "media_type": "Movie" | "Episode",  
            "poster_url": str,  
        },  
        ...  
    ]  
"""  
  
import os  
  
from core.logger import Logger  
  
_BASE = "https://api.themoviedb.org/3"  
_POSTER_BASE = "https://image.tmdb.org/t/p/w200"  
  
  
class RecommendationSource:  
    """Suggests similar titles via TMDB's /recommendations endpoint."""  
  
    def __init__(self, api_key=None, timeout=10):  
        self.api_key = api_key or os.environ.get("TMDB_API_KEY", "")  
        self.timeout = timeout  
  
    def recommend(self, tmdb_id, media_type="Movie", limit=8):  
        """Return up to `limit` similar-title candidates for a TMDB id.  
  
        Offline / without a key / on failure -> []. The candidate dicts  
        are the same shape TMDBSource.search_candidates() emits, so they  
        can flow straight into the /choose route.  
        """  
  
        if not self.api_key:  
            Logger.info("TMDB_API_KEY not set; no recommendations.")  
            return []  
  
        if not tmdb_id:  
            return []  
  
        import requests  # lazy: keeps the offline smoke test network-free  
  
        endpoint = "tv" if media_type in ("Episode", "TVShow", "TV_SHOW") else "movie"  
  
        try:  
            resp = requests.get(  
                f"{_BASE}/{endpoint}/{tmdb_id}/recommendations",  
                params={"api_key": self.api_key},  
                timeout=self.timeout,  
            )  
            resp.raise_for_status()  
            results = resp.json().get("results", [])  
        except Exception as exc:  # noqa: BLE001 - recommendations are best-effort  
            Logger.warning(  
                f"TMDB recommendations for {endpoint}:{tmdb_id} failed: {exc!r}."  
            )  
            return []  
  
        candidates = []  
        for r in results[:limit]:  
            date = r.get("release_date") or r.get("first_air_date") or ""  
            year = int(date[:4]) if len(date) >= 4 and date[:4].isdigit() else 0  
            poster = r.get("poster_path")  
            candidates.append(  
                {  
                    "tmdb_id": r.get("id"),  
                    "title": r.get("title") or r.get("name") or "",  
                    "release_year": year,  
                    "media_type": "Movie" if endpoint == "movie" else "Episode",  
                    "poster_url": f"{_POSTER_BASE}{poster}" if poster else "",  
                }  
            )  
        return candidates