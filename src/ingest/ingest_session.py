"""  
VISTOR Ingest Session  
  
Backend seam for the drag-and-drop web UI. A thin pass-through that never  
adds its own metadata logic:  
  
    build(url, overrides)          -> RecordBuilder.build (full service chain)  
    search_candidates(title)       -> TMDBSource.search_candidates ("did you mean?")  
    build_from_tmdb(url, tmdb_id)  -> record assembled from a chosen candidate  
    commit(record, download, overwrite) -> MediaIngestor.ingest_records  
  
`poster_url` is a display-only key; it is stripped before commit so it never  
pollutes media.json.  
"""  
  
from metadata.services.link_resolver import LinkResolver  
from metadata.services.record_builder import RecordBuilder, _slugify  
from metadata.services.media_ingestor import MediaIngestor  
from metadata.services.enrichment.tmdb_source import TMDBSource  
  
  
class IngestSession:  
  
    def __init__(self, metadata_path="Metadata/data"):  
        self.builder = RecordBuilder()  
        self.resolver = LinkResolver()  
        self.tmdb = TMDBSource()  
        self.ingestor = MediaIngestor(metadata_path)  
  
    # ------------------------------------------------------------------  
    # Preview (nothing written / downloaded)  
    # ------------------------------------------------------------------  
  
    def build(self, url, overrides=None):  
        """Full service-chain build: resolve -> scrape -> enrich -> classify."""  
        return self.builder.build(url, overrides=overrides)  
  
    def candidates(self, title, media_type=None):  
        """List possible TMDB matches for the 'did you mean...?' side panel."""  
        if not title:  
            return []  
        return self.tmdb.search_candidates(title, media_type=media_type)
  
    def build_from_tmdb(self, url, tmdb_id, media_type="Movie"):  
        """  
        Assemble a record from a specific TMDB candidate the user clicked,  
        keeping the original link as the download source. Falls back to the  
        normal builder if the authoritative lookup returns nothing.  
        """  
  
        provider, reference = self.resolver.resolve(url)  
        info = self.tmdb.lookup_by_id(tmdb_id, media_type=media_type)  
  
        if not info:  
            return self.builder.build(url)  
  
        title = info.get("title", "") or "Untitled"  
        media_id = _slugify(title)  
        rtype = info.get("media_type") or media_type or "Movie"  
  
        record = {  
            "type": rtype,  
            "id": media_id,  
            "title": title,  
            "description": info.get("description", ""),  
            "release_year": info.get("release_year", 0),  
            "runtime_minutes": info.get("runtime_minutes", 0),  
            "scheduling_priority": 0,  
            "genres": list(info.get("genres", [])),  
            "tags": [],  
            "themes": [],  
            "languages": [],  
            "cast": info.get("cast", []),  
            "crew": info.get("crew", []),  
            "studios": info.get("studios", []),  
            "poster_url": info.get("poster_url", ""),  
            "assets": [  
                {  
                    "asset_id": f"{media_id}-asset-1",  
                    "path": self.builder._path_for(rtype, media_id),  
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
        return record  
  
    # ------------------------------------------------------------------  
    # Commit (writes + optionally downloads)  
    # ------------------------------------------------------------------  
  
    def commit(self, record, download=True, overwrite=False):  
        """Merge the (edited) record into media.json and resolve its asset."""  
  
        record = dict(record)  
        record.pop("poster_url", None)  # display-only; keep it out of media.json  
        return self.ingestor.ingest_records(  
            [record], download=download, overwrite=overwrite  
        )