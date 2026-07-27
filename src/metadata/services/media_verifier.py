"""  
VISTOR Media Verifier  
  
Verifies that the physical media files referenced by the metadata  
library actually exist on disk, updates each asset's verification  
status, and provides a filename normalization helper for organizing  
incoming media.  
"""  
  
import re  
import unicodedata  
  
from pathlib import Path  
  
from core.logger import Logger  
from metadata.services.metadata_library import MetadataLibrary  
  
  
# ----------------------------------------------------------------------  
# Filename Normalization  
# ----------------------------------------------------------------------  
  
def normalize_filename(filename):  
    """  
    Normalize a filename to a safe, lowercase form.  
  
    - Strips surrounding whitespace  
    - Lowercases the stem and extension  
    - Collapses any run of non-alphanumeric characters into a single underscore  
    - Strips leading/trailing underscores from the stem so trailing  
      punctuation before the extension does not leave a dangling underscore  
    """  
    name = filename.strip().lower()  
  
    if "." in name:  
        stem, _, extension = name.rpartition(".")  
        extension = "." + extension  
    else:  
        stem, extension = name, ""  
  
    stem = re.sub(r"[^a-z0-9]+", "_", stem).strip("_")  
  
    return f"{stem}{extension}"  
  
# ----------------------------------------------------------------------  
# Media Verifier  
# ----------------------------------------------------------------------  
  
class MediaVerifier:  
    """  
    Verifies physical media assets referenced by a MetadataLibrary.  
  
    For each media item's assets, checks whether the file exists on  
    disk, updates the asset's verified flag, and produces a report of  
    verified, missing, and previously-unverified assets.  
    """  
  
    def __init__(self, library: MetadataLibrary):  
        self.library = library  
  
    # ------------------------------------------------------------------  
    # Verification  
    # ------------------------------------------------------------------  
  
    def verify(self):  
        """  
        Walk every media item and verify its assets.  
  
        Returns a report dictionary:  
            {  
                "total_media": int,  
                "total_assets": int,  
                "verified": [asset_id, ...],  
                "missing": [(media_id, asset_id, path), ...],  
            }  
        """  
  
        report = {  
            "total_media": 0,  
            "total_assets": 0,  
            "verified": [],  
            "missing": [],  
        }  
  
        media_items = self.library.get_media()  
  
        report["total_media"] = len(media_items)  
  
        for item in media_items:  
  
            assets = item.get_media_assets()  
  
            for asset in assets:  
  
                report["total_assets"] += 1  
  
                if asset.exists():  
  
                    asset.set_verified(True)  
  
                    report["verified"].append(asset.get_asset_id())  
  
                else:  
  
                    asset.set_verified(False)  
  
                    report["missing"].append(  
                        (  
                            item.get_id(),  
                            asset.get_asset_id(),  
                            str(asset.get_path()),  
                        )  
                    )  
  
                    Logger.warning(  
                        f"Missing media asset "  
                        f"{asset.get_asset_id()} "  
                        f"for '{item.get_title()}' "  
                        f"({item.get_id()}): "  
                        f"{asset.get_path()}"  
                    )  
  
        self._log_summary(report)  
  
        return report  
  
    # ------------------------------------------------------------------  
    # Reporting  
    # ------------------------------------------------------------------  
  
    def _log_summary(self, report):  
        """Log a human-readable summary of the verification run."""  
  
        verified_count = len(report["verified"])  
        missing_count = len(report["missing"])  
  
        Logger.info(  
            f"Media verification complete: "  
            f"{report['total_media']} media items, "  
            f"{report['total_assets']} assets."  
        )  
  
        if missing_count == 0:  
  
            Logger.success(  
                f"All {verified_count} media assets verified."  
            )  
  
        else:  
  
            Logger.error(  
                f"{missing_count} media asset(s) missing; "  
                f"{verified_count} verified."  
            )