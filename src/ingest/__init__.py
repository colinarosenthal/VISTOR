"""
VISTOR Ingest

Operator-facing drag-and-drop authoring front-end for adding media to the
library. Drives the existing RecordBuilder -> TMDBSource -> MediaIngestor
seam; it is NOT part of the TV-viewing runtime (see src/osd for on-screen
playback overlays).
"""

from .ingest_session import IngestSession

__all__ = ["IngestSession"]
