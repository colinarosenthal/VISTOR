"""  
VISTOR IMDb (OMDb) Authoritative Source  
  
IMDb exposes no free official API, so this backend reads IMDb data through  
the OMDb API (https://www.omdbapi.com). It normalizes to the same shape as  
TMDBSource. Configuration: OMDB_API_KEY. With no key, lookup() returns None  
and the enricher is a no-op, so the offline smoke test is unaffected.  
"""  
  
import os  
  
from core.logger import Logger  
from metadata.services.enrichment.authoritative_source import AuthoritativeSource  
  
_BASE = "https://www.omdbapi.com/"  
  
_IMDB_GENRE_MAP = {  
    "Action": "Action",  
    "Adventure": "Adventure",  
    "Animation": "Animation",  
    "Comedy": "Comedy",  
    "Drama": "Drama",  
    "Documentary": "Documentary",  
    "Horror": "Horror",  
    "Sci-Fi": "Science Fiction",  
    "Fantasy": "Fantasy",  
    "War": "Action",  
    "Thriller": "Action",  
    "Music": "Music",  
    "Musical": "Music",  
    "History": "Documentary",  
    "Family": "Adventure",  
}  
  
  
class IMDbSource(AuthoritativeSource):  
    """Authoritative lookup backed by OMDb (IMDb data)."""  
  
    def __init__(self, api_key=None, timeout=10):  
        self.api_key = api_key or os.environ.get("OMDB_API_KEY", "")  
        self.timeout = timeout  
  
    def lookup(self, title, year=None, media_type=None):  
        if not self.api_key:  
            Logger.info("OMDB_API_KEY not set; skipping IMDb lookup.")  
            return None  
  
        import requests  # lazy: keeps smoke test offline  
  
        params = {"apikey": self.api_key, "t": title}  
        if year:  
            params["y"] = year  
        if media_type in ("Episode", "TVShow", "TV_SHOW"):  
            params["type"] = "series"  
        elif media_type == "Movie":  
            params["type"] = "movie"  
  
        try:  
            resp = requests.get(_BASE, params=params, timeout=self.timeout)  
            resp.raise_for_status()  
            data = resp.json()  
        except Exception as exc:  # noqa: BLE001 - best-effort  
            Logger.warning(f"IMDb lookup for '{title}' failed: {exc!r}.")  
            return None  
  
        if data.get("Response") != "True":  
            Logger.warning(f"IMDb: no match for '{title}'.")  
            return None  
  
        return self._normalize(data)  
  
    @staticmethod  
    def _int(value):  
        try:  
            return int(str(value).split("\u2013")[0].split("-")[0].strip())  
        except (ValueError, AttributeError):  
            return 0  
  
    def _normalize(self, data):  
        genres = []  
        for raw in (data.get("Genre", "") or "").split(","):  
            mapped = _IMDB_GENRE_MAP.get(raw.strip())  
            if mapped and mapped not in genres:  
                genres.append(mapped)  
  
        runtime = self._int((data.get("Runtime", "") or "").replace(" min", ""))  
        is_series = (data.get("Type") == "series")  
  
        return {  
            "title": data.get("Title", ""),  
            "release_year": self._int(data.get("Year", "")),  
            "runtime_minutes": runtime,  
            "description": data.get("Plot", "") or "",  
            "media_type": "Episode" if is_series else "Movie",  
            "genres": genres,  
        }