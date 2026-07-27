"""  
VISTOR Media Associator  
  
Associates physical media files with metadata items using a  
manifest that maps each media item's identifier to one or more  
filenames located under the Media directory.  
  
This keeps physical filenames free-form: rather than requiring  
each file to be named after its metadata id, the manifest records  
the mapping explicitly.  
"""  
  
import json  
  
from pathlib import Path  
  
from core.logger import Logger  
from metadata.relationships.media_asset import MediaAsset  
from metadata.services.metadata_library import MetadataLibrary  
  
  
class MediaAssociator:  
    """  
    Associates media files with metadata items via a manifest.  
  
    The manifest is a JSON object mapping a media item's id to a  
    single filename (string) or a list of filenames. Each filename  
    is interpreted relative to the media directory. For every entry  
    that matches a media item in the library, a MediaAsset is  
    constructed and attached to that item.  
    """  
  
    def __init__(  
        self,  
        library: MetadataLibrary,  
        media_directory: Path,  
    ):  
        self.library = library  
  
        self.media_directory = Path(media_directory)  
  
    # ------------------------------------------------------------------  
    # Association  
    # ------------------------------------------------------------------  
  
    def associate_from_manifest(self, manifest_path):  
        """  
        Read the manifest and attach a MediaAsset to each matching item.  
  
        Returns a report dictionary:  
            {  
                "associated": [(media_id, asset_id, path), ...],  
                "unmatched_ids": [manifest_id, ...],  
                "missing_files": [(media_id, path), ...],  
            }  
        """  
  
        report = {  
            "associated": [],  
            "unmatched_ids": [],  
            "missing_files": [],  
        }  
  
        manifest = self._read_manifest(manifest_path)  
  
        if manifest is None:  
            return report  
  
        # Index media items by id for direct lookup.  
        items_by_id = {  
            item.get_id(): item  
            for item in self.library.get_media()  
        }  
  
        for media_id, filenames in manifest.items():  
  
            item = items_by_id.get(media_id)  
  
            if item is None:  
  
                report["unmatched_ids"].append(media_id)  
  
                Logger.warning(  
                    f"Manifest id '{media_id}' has no matching "  
                    f"media item; skipping."  
                )  
  
                continue  
  
            # Normalize a single filename to a list.  
            if isinstance(filenames, str):  
                filenames = [filenames]  
  
            for index, filename in enumerate(filenames):  
  
                path = self.media_directory / filename  
  
                asset_id = f"{media_id}-asset-{index + 1}"  
  
                asset = MediaAsset(  
                    asset_id=asset_id,  
                    path=path,  
                )  
  
                item.add_media_asset(asset)  
  
                report["associated"].append(  
                    (media_id, asset_id, str(path))  
                )  
  
                if not path.exists():  
  
                    report["missing_files"].append(  
                        (media_id, str(path))  
                    )  
  
                    Logger.warning(  
                        f"Associated asset {asset_id} for "  
                        f"'{item.get_title()}' points to a missing "  
                        f"file: {path}"  
                    )  
  
        self._log_summary(report)  
  
        return report  
  
    # ------------------------------------------------------------------  
    # Manifest reading  
    # ------------------------------------------------------------------  
  
    def _read_manifest(self, manifest_path):  
        """Read and parse the manifest, tolerating missing/bad files."""  
  
        path = Path(manifest_path)  
  
        if not path.exists():  
  
            Logger.warning(  
                f"Asset manifest not found: {path}"  
            )  
  
            return None  
  
        try:  
  
            with open(path, "r", encoding="utf-8") as file:  
  
                data = json.load(file)  
  
        except (json.JSONDecodeError, OSError) as error:  
  
            Logger.error(  
                f"Failed to read asset manifest {path}: {error}"  
            )  
  
            return None  
  
        if not isinstance(data, dict):  
  
            Logger.error(  
                f"Asset manifest {path} must be a JSON object "  
                f"mapping media ids to filenames."  
            )  
  
            return None  
  
        return data  
  
    # ------------------------------------------------------------------  
    # Reporting  
    # ------------------------------------------------------------------  
  
    def _log_summary(self, report):  
        """Log a human-readable summary of the association run."""  
  
        Logger.info(  
            f"Media association complete: "  
            f"{len(report['associated'])} asset(s) attached, "  
            f"{len(report['unmatched_ids'])} unmatched id(s), "  
            f"{len(report['missing_files'])} missing file(s)."  
        )  
  
        if not report["associated"]:  
  
            Logger.warning(  
                "No assets were associated. Check the manifest ids "  
                "against the metadata library."  
            )  
  
        elif not report["missing_files"]:  
  
            Logger.success(  
                f"All {len(report['associated'])} associated asset(s) "  
                f"exist on disk."  
            )