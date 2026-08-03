"""  
VISTOR Wikidata Authoritative Source  
  
Queries the public Wikidata SPARQL endpoint (no API key required) for a title  
and normalizes the result. Network import is lazy so importing this module  
never forces a network stack; on any failure it returns None so the enricher  
degrades gracefully.  
"""  
  
from core.logger import Logger  
from metadata.services.enrichment.authoritative_source import AuthoritativeSource  
  
_ENDPOINT = "https://query.wikidata.org/sparql"  
  
_QUERY = """  
SELECT ?item ?itemLabel ?year ?runtime ?desc WHERE {  
  ?item rdfs:label "%s"@en ;  
        wdt:P31 ?type .  
  VALUES ?type { wd:Q11424 wd:Q5398426 }   # film, television series  
  OPTIONAL { ?item wdt:P577 ?pub . BIND(YEAR(?pub) AS ?year) }  
  OPTIONAL { ?item wdt:P2047 ?runtime }  
  OPTIONAL { ?item schema:description ?desc . FILTER(LANG(?desc) = "en") }  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }  
}  
LIMIT 1  
"""  
  
  
class WikidataSource(AuthoritativeSource):  
    """Authoritative lookup backed by Wikidata SPARQL (keyless)."""  
  
    def __init__(self, timeout=10):  
        self.timeout = timeout  
  
    def lookup(self, title, year=None, media_type=None):  
        import requests  # lazy: keeps smoke test offline  
  
        query = _QUERY % title.replace('"', '\\"')  
        try:  
            resp = requests.get(  
                _ENDPOINT,  
                params={"query": query, "format": "json"},  
                headers={"User-Agent": "VISTOR/1.0 (enrichment)"},  
                timeout=self.timeout,  
            )  
            resp.raise_for_status()  
            bindings = resp.json().get("results", {}).get("bindings", [])  
        except Exception as exc:  # noqa: BLE001 - best-effort  
            Logger.warning(f"Wikidata lookup for '{title}' failed: {exc!r}.")  
            return None  
  
        if not bindings:  
            Logger.warning(f"Wikidata: no match for '{title}'.")  
            return None  
  
        row = bindings[0]  
  
        def _val(key):  
            return (row.get(key, {}) or {}).get("value", "")  
  
        try:  
            release_year = int(_val("year")) if _val("year") else 0  
        except ValueError:  
            release_year = 0  
        try:  
            runtime = int(float(_val("runtime"))) if _val("runtime") else 0  
        except ValueError:  
            runtime = 0  
  
        return {  
            "title": _val("itemLabel") or title,  
            "release_year": release_year,  
            "runtime_minutes": runtime,  
            "description": _val("desc"),  
            # Wikidata gives no controlled-vocabulary genres, so leave empty.  
            "genres": [],  
        }