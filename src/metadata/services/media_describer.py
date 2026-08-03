"""  
VISTOR Media Describer  
  
Best-effort descriptive-metadata scraper. Given a (provider, reference),  
returns a dict of descriptive fields (title, release_year, description,  
runtime_minutes, poster_url) harvested WITHOUT downloading the file.  
  
Only YouTube is supported for now (via yt-dlp's info-dict). Other providers  
return an empty dict, so the caller falls back to whatever the user typed.  
Everything is best-effort: a missing tool or network error never raises.  
"""  
  
import re  
  
from core.logger import Logger  
  
# A line is promo boilerplate if it contains a URL (subscribe / "WATCH ... ►"  
# / social links all do). Hashtag runs are stripped wherever they appear.  
_URL_RE = re.compile(r"https?://\S+|\bwww\.\S+", re.IGNORECASE)  
_HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")  
  
# Orphan promo headers whose URL sat on a following line (so the URL filter  
# alone would leave the header behind).  
_PROMO_PREFIXES = (  
    "watch ",  
    "subscribe",  
    "stream and download",  
    "follow ",  
    "official website",  
    "listen ",  
    "download ",  
)  
  
# If the description has an explicit lyrics marker, keep only what follows it.  
_LYRICS_MARKER_RE = re.compile(r"^\s*lyrics\s*:?\s*$", re.IGNORECASE)  
  
  
def _clean_youtube_description(text):  
    """Strip promo boilerplate (URLs, WATCH/Subscribe/Follow lines, hashtags)  
    and, when present, keep only the text after a 'Lyrics:' marker. Newlines  
    in the original are preserved so lyrics stay line-broken."""  
    if not text:  
        return ""  
  
    lines = text.splitlines()  
  
    # If there's a "Lyrics:" line, everything above it is promo/credits noise.  
    for i, raw in enumerate(lines):  
        if _LYRICS_MARKER_RE.match(raw):  
            lines = lines[i + 1:]  
            break  
  
    kept = []  
    for raw in lines:  
        line = _HASHTAG_RE.sub("", raw).rstrip()  
        stripped = line.strip()  
  
        # Drop any line carrying a URL (subscribe / WATCH ► / social / promo).  
        if _URL_RE.search(stripped):  
            continue  
  
        low = stripped.lower()  
  
        # Drop orphaned promo headers (their URL was on a now-removed line).  
        if low.endswith("here:") or low.startswith(_PROMO_PREFIXES):  
            continue  
  
        kept.append(line)  
  
    # Collapse 3+ blank lines to a single blank line and trim the edges.  
    cleaned = "\n".join(kept)  
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()  
    return cleaned  
  
  
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
  
        # Clean promo boilerplate out of the scraped description; keep lyrics.  
        if info.get("description"):  
            cleaned = _clean_youtube_description(info["description"])  
            if cleaned:  
                data["description"] = cleaned  
  
        # duration is in seconds; MediaItem stores runtime in minutes.  
        if info.get("duration"):  
            data["runtime_minutes"] = max(1, round(info["duration"] / 60))  
  
        # Thumbnail -> poster_url for the preview cover. yt-dlp exposes a single  
        # best "thumbnail" plus a "thumbnails" list; prefer the explicit one and  
        # fall back to the highest-preference entry in the list.  
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
  
        Logger.info(  
            f"Scraped YouTube metadata for '{reference}': "  
            f"{data.get('title', '?')} ({data.get('release_year', '?')})."  
        )  
        return data