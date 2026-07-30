"""  
VISTOR TMDB Authoritative Source  
  
Looks a title up on The Movie Database (https://www.themoviedb.org) and  
normalizes the response. Uses `requests` (already a VISTOR dependency); the  
import is lazy so importing this module never forces a network stack.  
  
Configuration:  
    TMDB_API_KEY environment variable (v3 API key). If it is absent, lookup()  
    returns None and the enricher silently keeps its best-guess values, so the  
    offline smoke test is unaffected.  
"""  
  
import os  
  
from core.logger import Logger  
  
_BASE = "https://api.themoviedb.org/3"  
  
# TMDB genre name -> VISTOR controlled Genre vocabulary name. Only VISTOR's 13  
# names may appear on the right; anything unmapped is dropped.  
_TMDB_GENRE_MAP = {  
    "Action": "Action",  
    "Adventure": "Adventure",  
    "Animation": "Animation",  
    "Comedy": "Comedy",  
    "Drama": "Drama",  
    "Documentary": "Documentary",  
    "Horror": "Horror",  
    "Science Fiction": "Science Fiction",  
    "Fantasy": "Fantasy",  
    "Reality": "Reality",  
    "War": "Action",  
    "Thriller": "Action",  
    "Music": "Music",  
    "History": "Documentary",  
    "Family": "Adventure",  
}  

# TMDB crew "department" -> VISTOR RoleType name. Unmapped crew is dropped.  
_TMDB_DEPARTMENT_ROLE = {  
    "Directing": "DIRECTOR",  
    "Writing": "WRITER",  
    "Production": "PRODUCER",  
    "Sound": "COMPOSER",  
    "Camera": "CINEMATOGRAPHER",  
    "Editing": "EDITOR",  
}
  
class TMDBSource:  
    """Authoritative lookup backed by TMDB's /search + /details endpoints."""  
  
    def __init__(self, api_key=None, timeout=10):  
        self.api_key = api_key or os.environ.get("TMDB_API_KEY", "")  
        self.timeout = timeout  
  
    def lookup(self, title, year=None, media_type=None):  
        if not self.api_key:  
            Logger.info("TMDB_API_KEY not set; skipping authoritative lookup.")  
            return None 
  
        import requests  # lazy: keeps smoke test offline  
  
        endpoint = "movie"  
        if media_type in ("Episode", "TVShow", "TV_SHOW"):  
            endpoint = "tv"  
  
        try:  
            params = {"api_key": self.api_key, "query": title}  
            if year and endpoint == "movie":  
                params["year"] = year  
  
            search = requests.get(  
                f"{_BASE}/search/{endpoint}",  
                params=params,  
                timeout=self.timeout,  
            )  
            search.raise_for_status()  
            results = search.json().get("results", [])  
            if not results:  
                Logger.warning(f"TMDB: no match for '{title}'.")  
                return None  
  
            best = results[0]  
            detail_params = {"api_key": self.api_key, "append_to_response": "credits"}  
            details = requests.get(  
                f"{_BASE}/{endpoint}/{best['id']}",  
                params=detail_params,  
                timeout=self.timeout,  
            )  
            details.raise_for_status()  
            return self._normalize(details.json(), endpoint)
  
        except Exception as exc:  # noqa: BLE001 - lookup is best-effort  
            Logger.warning(f"TMDB lookup for '{title}' failed: {exc!r}.")  
            return None  

  
    # ------------------------------------------------------------------  
    # Normalization  
    # ------------------------------------------------------------------  
  
    def _normalize(self, data, endpoint):  
        if endpoint == "movie":  
            date = data.get("release_date", "") or ""  
            runtime = data.get("runtime", 0) or 0  
            media_type = "Movie"  
            title = data.get("title", "")  
        else:  
            date = data.get("first_air_date", "") or ""  
            runtimes = data.get("episode_run_time") or [0]  
            runtime = runtimes[0] if runtimes else 0  
            media_type = "Episode"  
            title = data.get("name", "")  
  
        year = 0  
        if len(date) >= 4 and date[:4].isdigit():  
            year = int(date[:4])  
  
        genres = []  
        for genre in data.get("genres", []):  
            mapped = _TMDB_GENRE_MAP.get(genre.get("name", ""))  
            if mapped and mapped not in genres:  
                genres.append(mapped)  
  
        credits = data.get("credits", {}) or {}  
  
        cast = [  
            {  
                "tmdb_id": c.get("id"),  
                "name": c.get("name", ""),  
                "character": c.get("character", ""),  
                "order": c.get("order", 0),  
            }  
            for c in (credits.get("cast") or [])  
            if c.get("name")  
        ]  
  
        crew = [  
            {  
                "tmdb_id": c.get("id"),  
                "name": c.get("name", ""),  
                "department": c.get("department", ""),  
                "job": c.get("job", ""),  
            }  
            for c in (credits.get("crew") or [])  
            if c.get("name") and c.get("department") in _TMDB_DEPARTMENT_ROLE  
        ]  
  
        studios = [  
            {"tmdb_id": s.get("id"), "name": s.get("name", "")}  
            for s in (data.get("production_companies") or [])  
            if s.get("name")  
        ]  
  
        return {  
            "title": title,  
            "release_year": year,  
            "runtime_minutes": int(runtime),  
            "description": data.get("overview", "") or "",  
            "media_type": media_type,  
            "genres": genres,  
            "cast": cast,  
            "crew": crew,  
            "studios": studios,  
        }