"""  
VISTOR LLM Authoritative Source  
  
Uses an LLM to produce a best-guess normalized record for a title when the  
factual sources (TMDB / IMDb / Wikidata) return nothing. Configuration:  
OPENAI_API_KEY (and optional VISTOR_LLM_MODEL). With no key, lookup() returns  
None and the enricher is a no-op, so the offline smoke test is unaffected.  
  
This is a BEST-GUESS backend and must sit lowest in the composite chain so it  
never overrides an authoritative factual match.  
"""  
  
import json  
import os  
  
from core.logger import Logger  
from metadata.services.enrichment.authoritative_source import AuthoritativeSource  
  
# Only VISTOR's controlled Genre names may be returned by the model.  
_ALLOWED_GENRES = {  
    "Action", "Adventure", "Animation", "Comedy", "Drama", "Documentary",  
    "Horror", "Science Fiction", "Fantasy", "Reality", "Music",  
}  
  
  
class LLMSource(AuthoritativeSource):  
    """Best-guess authoritative lookup backed by an LLM."""  
  
    def __init__(self, api_key=None, model=None, timeout=20):  
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")  
        self.model = model or os.environ.get("VISTOR_LLM_MODEL", "gpt-4o-mini")  
        self.timeout = timeout  
  
    def lookup(self, title, year=None, media_type=None):  
        if not self.api_key:  
            Logger.info("OPENAI_API_KEY not set; skipping LLM lookup.")  
            return None  
  
        import requests  # lazy: keeps smoke test offline  
  
        prompt = (  
            "Return ONLY compact JSON with keys title, release_year (int), "  
            "runtime_minutes (int), description, media_type ('Movie' or "  
            "'Episode'), genres (subset of "  
            f"{sorted(_ALLOWED_GENRES)}). Title: {title!r}"  
            + (f", year {year}" if year else "")  
        )  
  
        try:  
            resp = requests.post(  
                "https://api.openai.com/v1/chat/completions",  
                headers={"Authorization": f"Bearer {self.api_key}"},  
                json={  
                    "model": self.model,  
                    "messages": [{"role": "user", "content": prompt}],  
                    "response_format": {"type": "json_object"},  
                    "temperature": 0,  
                },  
                timeout=self.timeout,  
            )  
            resp.raise_for_status()  
            content = resp.json()["choices"][0]["message"]["content"]  
            data = json.loads(content)  
        except Exception as exc:  # noqa: BLE001 - best-effort  
            Logger.warning(f"LLM lookup for '{title}' failed: {exc!r}.")  
            return None  
  
        genres = [g for g in data.get("genres", []) if g in _ALLOWED_GENRES]  
  
        return {  
            "title": data.get("title", title),  
            "release_year": int(data.get("release_year") or 0),  
            "runtime_minutes": int(data.get("runtime_minutes") or 0),  
            "description": data.get("description", ""),  
            "media_type": data.get("media_type") or "Movie",  
            "genres": genres,  
        }