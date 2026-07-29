"""  
VISTOR YouTube Fetcher  
  
reference format: a YouTube video id, e.g. "fzHD04_OwyQ".  
  
Uses yt-dlp's Python API. "video unavailable / private / removed" errors  
map to takedown status 410 so the resolver advances to the next source.  
"""  
  
from pathlib import Path  
  
from metadata.services.fetchers.base_fetcher import BaseFetcher  
  
_TAKEDOWN_MARKERS = (  
    "video unavailable",  
    "private video",  
    "has been removed",  
    "account associated with this video has been terminated",  
    "video is not available",  
)  
  
  
class YouTubeFetcher(BaseFetcher):  
  
    def _download(self, reference, temp_path):  
        import yt_dlp  # optional dep, imported lazily  
  
        temp_path = Path(temp_path)  
        url = f"https://www.youtube.com/watch?v={reference}"  
  
        options = {  
            "format": "bv*+ba/b",  
            # yt-dlp appends the real container extension, so give it a  
            # template it can extend rather than the exact temp file.  
            "outtmpl": str(temp_path) + ".%(ext)s",  
            "merge_output_format": "mkv",  
            "quiet": True,  
            "no_warnings": True,  
            "overwrites": True,  
        }  
  
        try:  
            with yt_dlp.YoutubeDL(options) as ydl:  
                ydl.download([url])  
        except yt_dlp.utils.DownloadError as exc:  
            message = str(exc).lower()  
            if any(marker in message for marker in _TAKEDOWN_MARKERS):  
                return 410  
            return 0  
  
        # yt-dlp wrote "<temp_path>.<ext>" (e.g. .mkv after a merge). Move  
        # the produced file back onto the extensionless temp_path that  
        # BaseFetcher.fetch() verifies, probes, fingerprints, and moves.  
        produced = sorted(  
            temp_path.parent.glob(temp_path.name + ".*"),  
            key=lambda p: p.stat().st_size,  
            reverse=True,  
        )  
  
        if not produced:  
            return 0  
  
        produced[0].replace(temp_path)  
        return 200