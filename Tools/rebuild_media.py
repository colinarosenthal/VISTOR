"""
VISTOR rebuild-from-sidecars CLI

Rebuild the catalog from the per-file .sidecar metadata without pulling the
media bytes:

    python rebuild_media.py               # rebuild AND download
    python rebuild_media.py --no-download # catalog-only; leave files evicted
"""

import sys
from pathlib import Path

# Resolve <repo root>/src regardless of where this script is launched from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from metadata.services.media_ingestor import MediaIngestor


def main(argv):
    download = "--no-download" not in argv

    report = MediaIngestor().rebuild_from_sidecars(download=download)

    print("Added:      ", report.get("added", []))
    print("Retried:    ", report.get("retried", []))
    print("Skipped:    ", report.get("skipped", []))
    print("Downloaded: ", report.get("resolved", []))
    print("Unresolved: ", report.get("unresolved", []))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
