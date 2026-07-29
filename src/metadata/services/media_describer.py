"""  
VISTOR Media Describer  
  
Best-effort descriptive-metadata scraper. Given a (provider, reference),  
returns a dict of descriptive fields (title, release_year, description,  
runtime_minutes) harvested WITHOUT downloading the file.  
  
Only YouTube is supported for now (via yt-dlp's info-dict). Other providers  
return an empty dict, so the caller falls back to whatever the user typed.  
Everything is best-effort: a missing tool or network error never raises.  
"""  
  
from core.logger import Logger  
  
  
class MediaDescriber:  
    """Scrape descriptive metadata for a source, download-free."""  
  
    def describe(self, provider, reference):  
        if provider == "youtube":  
            return self._describe_youtube(reference)  
  
        Logger.info(  
            f"No describer for provider '{provider}'; "  
            f"descriptive fields must be supplied manually."  
        )  
        return {}  
  
    # ------------------------------------------------------------------  
    # YouTube  
    # ------------------------------------------------------------------  
  
    def _describe_youtube(self, reference):  
        try:  
            import yt_dlp  # optional dep, imported lazily  
        except ImportError:  
            Logger.warning("yt-dlp not installed; cannot scrape metadata.")  
            return {}  
  
        url = f"https://www.youtube.com/watch?v={reference}"  
        options = {"quiet": True, "no_warnings": True, "skip_download": True}  
  
        try:  
            with yt_dlp.YoutubeDL(options) as ydl:  
                info = ydl.extract_info(url, download=False)  
        except Exception as exc:  # noqa: BLE001 - never fail the caller  
            Logger.warning(f"Could not scrape YouTube metadata: {exc!r}.")  
            return {}  
  
        data = {}  
  
        if info.get("title"):  
            data["title"] = info["title"]  
  
        # upload_date is "YYYYMMDD"; release_year is the first 4 digits.  
        upload_date = info.get("upload_date") or ""  
        if len(upload_date) >= 4 and upload_date[:4].isdigit():  
            data["release_year"] = int(upload_date[:4])  
  
        if info.get("description"):  
            data["description"] = info["description"]  
  
        # duration is in seconds; MediaItem stores runtime in minutes.  
        if info.get("duration"):  
            data["runtime_minutes"] = max(1, round(info["duration"] / 60))  
  
        Logger.info(  
            f"Scraped YouTube metadata for '{reference}': "  
            f"{data.get('title', '?')} ({data.get('release_year', '?')})."  
        )  
        return data