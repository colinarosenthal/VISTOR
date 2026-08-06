"""  
VISTOR Asset Sidecar  
  
A sidecar is a small JSON file written next to every downloaded media file  
(<asset path>.vistor.json). It carries the complete media.json record for the  
item that owns the file, so:  
  
  * if the media file is evicted or deleted out-of-band, its metadata,  
    ranked sources, and fingerprint survive ON DISK and can drive a  
    re-download without the central catalog; and  
  * a marathon / re-catalogue tool can rebuild media.json by scanning the  
    Media tree for sidecars.  
  
The sidecar mirrors the exact record MediaIngestor writes to media.json, so  
there is no second serialization format to keep in sync.  
"""  
  
import json  
from pathlib import Path  
  
from core.logger import Logger  
  
SIDECAR_SUFFIX = ".vistor.json"  
SCHEMA_VERSION = 1  
  
  
class AssetSidecar:  
    """Reads/writes per-file metadata sidecars next to media files."""  
  
    @staticmethod  
    def sidecar_path(asset_path):  
        """Return the sidecar path for a given media file path."""  
        return Path(str(asset_path) + SIDECAR_SUFFIX)  
  
    @classmethod  
    def write(cls, record):  
        """  
        Write one sidecar next to every asset in `record` that has a real  
        on-disk path. A sidecar is written regardless of download_status so  
        the metadata is present even after the file is later evicted.  
  
        `record` is a media.json-shaped dict (as produced by the serializer).  
        """  
        written = []  
        for asset in record.get("assets", []):  
            raw_path = asset.get("path")  
            if not raw_path:  
                continue  
  
            sidecar = cls.sidecar_path(Path(raw_path))  
            payload = {"schema_version": SCHEMA_VERSION, "record": record}  
  
            try:  
                sidecar.parent.mkdir(parents=True, exist_ok=True)  
                with open(sidecar, "w", encoding="utf-8") as handle:  
                    json.dump(payload, handle, indent=4)  
                written.append(str(sidecar))  
            except OSError as exc:  # never fail the ingest over a sidecar  
                Logger.warning(f"Could not write sidecar {sidecar}: {exc!r}.")  
  
        if written:  
            Logger.info(  
                f"Wrote {len(written)} sidecar(s) for "  
                f"'{record.get('id', '?')}'."  
            )  
        return written  
  
    @classmethod  
    def read(cls, sidecar_path):  
        """Load a sidecar; return the record dict or None on any failure."""  
        try:  
            with open(sidecar_path, "r", encoding="utf-8") as handle:  
                payload = json.load(handle) or {}  
        except (OSError, ValueError) as exc:  
            Logger.warning(f"Could not read sidecar {sidecar_path}: {exc!r}.")  
            return None  
        return payload.get("record")  
  
    @classmethod  
    def scan(cls, media_root):  
        """  
        Walk `media_root` and return every recoverable record from sidecars,  
        deduped by record id (last one wins). Used to rebuild media.json if  
        the central catalog is lost.  
        """  
        media_root = Path(media_root)  
        if not media_root.exists():  
            return []  
  
        records = {}  
        for path in sorted(media_root.rglob("*" + SIDECAR_SUFFIX)):  
            record = cls.read(path)  
            if record and record.get("id"):  
                records[record["id"]] = record  
  
        Logger.info(  
            f"Recovered {len(records)} record(s) from sidecars under "  
            f"{media_root}."  
        )  
        return list(records.values())