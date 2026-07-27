"""  
VISTOR Media Scanner  
  
Walks the physical Media directory and reports every media file  
found on disk. The scanner does not modify metadata; it produces a  
report that later stages use to associate files with metadata items.  
"""  
  
from pathlib import Path  
  
from core.logger import Logger  
from core.paths import Paths  
  
  
# Recognized playable media extensions (lowercase, with dot).  
MEDIA_EXTENSIONS = {  
    ".mp4",  
    ".mkv",  
    ".avi",  
    ".mov",  
    ".m4v",  
    ".webm",  
    ".ts",  
}  
  
  
class MediaScanner:  
    """Scans the physical media library for playable files."""  
  
    def __init__(self, media_root=None):  
        # Default to the project's Media directory via Paths.  
        self.media_root = Path(media_root) if media_root else Paths().get_media_directory()  
  
    # ------------------------------------------------------------------  
    # Scanning  
    # ------------------------------------------------------------------  
  
    def scan(self):  
        """  
        Recursively scan the media root for media files.  
  
        Returns a report dictionary:  
            {  
                "media_root": str,  
                "total_files": int,  
                "files": [  
                    {  
                        "path": str,  
                        "relative_path": str,  
                        "extension": str,  
                        "size_bytes": int,  
                    },  
                    ...  
                ],  
            }  
        """  
  
        report = {  
            "media_root": str(self.media_root),  
            "total_files": 0,  
            "files": [],  
        }  
  
        if not self.media_root.exists():  
            Logger.error(f"Media root does not exist: {self.media_root}")  
            return report  
  
        for path in sorted(self.media_root.rglob("*")):  
  
            if not path.is_file():  
                continue  
  
            if path.suffix.lower() not in MEDIA_EXTENSIONS:  
                continue  
  
            report["files"].append(  
                {  
                    "path": str(path),  
                    "relative_path": str(path.relative_to(self.media_root)),  
                    "extension": path.suffix.lower(),  
                    "size_bytes": path.stat().st_size,  
                }  
            )  
  
        report["total_files"] = len(report["files"])  
  
        self._log_summary(report)  
  
        return report  
  
    # ------------------------------------------------------------------  
    # Reporting  
    # ------------------------------------------------------------------  
  
    def _log_summary(self, report):  
        """Log a human-readable summary of the scan."""  
  
        Logger.info(  
            f"Media scan complete: {report['total_files']} "  
            f"file(s) found under {report['media_root']}."  
        )  
  
        if report["total_files"] == 0:  
            Logger.warning("No media files found. Library is empty.")