"""  
VISTOR Record Builder  
  
Builds a complete media record (the dict MediaIngestor/MetadataLoader  
consume) from a single pasted link, auto-filling descriptive metadata.  
  
    RecordBuilder().build("https://youtu.be/fzHD04_OwyQ")  
  
Field precedence (highest wins):  
  
    explicit overrides  >  authoritative source (TMDB)  >  classifier guess  
                        >  scraped info-dict  >  safe default  
  
This is implemented as fill-if-empty layering applied in precedence order,  
HIGHEST FIRST (the first writer of a field wins): explicit overrides are  
seeded first, then the authoritative enricher (TMDB), then the classifier  
guess, then the scraped info-dict, and finally the safe defaults. Scraped  
values are therefore applied LAST, just above the hard defaults, so an  
authoritative TMDB value (e.g. a real release year) always beats a scrape  
(e.g. the YouTube upload year) without any "provisional" bookkeeping.  
  
Everything degrades gracefully offline, so the record is always  
ingest-ready even with no network, no API key, and no yt-dlp.  
"""  
  
import re  
  
from core.logger import Logger  
  
from metadata.services.link_resolver import LinkResolver  
from metadata.services.media_describer import MediaDescriber  
from metadata.services.media_classifier import MediaClassifier  
  
from metadata.services.enrichment.metadata_enricher import MetadataEnricher  
from metadata.services.enrichment.enrichment_router import EnrichmentRouter
from metadata.services.enrichment.composite_source import CompositeSource  
  
  
def _slugify(text):  
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")  
    return slug or "untitled"  
  
  
class RecordBuilder:  
  
    LOCAL_DIRS = {  
        "Movie": "Movies",  
        "Episode": "Episodes",  
        "MusicVideo": "MusicVideos",  
        "Commercial": "Commercials",  
    }  
  
    def __init__(  
        self,  
        resolver=None,  
        describer=None,  
        classifier=None,  
        enricher=None,  
    ):  
        self.resolver = resolver or LinkResolver()  
        self.describer = describer or MediaDescriber()  
        self.classifier = classifier or MediaClassifier()  
        self.enricher = enricher or MetadataEnricher(EnrichmentRouter())  
  
    def build(self, url, media_type=None, overrides=None):  
        overrides = overrides or {}  
  
        provider, reference = self.resolver.resolve(url)  
        scraped = self.describer.describe(provider, reference)  
  
        # Title is needed both as the id seed and as the TMDB lookup key, so  
        # resolve it up front: explicit override wins, else the scrape, else a  
        # safe default. (TMDB may still refine other descriptive fields.)  
        title = overrides.get("title") or scraped.get("title") or "Untitled"  
        media_id = overrides.get("id") or _slugify(title)  
  
        # --- Layer 1: EXPLICIT OVERRIDES (highest) -----------------------  
        # Seed only what the caller explicitly supplied. An explicit --type  
        # (as override or as the media_type arg) is sticky: nothing below may  
        # overwrite it. Every other field is left empty/zero so the lower  
        # layers can fill it in strict precedence order.  
        record = {  
            "type": overrides.get("type") or media_type or "",  
            "id": media_id,  
            "title": title,  
            "description": overrides.get("description", ""),  
            "release_year": overrides.get("release_year", 0),  
            "runtime_minutes": overrides.get("runtime_minutes", 0),  
            "scheduling_priority": overrides.get("scheduling_priority", 0),  
            "genres": list(overrides.get("genres", [])),  
            "tags": overrides.get("tags", []),  
            "themes": overrides.get("themes", []),  
            "languages": overrides.get("languages", []),
            "season_number": overrides.get("season_number", 0),  
            "episode_number": overrides.get("episode_number", 0),
        }  
  
        # --- Layer 2: AUTHORITATIVE SOURCE (TMDB) ------------------------  
        # Fills only empty/zero fields, so it beats the classifier and the  
        # scrape but never an override. No-op offline / without TMDB_API_KEY  
        # / on no match. NOTE: enrich() reads record["title"] as its lookup  
        # key, so the (override-or-scraped) title above seeds the query.  
        record = self.enricher.enrich(record)

        # --- TV episode chain: fetch the whole Series -> Season -> Episode  
        # structure so the ingestor can persist the full backlog, not just  
        # the dropped episode. No-op offline / without TMDB_API_KEY.  
        if (overrides.get("type") or media_type) == "Episode":  
            source = getattr(self.enricher, "source", None)  
            if source and hasattr(source, "lookup_tv_chain"):  
                chain = source.lookup_tv_chain(  
                    record["title"],  
                    year=overrides.get("release_year") or None,  
                )  
                if chain:  
                    record["tv_chain"] = chain  
                    record["season_number"] = overrides.get("season_number", 1)  
                    record["episode_number"] = overrides.get("episode_number", 1)
  
        # --- Layer 3: CLASSIFIER GUESS -----------------------------------  
        # Deterministic offline best-guess for the two fields the classifier  
        # owns; only fills if TMDB/override left them empty.  
        if not record["type"]:  
            guessed = self.classifier.classify_type(scraped)  
            if guessed:  
                record["type"] = guessed  
        if not record["genres"]:  
            record["genres"] = self.classifier.classify_genres(scraped)  
  
        # --- Layer 4: SCRAPED INFO-DICT (LAST, above defaults) -----------  
        # Fills anything still empty/zero from the download-free scrape.  
        self._fill(record, "description", scraped.get("description"))  
        self._fill(record, "release_year", scraped.get("release_year"))  
        self._fill(record, "runtime_minutes", scraped.get("runtime_minutes"))  
  
        # --- Layer 5: SAFE DEFAULTS (lowest) -----------------------------  
        if not record["type"]:  
            record["type"] = "Movie"  
        if not record["title"]:  
            record["title"] = "Untitled"  
  
        # Attach the single source asset now that the type (folder) is final.  
        record["assets"] = [  
            {  
                "asset_id": f"{media_id}-asset-1",  
                "path": self._path_for(record["type"], media_id),  
                "sources": [  
                    {  
                        "provider": provider,  
                        "reference": reference,  
                        "quality": "",  
                        "date_posted": "",  
                    }  
                ],  
            }  
        ]  
  
        Logger.success(  
            f"Built record '{media_id}' ({record['type']}) "  
            f"from {provider}:{reference}."  
        )  
        return record  
  
    @staticmethod  
    def _fill(record, key, value):  
        """Set record[key] only if the current value is empty/zero/absent."""  
  
        if value in (None, "", 0):  
            return  
        if not record.get(key):  
            record[key] = value  
  
    def _path_for(self, media_type, media_id):  
        folder = self.LOCAL_DIRS.get(media_type, "Media")  
        return f"Media/{folder}/{media_id}.mkv"