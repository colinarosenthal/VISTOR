"""  
VISTOR Record Builder  
  
Builds a complete media record (the dict MediaIngestor/MetadataLoader  
consume) from a single pasted link, auto-filling descriptive metadata.  
  
    RecordBuilder().build("https://youtu.be/fzHD04_OwyQ")  
  
Field precedence (highest wins):  
  
    explicit overrides  >  authoritative source (TMDB)  >  classifier guess  
                        >  scraped info-dict  >  safe default  
  
The classifier fills `type`/`genres` when the caller does not; the  
authoritative enricher fills any field still empty/zero from an external  
source (TMDB). Everything degrades gracefully offline, so the record is  
always ingest-ready even with no network, no API key, and no yt-dlp.  
"""  
  
import re  
  
from core.logger import Logger 

from metadata.services.link_resolver import LinkResolver  
from metadata.services.media_describer import MediaDescriber  
from metadata.services.media_classifier import MediaClassifier 

from metadata.services.enrichment.metadata_enricher import MetadataEnricher 
from metadata.services.enrichment.tmdb_source import TMDBSource 
  
  
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
        self.enricher = enricher or MetadataEnricher(TMDBSource())
  
    def build(self, url, media_type=None, overrides=None):  
        overrides = overrides or {}  
  
        provider, reference = self.resolver.resolve(url)  
        scraped = self.describer.describe(provider, reference)  
  
        # --- Type: override > classifier guess > media_type arg > default ---  
        media_type = (  
            overrides.get("type")  
            or media_type  
            or self.classifier.classify_type(scraped)  
            or "Movie"  
        )  
  
        # --- Genres: override > classifier guess > empty ---  
        if overrides.get("genres"):  
            genres = list(overrides["genres"])  
        else:  
            genres = self.classifier.classify_genres(scraped)  
  
        # --- Descriptive fields: override > scraped > default ---  
        title = overrides.get("title") or scraped.get("title") or "Untitled"  
        media_id = overrides.get("id") or _slugify(title)  
  
        record = {  
            "type": media_type,  
            "id": media_id,  
            "title": title,  
            "description": overrides.get("description")  
                or scraped.get("description", ""),  
            "release_year": overrides.get("release_year")  
                or scraped.get("release_year", 0),  
            "runtime_minutes": overrides.get("runtime_minutes")  
                or scraped.get("runtime_minutes", 0),  
            "scheduling_priority": overrides.get("scheduling_priority", 0),  
            "genres": genres,  
            "tags": overrides.get("tags", []),  
            "themes": overrides.get("themes", []),  
            "languages": overrides.get("languages", []),  
            "assets": [  
                {  
                    "asset_id": f"{media_id}-asset-1",  
                    "path": self._path_for(media_type, media_id),  
                    "sources": [  
                        {  
                            "provider": provider,  
                            "reference": reference,  
                            "quality": "",  
                            "date_posted": "",  
                        }  
                    ],  
                }  
            ],  
        }  
  
        # --- Authoritative enrichment: fills any field still empty/zero ---  
        # (title/year/genres/description/runtime) from TMDB. No-op offline or  
        # without TMDB_API_KEY, and never overwrites a non-empty value, so  
        # explicit overrides and confident classifier guesses always survive.  
        record = self.enricher.enrich(record)  
  
        Logger.success(  
            f"Built record '{media_id}' ({record['type']}) "  
            f"from {provider}:{reference}."  
        )  
        return record  
  
    def _path_for(self, media_type, media_id):  
        folder = self.LOCAL_DIRS.get(media_type, "Media")  
        return f"Media/{folder}/{media_id}.mkv"