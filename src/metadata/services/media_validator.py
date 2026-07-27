"""  
VISTOR Media Validator  
  
Validates the integrity of a populated MetadataLibrary and resolves  
media items whose physical assets are missing from disk.  
  
Validation checks that every media item is well-formed (has an id and  
title), that it has at least one attached MediaAsset, and that each  
asset's file exists on disk. Resolution consumes the missing-asset  
findings and either drops the dangling MediaAsset references or leaves  
them flagged for manual repair.  
"""  
  
from core.logger import Logger  
from metadata.services.metadata_library import MetadataLibrary  
  
  
class MediaValidator:  
    """  
    Validates media items in a MetadataLibrary and resolves missing assets.  
    """  
  
    def __init__(self, library: MetadataLibrary):  
        self.library = library  
  
    # ------------------------------------------------------------------  
    # Validation  
    # ------------------------------------------------------------------  
  
    def validate(self):  
        """  
        Validate every media item in the library.  
  
        Returns a report dictionary:  
            {  
                "total_media": int,  
                "valid": [media_id, ...],  
                "issues": [(media_id, issue), ...],  
                "media_without_assets": [media_id, ...],  
                "missing_assets": [(media_id, asset_id, path), ...],  
            }  
        """  
  
        report = {  
            "total_media": 0,  
            "valid": [],  
            "issues": [],  
            "media_without_assets": [],  
            "missing_assets": [],  
        }  
  
        media_items = self.library.get_media()  
  
        report["total_media"] = len(media_items)  
  
        for item in media_items:  
  
            media_id = item.get_id()  
  
            item_ok = True  
  
            # Core fields must be present.  
            if not media_id:  
                report["issues"].append((media_id, "missing id"))  
                item_ok = False  
  
            if not item.get_title():  
                report["issues"].append((media_id, "missing title"))  
                item_ok = False  
  
            assets = item.get_media_assets()  
  
            # Every media item should have at least one physical asset.  
            if not assets:  
                report["media_without_assets"].append(media_id)  
                Logger.warning(  
                    f"Media item '{item.get_title()}' ({media_id}) "  
                    f"has no attached media assets."  
                )  
                item_ok = False  
  
            # Each attached asset must point at a real file.  
            for asset in assets:  
                if not asset.exists():  
                    report["missing_assets"].append(  
                        (  
                            media_id,  
                            asset.get_asset_id(),  
                            str(asset.get_path()),  
                        )  
                    )  
                    item_ok = False  
  
            if item_ok:  
                report["valid"].append(media_id)  
  
        self._log_validation_summary(report)  
  
        return report  
  
    # ------------------------------------------------------------------  
    # Resolution  
    # ------------------------------------------------------------------  
  
    def resolve_missing_assets(self, strategy="drop"):  
        """  
        Resolve media assets whose files are missing from disk.  
  
        strategy:  
            "drop"  - remove the dangling MediaAsset from its media item  
            "flag"  - keep the asset but mark it unverified and log it  
  
        Returns a report dictionary:  
            {  
                "dropped": [(media_id, asset_id, path), ...],  
                "flagged": [(media_id, asset_id, path), ...],  
            }  
        """  
  
        report = {  
            "dropped": [],  
            "flagged": [],  
        }  
  
        for item in self.library.get_media():  
  
            media_id = item.get_id()  
  
            surviving_assets = []  
  
            for asset in item.get_media_assets():  
  
                if asset.exists():  
                    surviving_assets.append(asset)  
                    continue  
  
                record = (  
                    media_id,  
                    asset.get_asset_id(),  
                    str(asset.get_path()),  
                )  
  
                if strategy == "drop":  
                    report["dropped"].append(record)  
                    Logger.warning(  
                        f"Dropping missing asset {asset.get_asset_id()} "  
                        f"from '{item.get_title()}' ({media_id}): "  
                        f"{asset.get_path()}"  
                    )  
                else:  
                    asset.set_verified(False)  
                    surviving_assets.append(asset)  
                    report["flagged"].append(record)  
                    Logger.warning(  
                        f"Flagging missing asset {asset.get_asset_id()} "  
                        f"on '{item.get_title()}' ({media_id}): "  
                        f"{asset.get_path()}"  
                    )  
  
            # Replace the asset list in place.  
            item.media_assets = surviving_assets  
  
        self._log_resolution_summary(report, strategy)  
  
        return report  
  
    # ------------------------------------------------------------------  
    # Reporting  
    # ------------------------------------------------------------------  
  
    def _log_validation_summary(self, report):  
        """Log a human-readable summary of the validation run."""  
  
        valid_count = len(report["valid"])  
        issue_count = len(report["issues"])  
        no_asset_count = len(report["media_without_assets"])  
        missing_count = len(report["missing_assets"])  
  
        Logger.info(  
            f"Media validation complete: "  
            f"{report['total_media']} media items, "  
            f"{valid_count} valid."  
        )  
  
        if issue_count == 0 and no_asset_count == 0 and missing_count == 0:  
            Logger.success("All media items passed validation.")  
        else:  
            Logger.error(  
                f"Validation found problems: "  
                f"{issue_count} field issue(s), "  
                f"{no_asset_count} item(s) without assets, "  
                f"{missing_count} missing asset file(s)."  
            )  
  
    def _log_resolution_summary(self, report, strategy):  
        """Log a human-readable summary of the resolution run."""  
  
        dropped_count = len(report["dropped"])  
        flagged_count = len(report["flagged"])  
  
        Logger.info(  
            f"Missing-asset resolution complete (strategy='{strategy}'): "  
            f"{dropped_count} dropped, {flagged_count} flagged."  
        )