"""  
VISTOR MusicBrainz Authoritative Source  
  
Free, keyless authoritative lookup for music media (music videos, concerts,  
live performances) backed by the MusicBrainz recording search. MusicBrainz  
requires a descriptive User-Agent and asks for <=1 request/second; both are  
honored here. Network import is lazy so importing this module stays offline-safe.  
  
Docs: https://musicbrainz.org/doc/MusicBrainz_API  
"""  
  
import os  
  
from core.logger import Logger  
  
_BASE = "https://musicbrainz.org/ws/2"  
# MusicBrainz REQUIRES a meaningful User-Agent or it returns 403.  
_USER_AGENT = os.environ.get(  
    "VISTOR_USER_AGENT",  
    "VISTOR/0.6 (https://github.com/colinarosenthal/VISTOR)",  
)  
  
_MUSIC_TYPES = ("MusicVideo", "Concert", "LivePerformance", "MUSIC_VIDEO", "CONCERT")  
  
  
class MusicBrainzSource:  
    """Authoritative lookup for music recordings. Never raises to the caller."""  
  
    def __init__(self, timeout=10):  
        self.timeout = timeout  
  
    def handles(self, media_type):  
        return media_type in _MUSIC_TYPES  
  
    def lookup(self, title, year=None, media_type=None):  
        import requests  # lazy  
  
        try:  
            resp = requests.get(  
                f"{_BASE}/recording",  
                params={"query": title, "fmt": "json", "limit": 5},  
                headers={"User-Agent": _USER_AGENT},  
                timeout=self.timeout,  
            )  
            resp.raise_for_status()  
            recordings = resp.json().get("recordings", [])  
        except Exception as exc:  # noqa: BLE001 - best effort  
            Logger.warning(f"MusicBrainz lookup for '{title}' failed: {exc!r}.")  
            return None  
  
        if not recordings:  
            Logger.warning(f"MusicBrainz: no match for '{title}'.")  
            return None  
  
        best = recordings[0]  
        return self._normalize(best)  
  
    def _normalize(self, rec):  
        date = rec.get("first-release-date", "") or ""  
        year = int(date[:4]) if len(date) >= 4 and date[:4].isdigit() else 0  
  
        length_ms = rec.get("length") or 0  
        runtime_minutes = int(round(length_ms / 60000)) if length_ms else 0  
  
        artists = [  
            {"name": c.get("artist", {}).get("name", "")}  
            for c in (rec.get("artist-credit") or [])  
            if c.get("artist", {}).get("name")  
        ]  
        artist_names = ", ".join(a["name"] for a in artists)  
  
        title = rec.get("title", "")  
        description = f"{title} by {artist_names}." if artist_names else title  
  
        return {  
            "title": title,  
            "release_year": year,  
            "runtime_minutes": runtime_minutes,  
            "description": description,  
            "media_type": "MusicVideo",  
            "genres": ["Music"],   # controlled-vocabulary name  
            "cast": artists,       # artist credits reuse the cast slot  
            "crew": [],  
            "studios": [],  
            "poster_url": "",  
        }