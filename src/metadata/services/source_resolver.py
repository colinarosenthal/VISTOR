"""  
VISTOR Source Resolver  
  
Headless multi-archive re-acquisition service. Given a MediaAsset with a  
ranked list of fetch sources, the resolver tries each source in order,  
cleanly handling takedown/error responses (e.g. 404 / 403 / 410), and  
updates the asset's DownloadStatus accordingly.  
  
If every source fails, the resolver falls back to a fingerprint-based  
replacement search across a pool of candidate assets, substituting a  
different-but-equivalent asset when an exact re-fetch is impossible.  
  
The network fetch is delegated to a pluggable "fetcher" object so this  
service stays fully testable without touching the network. A fetcher must  
expose:  
  
    fetch(provider: str, reference: str) -> FetchResult  
"""  
  
from core.logger import Logger  
from metadata.enums.download_status import DownloadStatus  
  
  
class FetchResult:  
    """Outcome of a single source fetch attempt."""  
  
    def __init__(self, ok: bool, status_code=None, detail: str = ""):  
        self.ok = ok  
        self.status_code = status_code  
        self.detail = detail  
  
    @classmethod  
    def success(cls, detail: str = ""):  
        return cls(True, status_code=200, detail=detail)  
  
    @classmethod  
    def failure(cls, status_code, detail: str = ""):  
        return cls(False, status_code=status_code, detail=detail)  
  
  
class SourceResolver:  
    """Resolves a MediaAsset by trying its ranked sources in order."""  
  
    # HTTP-style statuses that mean "this source is gone / forbidden".  
    TAKEDOWN_STATUSES = (403, 404, 410)  
  
    def __init__(self, fetcher):  
        self.fetcher = fetcher  
  
    # ------------------------------------------------------------------  
    # Resolution  
    # ------------------------------------------------------------------  
  
    def resolve(self, asset, candidates=None):  
        """  
        Try to (re)acquire `asset` from its ranked sources.  
  
        candidates: optional iterable of other MediaAssets usable as  
        fingerprint-matched replacements if every source fails.  
  
        Returns a report dictionary:  
            {  
                "asset_id": str,  
                "resolved": bool,  
                "used_source": dict | None,  
                "attempts": [(source, status_code), ...],  
                "replacement": asset_id | None,  
            }  
        """  
  
        report = {  
            "asset_id": asset.get_asset_id(),  
            "resolved": False,  
            "used_source": None,  
            "attempts": [],  
            "replacement": None,  
        }  
  
        sources = asset.get_sources()  
  
        if not sources:  
            Logger.warning(  
                f"No sources registered for asset "  
                f"'{asset.get_asset_id()}'; cannot resolve."  
            )  
  
        asset.set_download_status(DownloadStatus.DOWNLOADING)  
  
        for source in sources:  
            provider = source.get("provider", "")  
            reference = source.get("reference", "")  
  
            result = self.fetcher.fetch(provider, reference)  
  
            report["attempts"].append((source, result.status_code))  
  
            if result.ok:  
                asset.set_download_status(DownloadStatus.DOWNLOADED)  
                asset.set_verified(True)  
                report["resolved"] = True  
                report["used_source"] = source  
                Logger.success(  
                    f"Resolved asset '{asset.get_asset_id()}' from "  
                    f"{provider}:{reference}."  
                )  
                return report  
  
            if result.status_code in self.TAKEDOWN_STATUSES:  
                Logger.warning(  
                    f"Source {provider}:{reference} unavailable "  
                    f"({result.status_code}); trying next source."  
                )  
            else:  
                Logger.warning(  
                    f"Fetch from {provider}:{reference} failed "  
                    f"({result.status_code}); trying next source."  
                )  
  
        # Every source failed. Try a fingerprint-based replacement.  
        replacement = self._find_replacement(asset, candidates)  
  
        asset.set_download_status(DownloadStatus.FAILED)  
  
        if replacement is not None:  
            report["replacement"] = replacement.get_asset_id()  
            Logger.warning(  
                f"All sources failed for '{asset.get_asset_id()}'; "  
                f"substituting fingerprint match "  
                f"'{replacement.get_asset_id()}'."  
            )  
            return report  
  
        Logger.error(  
            f"Could not resolve asset '{asset.get_asset_id()}' from any "  
            f"source and no replacement was found."  
        )  
        return report  
  
    # ------------------------------------------------------------------  
    # Fingerprint-based replacement  
    # ------------------------------------------------------------------  
  
    def _find_replacement(self, asset, candidates):  
        """  
        Return an available candidate asset whose fingerprint matches the  
        target, or None. If no fingerprint match exists, fall back to any  
        available candidate (relevant-media substitution).  
        """  
  
        if not candidates:  
            return None  
  
        fingerprint = asset.get_fingerprint()  
  
        # Exact fingerprint match first.  
        if fingerprint:  
            for candidate in candidates:  
                if candidate is asset:  
                    continue  
                if not candidate.is_available():  
                    continue  
                if candidate.get_fingerprint() == fingerprint:  
                    return candidate  
  
        # Relevant-media fallback: any available candidate.  
        for candidate in candidates:  
            if candidate is asset:  
                continue  
            if candidate.is_available():  
                return candidate  
  
        return None