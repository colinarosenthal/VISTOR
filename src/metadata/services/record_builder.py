"""  
VISTOR Record Builder  
  
Builds a complete media record (the dict MediaIngestor/MetadataLoader  
consume) from a single pasted link, auto-filling descriptive metadata.  
  
    RecordBuilder().build("https://youtu.be/fzHD04_OwyQ")  
  
Field precedence (highest wins):  
  
    explicit overrides  >  authoritative source  >  classifier guess  
                        >  scraped info-dict     >  safe default  
  
The media TYPE is resolved BEFORE enrichment (explicit override, else the  
classifier's guess from the scrape) so the authoritative backend is chosen for  
that type: movies/TV go to TMDB, music videos go to MusicBrainz. Both live in  
the CompositeSource returned by default_source(), which is offline-safe.  
"""  
  
import re  
  
from core.logger import Logger  
  
from metadata.services.link_resolver import LinkResolver  
from metadata.services.media_describer import MediaDescriber  
from metadata.services.media_classifier import MediaClassifier  
  
from metadata.services.enrichment.metadata_enricher import MetadataEnricher  
from metadata.services.enrichment import default_source  
  
  
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
        # CompositeSource(TMDB + MusicBrainz). Each backend's handles() hook  
        # decides which media types it answers, so routing is per-type.  
        self.enricher = enricher or MetadataEnricher(default_source())  
  
    def build(self, url, media_type=None, overrides=None):  
        overrides = overrides or {}  
  
        provider, reference = self.resolver.resolve(url)  
        scraped = self.describer.describe(provider, reference)  
  
        title = overrides.get("title") or scraped.get("title") or "Untitled"  
        media_id = overrides.get("id") or _slugify(title)  
  
        # --- Layer 1: EXPLICIT OVERRIDES (highest) -----------------------  
        record = {  
            "type": overrides.get("type") or media_type or "",  
            "id": media_id,  
            "title": title,  
            "poster_url": overrides.get("poster_url", ""),  
            "description": overrides.get("description", ""),  
            "release_year": overrides.get("release_year", 0),  
            "runtime_minutes": overrides.get("runtime_minutes", 0),  
            "scheduling_priority": overrides.get("scheduling_priority", 0),  
            "genres": list(overrides.get("genres", [])),  
            "music_genre": overrides.get("music_genre", ""),  
            "tags": overrides.get("tags", []),  
            "themes": overrides.get("themes", []),  
            "languages": overrides.get("languages", []),  
            "season_number": overrides.get("season_number", 0),  
            "episode_number": overrides.get("episode_number", 0),  
        }  
  
        # --- Resolve TYPE up front so enrichment routes to the right API ---  
        # An explicit type is sticky; otherwise use the classifier's guess.  
        # This is what lets MusicBrainz (which only handles MusicVideo) run.  
        if not record["type"]:  
            guessed = self.classifier.classify_type(scraped)  
            if guessed:  
                record["type"] = guessed  
  
        # --- Layer 2: AUTHORITATIVE SOURCE (routed by type) --------------  
        # The scraped year is provisional (e.g. a YouTube upload date), so mark  
        # it so the authoritative first-release year replaces it.  
        provisional = set()  
        if not overrides.get("release_year") and scraped.get("release_year"):  
            record["release_year"] = scraped["release_year"]  
            provisional.add("release_year")  
        if record["type"] and not overrides.get("type"):  
            provisional.add("type")  
        if not overrides.get("genres"):  
            provisional.add("genres")  
  
        record = self.enricher.enrich(record, provisional=provisional)  
  
        # --- TV episode chain (TMDB only) --------------------------------  
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
  
        # --- Layer 3: CLASSIFIER GUESS (remaining genre fill) ------------  
        if not record["type"]:  
            guessed = self.classifier.classify_type(scraped)  
            if guessed:  
                record["type"] = guessed  
        if not record["genres"]:  
            record["genres"] = self.classifier.classify_genres(scraped)  
  
        # --- Layer 4: SCRAPED INFO-DICT (LAST, above defaults) -----------  
        self._fill(record, "description", scraped.get("description"))  
        self._fill(record, "release_year", scraped.get("release_year"))  
        self._fill(record, "runtime_minutes", scraped.get("runtime_minutes"))  
        self._fill(record, "poster_url", scraped.get("poster_url"))  
  
        # --- Layer 5: SAFE DEFAULTS (lowest) -----------------------------  
        if not record["type"]:  
            record["type"] = "Movie"  
        if not record["title"]:  
            record["title"] = "Untitled"  
  
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