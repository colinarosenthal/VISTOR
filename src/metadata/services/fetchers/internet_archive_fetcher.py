"""  
VISTOR Internet Archive Fetcher  
  
reference format: "<identifier>/<filename>"  
    e.g. "entiretyofeva/endofevaalldub.mkv"  
  
Builds https://archive.org/download/<identifier>/<filename> and streams  
it to disk, logging download progress so long transfers are visibly  
in-progress rather than appearing frozen. Most-reliable provider, so it  
is ranked first.  
"""  
  
import time  
  
from core.logger import Logger  
from metadata.services.fetchers.base_fetcher import BaseFetcher  
  
  
class InternetArchiveFetcher(BaseFetcher):  
  
    BASE = "https://archive.org/download"  
  
    # Emit at most one progress line every this many seconds.  
    _PROGRESS_INTERVAL_SECONDS = 2.0  
  
    def _download(self, reference, temp_path):  
        import requests  # optional dep, imported lazily  
  
        url = f"{self.BASE}/{reference.lstrip('/')}"  
  
        with requests.get(url, stream=True, timeout=30) as resp:  
            if resp.status_code != 200:  
                return resp.status_code  
  
            total = int(resp.headers.get("Content-Length") or 0)  
            downloaded = 0  
            last_log = 0.0  
  
            Logger.info(  
                f"Downloading internet_archive:{reference} "  
                f"({self._format_size(total) if total else 'unknown size'})."  
            )  
  
            with open(temp_path, "wb") as handle:  
                for chunk in resp.iter_content(chunk_size=1 << 16):  
                    if not chunk:  
                        continue  
  
                    handle.write(chunk)  
                    downloaded += len(chunk)  
  
                    now = time.monotonic()  
                    if now - last_log >= self._PROGRESS_INTERVAL_SECONDS:  
                        last_log = now  
                        self._log_progress(reference, downloaded, total)  
  
            # Final line so the last percentage/size is always shown.  
            self._log_progress(reference, downloaded, total)  
  
        return 200  
  
    # ------------------------------------------------------------------  
    # Progress helpers  
    # ------------------------------------------------------------------  
  
    def _log_progress(self, reference, downloaded, total):  
        if total:  
            pct = downloaded / total * 100  
            Logger.info(  
                f"  internet_archive:{reference} "  
                f"{self._format_size(downloaded)} / "  
                f"{self._format_size(total)} ({pct:.1f}%)."  
            )  
        else:  
            Logger.info(  
                f"  internet_archive:{reference} "  
                f"{self._format_size(downloaded)} downloaded."  
            )  
  
    @staticmethod  
    def _format_size(num_bytes):  
        size = float(num_bytes)  
        for unit in ("B", "KB", "MB", "GB", "TB"):  
            if size < 1024 or unit == "TB":  
                return f"{size:.1f} {unit}"  
            size /= 1024