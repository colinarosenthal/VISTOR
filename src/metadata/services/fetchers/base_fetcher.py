"""  
VISTOR Base Fetcher  
  
Shared download plumbing for all real fetchers: temp-download, verify,  
probe technical metadata, fingerprint, then atomically move into place.  
  
Subclasses implement `_download(reference, temp_path) -> int` which returns  
an HTTP-style status code (200 on success). Any exception or a status in  
TAKEDOWN_STATUSES makes the resolver advance to the next source.  
"""  
  
import shutil  
import tempfile  
from pathlib import Path  
  
from core.logger import Logger  

from metadata.services.source_resolver import FetchResult  
from metadata.services.fetchers.metadata_probe import MetadataProbe
from metadata.services.fetchers.breakpoint_detector import BreakpointDetector 
from metadata.services.keyframe_fingerprint import KeyframeFingerprintService  
  
# Same "gone/forbidden" codes SourceResolver understands.  
TAKEDOWN_STATUSES = (403, 404, 410)  
  
  
class BaseFetcher:  
    """Common download lifecycle for every provider-specific fetcher."""  
  
    def __init__(  
        self,  
        media_root=None,  
        probe=None,  
        fingerprint_service=None,  
    ):  
        from core.paths import Paths  
  
        self.media_root = (  
            Path(media_root) if media_root else Paths().get_media_directory()  
        )  
        self.temp_dir = self.media_root / "tmp"
        self.probe = probe or MetadataProbe()  
        self.fingerprint_service = (  
            fingerprint_service or KeyframeFingerprintService()  
        )  
        self.breakpoint_detector = BreakpointDetector()
        # Set by RealFetcher before each fetch so we can populate technical  
        # fields / fingerprint on the exact asset being resolved.  
        self.current_asset = None  
  
    # ------------------------------------------------------------------  
    # Contract  
    # ------------------------------------------------------------------  
  
    def fetch(self, provider, reference):  
        """Download `reference`, returning a FetchResult."""  
  
        self.temp_dir.mkdir(parents=True, exist_ok=True)  
  
        fd, temp_name = tempfile.mkstemp(dir=str(self.temp_dir))  
        temp_path = Path(temp_name)  
  
        try:  
            import os  
            os.close(fd)  
  
            status = self._download(reference, temp_path)  
  
            if status != 200:  
                temp_path.unlink(missing_ok=True)  
  
                if status in TAKEDOWN_STATUSES:  
                    Logger.warning(  
                        f"{provider}:{reference} unavailable ({status})."  
                    )  
                else:  
                    Logger.warning(  
                        f"{provider}:{reference} failed ({status})."  
                    )  
  
                return FetchResult.failure(status)  
  
            if not temp_path.exists() or temp_path.stat().st_size == 0:  
                temp_path.unlink(missing_ok=True)  
                return FetchResult.failure(0, "empty download")  
  
            self._finalize(temp_path)  
  
            Logger.success(  
                f"Downloaded {provider}:{reference} "  
                f"({temp_path.name} probed + fingerprinted)."  
            )  
            return FetchResult.success()  
  
        except Exception as exc:  # noqa: BLE001 - map everything to a failure  
            temp_path.unlink(missing_ok=True)  
            Logger.error(f"{provider}:{reference} raised {exc!r}.")  
            return FetchResult.failure(0, str(exc))  
  
    # ------------------------------------------------------------------  
    # Hooks  
    # ------------------------------------------------------------------  
  
    def _download(self, reference, temp_path):  
        """Download `reference` into temp_path. Return an HTTP-style code."""  
  
        raise NotImplementedError  
  
    def _finalize(self, temp_path):  
        """Probe metadata, fingerprint, and move the file to its final path."""  
  
        asset = self.current_asset  
  
        if asset is None:  
            return  
  
        # 1. Fill technical metadata (runtime, codecs, resolution, size...).  
        self.probe.populate(asset, temp_path)  
  
        # 2. Fingerprint BEFORE the file can ever be evicted.  
        self.fingerprint_service.ensure_fingerprint(asset)  
  
        # 3. Detect commercial-break offsets from chapters / black+silence  
        #    (best-effort; never fails the download).  
        try:  
            asset.set_breakpoints(  
                self.breakpoint_detector.detect(asset, temp_path)  
            )  
        except Exception as error:  # noqa: BLE001  
            Logger.warning(f"Breakpoint detection skipped: {error}.")  
  
        # 4. Move temp -> the asset's declared final path.  
        final_path = Path(asset.get_path())
        final_path.parent.mkdir(parents=True, exist_ok=True)  
        shutil.move(str(temp_path), str(final_path))