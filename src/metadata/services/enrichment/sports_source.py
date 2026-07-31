"""  
VISTOR SportsSource  
  
Authoritative-ish enrichment for sports events, backed by TheSportsDB  
(https://www.thesportsdb.com). Chosen for its deep historical backlog of  
event/season data (1980s onward) on a permanent free tier.  
  
Returns the SAME normalized dict shape as TMDBSource.lookup() so it drops  
straight into MetadataEnricher with no changes there. Degrades to None on  
no key / no network / no match, so the pipeline stays offline-safe.  
  
Configuration:  
    VISTOR_SPORTSDB_KEY  -- v1 API key. Defaults to the free public test  
                            key "123" (also documented as "3"). Sufficient  
                            for the low request volume of manual ingest.  
"""  
  
import os  
  
from core.logger import Logger  
  
_BASE = "https://www.thesportsdb.com/api/v1/json"  
  
# Media types this source is responsible for.  
SPORTS_TYPES = {"SportsEvent", "SportsTalk", "SPORTS_EVENT", "SPORTS_TALK"}  
  
  
class SportsSource:  
    """Look a sports event up on TheSportsDB and normalize the response."""  
  
    def __init__(self, api_key=None, timeout=10):  
        self.api_key = api_key or os.environ.get("VISTOR_SPORTSDB_KEY", "123")  
        self.timeout = timeout  
  
    def lookup(self, title, year=None, media_type=None):  
        if not self.api_key:  
            Logger.info("VISTOR_SPORTSDB_KEY not set; skipping sports lookup.")  
            return None  
  
        import requests  # lazy, mirrors TMDBSource  
  
        try:  
            resp = requests.get(  
                f"{_BASE}/{self.api_key}/searchevents.php",  
                params={"e": title},  
                timeout=self.timeout,  
            )  
            resp.raise_for_status()  
            events = resp.json().get("event") or []  
            if not events:  
                Logger.warning(f"TheSportsDB: no match for '{title}'.")  
                return None  
  
            # If a year was given, prefer the event from that season/year.  
            best = events[0]  
            if year:  
                for ev in events:  
                    date = (ev.get("dateEvent") or "")[:4]  
                    if date.isdigit() and int(date) == int(year):  
                        best = ev  
                        break  
  
            return self._normalize(best, media_type)  
  
        except Exception as exc:  # noqa: BLE001 - lookup is best-effort  
            Logger.warning(f"TheSportsDB lookup for '{title}' failed: {exc!r}.")  
            return None  
  
    @staticmethod  
    def _normalize(ev, media_type):  
        date = ev.get("dateEvent") or ""  
        year = int(date[:4]) if len(date) >= 4 and date[:4].isdigit() else 0  
  
        league = ev.get("strLeague") or ""  
        season = ev.get("strSeason") or ""  
        desc = ev.get("strDescriptionEN") or ""  
        if not desc:  
            home, away = ev.get("strHomeTeam", ""), ev.get("strAwayTeam", "")  
            if home and away:  
                desc = f"{league} {season}: {home} vs {away}.".strip()  
  
        poster = ev.get("strThumb") or ev.get("strPoster") or ""  
  
        return {  
            "title": ev.get("strEvent") or "",  
            "release_year": year,  
            "runtime_minutes": 0,          # not provided by TheSportsDB  
            "description": desc,  
            "media_type": media_type or "SportsEvent",  
            "genres": ["Sports"],          # matches the VISTOR genre vocabulary  
            "cast": [],  
            "crew": [],  
            "studios": [],  
            "poster_url": poster,  
        }