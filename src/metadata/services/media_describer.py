"""  
VISTOR Media Describer  
  
Best-effort descriptive-metadata scraper. Given a (provider, reference),  
returns a dict of descriptive fields (title, release_year, description,  
runtime_minutes, poster_url) PLUS raw detection signals (categories, duration,  
tags, channel, mediatype, collection, subject) that MediaClassifier scores on.  
Harvested WITHOUT downloading the file.  
  
YouTube (via yt-dlp) and Internet Archive (via the archive.org metadata JSON  
API) are supported. Other providers return {}. Everything is best-effort: a  
missing tool or network error never raises.  
"""  
  
import re  
import time
  
from core.logger import Logger  
  
_URL_RE = re.compile(r"https?://\S+|\bwww\.\S+", re.IGNORECASE)  
_HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")  
_PROMO_PREFIXES = (  
    "watch ", "subscribe", "stream and download", "follow ",  
    "official website", "listen ", "download ",  
)  
_LYRICS_MARKER_RE = re.compile(r"^\s*lyrics\s*:?\s*$", re.IGNORECASE)  
_HTML_TAG_RE = re.compile(r"<[^>]+>")  
  
  
def _clean_youtube_description(text):  
    """Strip promo boilerplate and, when present, keep only text after a  
    'Lyrics:' marker. Newlines preserved so lyrics stay line-broken."""  
    if not text:  
        return ""  
  
    lines = text.splitlines()  
    for i, raw in enumerate(lines):  
        if _LYRICS_MARKER_RE.match(raw):  
            lines = lines[i + 1:]  
            break  
  
    kept = []  
    for raw in lines:  
        line = _HASHTAG_RE.sub("", raw).rstrip()  
        stripped = line.strip()  
        if _URL_RE.search(stripped):  
            continue  
        low = stripped.lower()  
        if low.endswith("here:") or low.startswith(_PROMO_PREFIXES):  
            continue  
        kept.append(line)  
  
    cleaned = "\n".join(kept)  
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()  
    return cleaned  
  
  
def _first(value):  
    if isinstance(value, list):  
        return value[0] if value else ""  
    return value  
  
  
def _as_list(value):  
    """Archive fields may be scalar or list; always return a list of strings."""  
    if value is None:  
        return []  
    if isinstance(value, list):  
        return [str(v) for v in value]  
    return [str(value)]  
  
  
class MediaDescriber:  
    """Scrape descriptive metadata + detection signals, download-free."""  
  
    def describe(self, provider, reference):  
        if provider == "youtube":  
            return self._describe_youtube(reference)  
        if provider == "internet_archive":  
            return self._describe_internet_archive(reference)  
  
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
        except Exception as exc:  # noqa: BLE001  
            Logger.warning(f"Could not scrape YouTube metadata: {exc!r}.")  
            return {}  
  
        data = {}  
  
        if info.get("title"):  
            data["title"] = info["title"]  
  
        upload_date = info.get("upload_date") or ""  
        if len(upload_date) >= 4 and upload_date[:4].isdigit():  
            data["release_year"] = int(upload_date[:4])  
  
        if info.get("description"):  
            cleaned = _clean_youtube_description(info["description"])  
            if cleaned:  
                data["description"] = cleaned  
  
        if info.get("duration"):  
            data["runtime_minutes"] = max(1, round(info["duration"] / 60))  
  
        poster = info.get("thumbnail") or ""  
        if not poster:  
            thumbs = info.get("thumbnails") or []  
            if thumbs:  
                best = sorted(  
                    thumbs, key=lambda t: t.get("preference", 0), reverse=True  
                )[0]  
                poster = best.get("url", "")  
        if poster:  
            data["poster_url"] = poster  
  
        # --- Detection signals for MediaClassifier --------------------  
        data["categories"] = info.get("categories") or []  
        data["tags"] = info.get("tags") or []  
        data["duration"] = info.get("duration") or 0  
        data["channel"] = info.get("channel") or info.get("uploader") or ""  
  
        Logger.info(  
            f"Scraped YouTube metadata for '{reference}': "  
            f"{data.get('title', '?')} ({data.get('release_year', '?')})."  
        )  
        return data  
  
    # ------------------------------------------------------------------  
    # Internet Archive  
    # ------------------------------------------------------------------  
  
    def _describe_internet_archive(self, reference):  
        """Pull descriptive fields + detection signals from the archive.org  
        metadata JSON API."""  
        import requests  # optional dep, imported lazily  
  
        identifier = reference.split("/", 1)[0]  
        url = f"https://archive.org/metadata/{identifier}"  
  
        meta = None  
        # (connect, read) timeout: fail fast on connect, allow a slow body.  
        for attempt in range(3):  
            try:  
                resp = requests.get(url, timeout=(5, 30))  
                resp.raise_for_status()  
                meta = (resp.json() or {}).get("metadata", {}) or {}  
                break  
            except Exception as exc:  # noqa: BLE001 - describe is best-effort  
                if attempt == 2:  
                    Logger.warning(  
                        f"Could not scrape Internet Archive metadata "  
                        f"after 3 attempts: {exc!r}."  
                    )  
                    return {}  
                Logger.info(  
                    f"Archive metadata attempt {attempt + 1} failed "  
                    f"({exc!r}); retrying."  
                )  
                time.sleep(1.5 * (attempt + 1))
  
        data = {}  
  
        title = _first(meta.get("title"))  
        if title:  
            data["title"] = str(title).strip()  
  
        date = str(_first(meta.get("year")) or _first(meta.get("date")) or "")  
        if len(date) >= 4 and date[:4].isdigit():  
            data["release_year"] = int(date[:4])  
  
        desc = meta.get("description")  
        if isinstance(desc, list):  
            desc = " ".join(str(d) for d in desc)  
        if desc:  
            desc = _HTML_TAG_RE.sub("", str(desc)).strip()  
            if desc:  
                data["description"] = desc  
  
        # Every archive.org item has a derived thumbnail at this stable URL.  
        # No extra request needed; it 302s to the item's poster/first frame.  
        data["poster_url"] = f"https://archive.org/services/img/{identifier}"  
  
        # --- Detection signals for MediaClassifier --------------------  
        data["mediatype"] = str(_first(meta.get("mediatype")) or "")  
        data["collection"] = _as_list(meta.get("collection"))  
        data["subject"] = _as_list(meta.get("subject"))  
        # Some archive items carry runtime as "HH:MM:SS" or seconds.  
        runtime = _first(meta.get("runtime")) or _first(meta.get("length"))  
        data["duration"] = self._archive_seconds(runtime)  
  
        Logger.info(  
            f"Scraped Internet Archive metadata for '{identifier}': "  
            f"{data.get('title', '?')} ({data.get('release_year', '?')}) "  
            f"[mediatype={data['mediatype']}]."  
        )  
        return data  
  
    @staticmethod  
    def _archive_seconds(value):  
        """Parse 'HH:MM:SS' / 'MM:SS' / '123.4' into integer seconds; 0 if none."""  
        if not value:  
            return 0  
        text = str(value).strip()  
        if ":" in text:  
            parts = text.split(":")  
            try:  
                nums = [float(p) for p in parts]  
            except ValueError:  
                return 0  
            seconds = 0.0  
            for n in nums:  
                seconds = seconds * 60 + n  
            return int(seconds)  
        try:  
            return int(float(text))  
        except ValueError:  
            return 0