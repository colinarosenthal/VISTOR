"""  
VISTOR YouTube Fetcher  
  
reference format: a YouTube video id, e.g. "fzHD04_OwyQ".  
  
Uses yt-dlp's Python API. "video unavailable / private / removed" errors  
map to takedown status 410 so the resolver advances to the next source.  
"""  
  
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
  
        url = f"https://www.youtube.com/watch?v={reference}"  
  
        options = {  
            "format": "bv*+ba/b",  
            "outtmpl": str(temp_path),  
            "quiet": True,  
            "no_warnings": True,  
            "overwrites": True,  
        }  
  
        try:  
            with yt_dlp.YoutubeDL(options) as ydl:  
                ydl.download([url])  
            return 200  
        except yt_dlp.utils.DownloadError as exc:  
            message = str(exc).lower()  
            if any(marker in message for marker in _TAKEDOWN_MARKERS):  
                return 410  
            return 0