"""  
VISTOR Internet Archive Fetcher  
  
reference format: "<identifier>/<filename>"  
    e.g. "entiretyofeva/endofevaalldub.mkv"  
  
A bare "<identifier>" (what LinkResolver returns for a /details/ URL) is  
also accepted: the largest playable file inside the item is resolved from  
the archive metadata API and appended before downloading.  
  
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
    METADATA_BASE = "https://archive.org/metadata"  
  
    # Emit at most one progress line every this many seconds.  
    _PROGRESS_INTERVAL_SECONDS = 2.0  
  
    # Playable extensions we consider when picking an item's primary file.  
    _MEDIA_EXTS = (  
        ".mkv", ".mp4", ".m4v", ".avi", ".mov", ".webm", ".ogv",  
        ".mpg", ".mpeg", ".flv", ".wmv",  
        ".mp3", ".m4a", ".flac", ".ogg", ".wav",  
    )  
  
    def _download(self, reference, temp_path):  
        import requests  # optional dep, imported lazily  
  
        reference = reference.lstrip("/")  
  
        # A /details/ drop resolves to a bare identifier with no filename.  
        # archive.org serves an HTML directory listing (200!) for that URL,  
        # so resolve the real primary file before downloading.  
        if "/" not in reference:  
            filename = self._resolve_primary_file(reference)  
            if not filename:  
                Logger.warning(  
                    f"internet_archive:{reference} exposes no playable file."  
                )  
                return 404  
            reference = f"{reference}/{filename}"  
  
        url = f"{self.BASE}/{reference}"  
  
        with requests.get(url, stream=True, timeout=30) as resp:  
            if resp.status_code != 200:  
                return resp.status_code  
  
            # Guard: never save an HTML page (e.g. a directory listing or an  
            # error page that returned 200) as a media file.  
            content_type = (resp.headers.get("Content-Type") or "").lower()  
            if "text/html" in content_type:  
                Logger.warning(  
                    f"internet_archive:{reference} returned HTML, not media "  
                    f"(Content-Type: {content_type or 'unknown'})."  
                )  
                return 404  
  
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
    # File resolution  
    # ------------------------------------------------------------------  
  
    def _resolve_primary_file(self, identifier):  
        """Return the largest playable file name inside an item, or ""."""  
        import requests  # optional dep, imported lazily  
  
        url = f"{self.METADATA_BASE}/{identifier}"  
        try:  
            resp = requests.get(url, timeout=10)  
            resp.raise_for_status()  
            files = (resp.json() or {}).get("files", []) or []  
        except Exception as exc:  # noqa: BLE001 - degrade to "no file"  
            Logger.warning(  
                f"Could not list archive files for '{identifier}': {exc!r}."  
            )  
            return ""  
  
        best_name, best_size = "", -1  
        for entry in files:  
            name = entry.get("name", "")  
            if not name.lower().endswith(self._MEDIA_EXTS):  
                continue  
            try:  
                size = int(entry.get("size") or 0)  
            except (TypeError, ValueError):  
                size = 0  
            if size > best_size:  
                best_name, best_size = name, size  
  
        return best_name  
  
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