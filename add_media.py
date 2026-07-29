"""  
VISTOR add_media CLI  
  
Add media to VISTOR two ways:  
  
1. From a JSON drop-in file (a single record or an array of records, each  
   matching the media.json shape: type, id, title, ... optional  
   assets[].sources[]):  
  
       python add_media.py path/to/redline.json  
       python add_media.py path/to/redline.json --no-download  
  
2. From a raw link (YouTube / Internet Archive / direct URL). The link is  
   parsed into a (provider, reference) source and, where possible, the  
   descriptive metadata (title, year, description, runtime) is scraped so the  
   record is built for you:  
  
       python add_media.py "https://youtu.be/fzHD04_OwyQ"  
       python add_media.py "https://youtu.be/fzHD04_OwyQ" --type Movie --title "Redline"  
       python add_media.py "https://youtu.be/fzHD04_OwyQ" --genres "Animation,Action" --no-download  
  
Anything that starts with "http" is treated as a link; otherwise the argument  
is treated as a path to a JSON drop-in file.  
"""  
  
import json  
import sys  
import tempfile  
from pathlib import Path  
  
# Make the src/ layout importable exactly like test_metadata.py does.  
sys.path.insert(0, "src")  
  
from metadata.services.media_ingestor import MediaIngestor  
  
  
def _parse_flags(argv):  
    """Split argv into (positional, options-dict).  
  
    Supports:  
        --no-download            -> download = False  
        --type <MediaType>       -> overrides["type"]  (e.g. Movie, MusicVideo)  
        --title <title>          -> overrides["title"]  
        --genres "A,B,C"         -> overrides["genres"] as a list  
    """  
  
    positional = []  
    download = True  
    media_type = "Movie"  
    overrides = {}  
  
    i = 0  
    while i < len(argv):  
        arg = argv[i]  
  
        if arg == "--no-download":  
            download = False  
        elif arg == "--type" and i + 1 < len(argv):  
            media_type = argv[i + 1]  
            i += 1  
        elif arg == "--title" and i + 1 < len(argv):  
            overrides["title"] = argv[i + 1]  
            i += 1  
        elif arg == "--genres" and i + 1 < len(argv):  
            overrides["genres"] = [  
                g.strip() for g in argv[i + 1].split(",") if g.strip()  
            ]  
            i += 1  
        else:  
            positional.append(arg)  
  
        i += 1  
  
    return positional, download, media_type, overrides  
  
  
def _ingest_link(url, download, media_type, overrides):  
    """Build a record from a raw URL, then ingest it via a temp JSON file."""  
  
    # Imported lazily so the JSON-file path keeps working even if the  
    # link-building dependencies (yt-dlp, etc.) are not installed.  
    from metadata.services.record_builder import RecordBuilder  
  
    record = RecordBuilder().build(  
        url,  
        media_type=media_type,  
        overrides=overrides,  
    )  
  
    # Drop the built record to a temp JSON file and reuse the file path so  
    # there is exactly one ingestion path (the same one the UI will emit).  
    tmp = Path(tempfile.mkdtemp()) / "drop_in.json"  
    tmp.write_text(json.dumps([record], indent=2), encoding="utf-8")  
  
    print("Built record:")  
    print(json.dumps(record, indent=2))  
  
    return MediaIngestor().ingest_file(str(tmp), download=download)  
  
  
def main(argv):  
    positional, download, media_type, overrides = _parse_flags(argv)  
  
    if not positional:  
        print(  
            "Usage:\n"  
            "  python add_media.py <drop_in.json> [--no-download]\n"  
            "  python add_media.py <url> [--type Movie] [--title \"...\"] "  
            "[--genres \"A,B\"] [--no-download]"  
        )  
        return 1  
  
    target = positional[0]  
  
    if target.lower().startswith("http"):  
        report = _ingest_link(target, download, media_type, overrides)  
    else:  
        report = MediaIngestor().ingest_file(target, download=download)  
  
    print("Added:      ", report["added"])  
    print("Skipped:    ", report["skipped"])  
    print("Downloaded: ", report["resolved"])  
    print("Unresolved: ", report["unresolved"])  
  
    return 0  
  
  
if __name__ == "__main__":  
    raise SystemExit(main(sys.argv[1:]))