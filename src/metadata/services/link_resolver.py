"""  
VISTOR Link Resolver  
  
Parses a pasted media URL into the (provider, reference) pair that the  
fetcher stack expects. This is the piece that lets a user paste a raw link  
instead of hand-authoring a source dict.  
  
    LinkResolver.resolve("https://youtu.be/fzHD04_OwyQ?si=abc")  
        -> ("youtube", "fzHD04_OwyQ")  
    LinkResolver.resolve("https://archive.org/download/eva/eva.mkv")  
        -> ("internet_archive", "eva/eva.mkv")  
    LinkResolver.resolve("https://example.com/clip.mp4")  
        -> ("http", "https://example.com/clip.mp4")  
"""  
  
from urllib.parse import urlparse, parse_qs  
  
  
class LinkResolver:  
    """Convert a raw URL into (provider, reference)."""  
  
    def resolve(self, url):  
        url = url.strip()  
        parsed = urlparse(url)  
        host = parsed.netloc.lower().lstrip("www.")  
  
        # --- YouTube -------------------------------------------------  
        if host in ("youtube.com", "m.youtube.com"):  
            video_id = parse_qs(parsed.query).get("v", [""])[0]  
            if video_id:  
                return ("youtube", video_id)  
            # /shorts/<id> or /embed/<id>  
            parts = [p for p in parsed.path.split("/") if p]  
            if len(parts) >= 2 and parts[0] in ("shorts", "embed"):  
                return ("youtube", parts[1])  
  
        if host == "youtu.be":  
            video_id = parsed.path.lstrip("/")  
            if video_id:  
                return ("youtube", video_id)  
  
        # --- Internet Archive ---------------------------------------  
        if host == "archive.org":  
            parts = [p for p in parsed.path.split("/") if p]  
            # /download/<identifier>/<filename...>  
            if len(parts) >= 3 and parts[0] == "download":  
                return ("internet_archive", "/".join(parts[1:]))  
            # /details/<identifier>  -> identifier only; filename must be  
            # appended by the caller (the archive item may hold many files).  
            if len(parts) >= 2 and parts[0] == "details":  
                return ("internet_archive", parts[1])  
  
        # --- Anything else: treat the whole URL as a direct download -  
        return ("http", url)