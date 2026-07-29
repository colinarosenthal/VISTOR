"""  
VISTOR Media Ingestor  
  
Single entry point for adding media to VISTOR from JSON.  
  
A drop-in JSON file describes one or more media items (each optionally  
carrying an `assets` array with ranked `sources`). The ingestor:  
  
    1. Reads and validates the drop-in records.  
    2. Merges them into Metadata/data/media.json (dedupe by id).  
    3. Reloads the library via MetadataLoader so every record becomes a  
       fully-wired MediaItem + MediaAsset (JSON -> object).  
    4. Auto-resolves any asset still marked NOT_DOWNLOADED using the  
       production RealFetcher + SourceResolver, so adding media also  
       downloads, probes, and fingerprints it.  
  
This is the seam a future UI targets: the GUI just emits the same JSON.  
  
Network imports are lazy so the headless test suite runs offline.  
"""  
  
import json  
  
from pathlib import Path  
  
from core.logger import Logger  
from metadata.services.metadata_loader import MetadataLoader  
from metadata.enums.download_status import DownloadStatus  
  
  
# Media types the loader's type-switch can currently reconstruct.  
SUPPORTED_TYPES = ("Movie", "Commercial", "MusicVideo", "Episode")  
  
  
class MediaIngestor:  
    """Adds media to the catalog from JSON and optionally downloads it."""  
  
    def __init__(self, metadata_path="Metadata/data"):  
        self.metadata_path = Path(metadata_path)  
        self.media_json = self.metadata_path / "media.json"  
  
    # ------------------------------------------------------------------  
    # Public Interface  
    # ------------------------------------------------------------------  
  
    def ingest_file(self, drop_in_path, download=True):  
        """  
        Ingest a drop-in JSON file (a single record or a list of records).  
  
        Returns a report dictionary:  
            {  
                "added": [id, ...],  
                "skipped": [(id, reason), ...],  
                "resolved": [id, ...],  
                "unresolved": [id, ...],  
            }  
        """  
  
        records = self._read_records(drop_in_path)  
  
        return self.ingest_records(records, download=download)  
  
    def ingest_records(self, records, download=True):  
        """Ingest already-parsed records (list of dicts)."""  
  
        report = {  
            "added": [],  
            "skipped": [],  
            "resolved": [],  
            "unresolved": [],  
        }  
  
        existing = self._read_media_json()  
        existing_ids = {r.get("id") for r in existing}  
  
        for record in records:  
  
            problem = self._validate(record, existing_ids)  
  
            if problem is not None:  
                report["skipped"].append((record.get("id", "?"), problem))  
                Logger.warning(  
                    f"Skipping media record '{record.get('id', '?')}': "  
                    f"{problem}."  
                )  
                continue  
  
            existing.append(record)  
            existing_ids.add(record["id"])  
            report["added"].append(record["id"])  
  
            Logger.success(f"Ingested media record '{record['id']}'.")  
  
        # Persist the merged catalog before reloading.  
        self._write_media_json(existing)  
  
        if download and report["added"]:  
            self._resolve_new_assets(report)  
  
        Logger.info(  
            f"Ingestion complete: {len(report['added'])} added, "  
            f"{len(report['skipped'])} skipped, "  
            f"{len(report['resolved'])} downloaded."  
        )  
  
        return report  
  
    # ------------------------------------------------------------------  
    # Validation  
    # ------------------------------------------------------------------  
  
    def _validate(self, record, existing_ids):  
        """Return a reason string if the record is invalid, else None."""  
  
        if not isinstance(record, dict):  
            return "record is not a JSON object"  
  
        for field in ("type", "id", "title"):  
            if field not in record:  
                return f"missing required field '{field}'"  
  
        if record["type"] not in SUPPORTED_TYPES:  
            return (  
                f"type '{record['type']}' is not loadable yet "  
                f"(supported: {', '.join(SUPPORTED_TYPES)})"  
            )  
  
        if record["id"] in existing_ids:  
            return "id already exists in media.json"  
  
        return None  
  
    # ------------------------------------------------------------------  
    # Download / Resolution  
    # ------------------------------------------------------------------  
  
    def _resolve_new_assets(self, report):  
        """Reload the library and resolve every NOT_DOWNLOADED asset."""  
  
        # Lazy import so importing MediaIngestor never requires network deps.  
        from metadata.services.source_resolver import SourceResolver  
        from metadata.services.fetchers.real_fetcher import RealFetcher  
  
        library = MetadataLoader().load(self.metadata_path)  
  
        real = RealFetcher()  
        resolver = SourceResolver(real)  
  
        added = set(report["added"])  
  
        for item in library.get_media():  
  
            if item.get_id() not in added:  
                continue  
  
            for asset in item.get_media_assets():  
  
                if asset.get_download_status() != DownloadStatus.NOT_DOWNLOADED:  
                    continue  
  
                if not asset.get_sources():  
                    Logger.warning(  
                        f"Asset '{asset.get_asset_id()}' has no sources; "  
                        f"cannot auto-download."  
                    )  
                    report["unresolved"].append(item.get_id())  
                    continue  
  
                real.bind(asset)  
                result = resolver.resolve(asset)  
  
                if result.get("resolved"):  
                    report["resolved"].append(item.get_id())  
                else:  
                    report["unresolved"].append(item.get_id())  
  
    # ------------------------------------------------------------------  
    # File Helpers  
    # ------------------------------------------------------------------  
  
    def _read_records(self, drop_in_path):  
        """Read a drop-in file into a list of records."""  
  
        path = Path(drop_in_path)  
  
        if not path.exists():  
            Logger.error(f"Drop-in file not found: {path}")  
            return []  
  
        try:  
            with open(path, "r", encoding="utf-8") as file:  
                data = json.load(file)  
        except (json.JSONDecodeError, OSError) as error:  
            Logger.error(f"Could not read drop-in file {path}: {error}")  
            return []  
  
        if isinstance(data, dict):  
            return [data]  
  
        if isinstance(data, list):  
            return data  
  
        Logger.error(  
            f"Drop-in file {path} must be a JSON object or array."  
        )  
        return []  
  
    def _read_media_json(self):  
        """Read the current media.json as a list (empty if missing/bad)."""  
  
        if not self.media_json.exists():  
            return []  
  
        try:  
            with open(self.media_json, "r", encoding="utf-8") as file:  
                data = json.load(file)  
        except (json.JSONDecodeError, OSError) as error:  
            Logger.error(f"Could not read {self.media_json}: {error}")  
            return []  
  
        return data if isinstance(data, list) else []  
  
    def _write_media_json(self, records):  
        """Write the merged media list back to media.json."""  
  
        self.metadata_path.mkdir(parents=True, exist_ok=True)  
  
        with open(self.media_json, "w", encoding="utf-8") as file:  
            json.dump(records, file, indent=4)