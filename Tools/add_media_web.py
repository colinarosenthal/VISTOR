"""
VISTOR Add-Media Web launcher.

Bootstraps the environment BEFORE the web app imports/runs:
  1. Puts src/ on sys.path (same as add_media.py / test_metadata.py).
  2. Injects the winget ffmpeg bin folder onto PATH so yt-dlp can merge.
  3. FORCES TMDB_API_KEY into this process's env so the enrichment chain
     and the "did you mean?" candidate search both fire.
  4. Auto-opens the browser, then serves the Flask app.

Order matters: steps 1-3 must all run BEFORE `from ingest.web_app import run`,
because importing web_app constructs `_session = IngestSession()` at module
load, which constructs `TMDBSource()`, which reads TMDB_API_KEY *once* in its
__init__. If the key isn't in os.environ at that moment, every lookup is
skipped and you get the raw 2019 "Word" scrape with no candidates.
"""

import os

# Ensure libmpv-2.dll is loadable via an ABSOLUTE path. python-mpv's loader
# refuses DLLs found under relative %PATH% entries (e.g. the cwd), so point it
# at the repo root where libmpv-2.dll lives before importing the binding.
from pathlib import Path  
_dll_dir = str(Path(__file__).resolve().parent.parent)  # repo root, where libmpv-2.dll lives  
if _dll_dir not in os.environ.get("PATH", ""):  
    os.environ["PATH"] = _dll_dir + os.pathsep + os.environ.get("PATH", "")

import mpv
import sys
import glob
import threading
import webbrowser

import sys  
from pathlib import Path  
  
# Resolve <repo root>/src regardless of where this script is launched from.  
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# 1. Put winget's ffmpeg bin on PATH (Windows). No-op if not found.
#    yt-dlp needs ffmpeg on PATH to merge the bv*+ba streams into .mkv;
#    without it every download lands in `unresolved`.
_matches = glob.glob(os.path.join(
    os.environ.get("LOCALAPPDATA", ""),
    r"Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*-full_build\bin",
))
if _matches:
    os.environ["PATH"] = _matches[0] + os.pathsep + os.environ.get("PATH", "")

# 2. FORCE the TMDB key into THIS process's environment.
#    Use a hard assignment, NOT os.environ.setdefault(...): setdefault is a
#    no-op if the name already exists as an empty/blank string, which is
#    exactly the failure you hit. Assigning guarantees TMDBSource() sees it.
os.environ.setdefault("TMDB_API_KEY", os.environ.get("TMDB_API_KEY", ""))  
if not os.environ.get("TMDB_API_KEY"):  
    raise SystemExit("Set the TMDB_API_KEY environment variable before launching.")

# 3. Import the app ONLY AFTER the env is ready (this line builds _session ->
#    IngestSession -> TMDBSource, which snapshots TMDB_API_KEY in __init__).
from ingest.web_app import run

_URL = "http://127.0.0.1:5000"


def _open_browser():
    # Small delay so the server is listening before the tab opens.
    webbrowser.open(_URL)


def main():
    # Fire the browser open on a timer thread; run() blocks serving forever.
    threading.Timer(1.0, _open_browser).start()
    print(f"Serving VISTOR ingest UI at {_URL} (Ctrl+C to quit)")
    run()

if __name__ == "__main__":
    main()
