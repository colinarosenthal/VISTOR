"""  
VISTOR Record Builder  
  
Builds a complete media record (the dict MediaIngestor/MetadataLoader  
consume) from a single pasted link, auto-filling descriptive metadata.  
  
    RecordBuilder().build("https://youtu.be/fzHD04_OwyQ", media_type="Movie")  
  
Anything the scraper cannot supply falls back to caller-provided overrides,  
then to safe defaults, so the record is always ingest-ready.  
"""  
  
import re  
  
from core.logger import Logger  
from metadata.services.link_resolver import LinkResolver  
from metadata.services.media_describer import MediaDescriber  
  
  
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
  
    def __init__(self, resolver=None, describer=None):  
        self.resolver = resolver or LinkResolver()  
        self.describer = describer or MediaDescriber()  
  
    def build(self, url, media_type="Movie", overrides=None):  
        overrides = overrides or {}  
  
        provider, reference = self.resolver.resolve(url)  
        scraped = self.describer.describe(provider, reference)  
  
        # Precedence: explicit overrides > scraped > defaults.  
        title = overrides.get("title") or scraped.get("title") or "Untitled"  
        media_id = overrides.get("id") or _slugify(title)  
  
        record = {  
            "type": overrides.get("type", media_type),  
            "id": media_id,  
            "title": title,  
            "description": overrides.get("description")  
                or scraped.get("description", ""),  
            "release_year": overrides.get("release_year")  
                or scraped.get("release_year", 0),  
            "runtime_minutes": overrides.get("runtime_minutes")  
                or scraped.get("runtime_minutes", 0),  
            "scheduling_priority": overrides.get("scheduling_priority", 0),  
            "genres": overrides.get("genres", []),  
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
  
        Logger.success(  
            f"Built record '{media_id}' from {provider}:{reference}."  
        )  
        return record  
  
    def _path_for(self, media_type, media_id):  
        folder = self.LOCAL_DIRS.get(media_type, "Media")  
        return f"Media/{folder}/{media_id}.mkv"