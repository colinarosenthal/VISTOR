"""  
VISTOR Library Reconciler  
  
Reconciles the physical Media/ tree against the catalogued MetadataLibrary.  
Merges the former MediaScanner (disk walk), MediaVerifier (asset-exists  
check + filename normalization), and MediaValidator (integrity + dangling-  
asset resolution) into one janitor service. This is NOT part of the ingest  
path; it is a maintenance pass for the marathon / re-download use case.  
"""  
  
import re  
from pathlib import Path  
  
from core.logger import Logger  
from core.paths import Paths  
from metadata.services.metadata_library import MetadataLibrary  
  
  
MEDIA_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".m4v", ".webm", ".ts"}  
  
  
def normalize_filename(filename):  
    """Normalize a filename to a safe, lowercase, underscore-collapsed form."""  
    name = filename.strip().lower()  
    if "." in name:  
        stem, _, extension = name.rpartition(".")  
        extension = "." + extension  
    else:  
        stem, extension = name, ""  
    stem = re.sub(r"[^a-z0-9]+", "_", stem).strip("_")  
    return f"{stem}{extension}"  
  
  
class LibraryReconciler:  
    """Disk-vs-catalog reconciliation: scan, verify, validate, resolve."""  
  
    def __init__(self, library: MetadataLibrary, media_root=None):  
        self.library = library  
        self.media_root = (  
            Path(media_root) if media_root else Paths().get_media_directory()  
        )  
  
    # ------------------------------------------------------------------  
    # Scan: what is physically on disk  
    # ------------------------------------------------------------------  
    def scan(self):  
        files = []  
        if not self.media_root.exists():  
            Logger.error(f"Media root does not exist: {self.media_root}")  
            return {"media_root": str(self.media_root), "total_files": 0, "files": []}  
  
        for path in sorted(self.media_root.rglob("*")):  
            if not path.is_file() or path.suffix.lower() not in MEDIA_EXTENSIONS:  
                continue  
            files.append(  
                {  
                    "path": str(path),  
                    "relative_path": str(path.relative_to(self.media_root)),  
                    "extension": path.suffix.lower(),  
                    "size_bytes": path.stat().st_size,  
                }  
            )  
        Logger.info(f"Scan: {len(files)} file(s) under {self.media_root}.")  
        return {"media_root": str(self.media_root), "total_files": len(files), "files": files}  
  
    # ------------------------------------------------------------------  
    # Verify: do catalogued assets exist on disk  
    # ------------------------------------------------------------------  
    def verify(self):  
        report = {"total_media": 0, "total_assets": 0, "verified": [], "missing": []}  
        media_items = self.library.get_media()  
        report["total_media"] = len(media_items)  
  
        for item in media_items:  
            for asset in item.get_media_assets():  
                report["total_assets"] += 1  
                if asset.exists():  
                    asset.set_verified(True)  
                    report["verified"].append(asset.get_asset_id())  
                else:  
                    asset.set_verified(False)  
                    report["missing"].append(  
                        (item.get_id(), asset.get_asset_id(), str(asset.get_path()))  
                    )  
                    Logger.warning(  
                        f"Missing asset {asset.get_asset_id()} for "  
                        f"'{item.get_title()}' ({item.get_id()})."  
                    )  
        return report  
  
    # ------------------------------------------------------------------  
    # Validate: integrity of catalogued items  
    # ------------------------------------------------------------------  
    def validate(self):  
        report = {  
            "total_media": 0, "valid": [], "issues": [],  
            "media_without_assets": [], "missing_assets": [],  
        }  
        media_items = self.library.get_media()  
        report["total_media"] = len(media_items)  
  
        for item in media_items:  
            media_id = item.get_id()  
            ok = True  
            if not media_id:  
                report["issues"].append((media_id, "missing id")); ok = False  
            if not item.get_title():  
                report["issues"].append((media_id, "missing title")); ok = False  
  
            assets = item.get_media_assets()  
            if not assets:  
                report["media_without_assets"].append(media_id); ok = False  
            for asset in assets:  
                if not asset.exists():  
                    report["missing_assets"].append(  
                        (media_id, asset.get_asset_id(), str(asset.get_path()))  
                    )  
                    ok = False  
            if ok:  
                report["valid"].append(media_id)  
        return report  
  
    # ------------------------------------------------------------------  
    # Resolve: drop or flag dangling assets  
    # ------------------------------------------------------------------  
    def resolve_missing_assets(self, strategy="flag"):  
        """strategy='flag' keeps the asset (default: metadata survives for  
        re-download, matching Deleted-Content Metadata Retention);  
        'drop' removes the dangling MediaAsset entirely."""  
        report = {"dropped": [], "flagged": []}  
        for item in self.library.get_media():  
            media_id = item.get_id()  
            surviving = []  
            for asset in item.get_media_assets():  
                if asset.exists():  
                    surviving.append(asset); continue  
                record = (media_id, asset.get_asset_id(), str(asset.get_path()))  
                if strategy == "drop":  
                    report["dropped"].append(record)  
                else:  
                    asset.set_verified(False)  
                    surviving.append(asset)  
                    report["flagged"].append(record)  
            item.media_assets = surviving  
        Logger.info(  
            f"Resolve (strategy='{strategy}'): "  
            f"{len(report['dropped'])} dropped, {len(report['flagged'])} flagged."  
        )  
        return report