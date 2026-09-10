"""
VISTOR Media Asset
"""

from pathlib import Path

from metadata.enums.download_status import DownloadStatus


class MediaAsset:
    """Represents a single physical media file."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        asset_id: str,
        path: Path,
        checksum: str = "",
        runtime_seconds: int = 0,
        file_size: int = 0,
        video_codec: str = "",
        audio_codec: str = "",
        container: str = "",
        width: int = 0,
        height: int = 0,
        frame_rate: float = 0.0,
        verified: bool = False,
        download_status: DownloadStatus = DownloadStatus.NOT_DOWNLOADED,
        last_played: str = "",
        sources=None,
        pinned: bool = False,
        broadcast_score: float = 0.0,
        retention_score: float = 0.0,
        fingerprint: str = "",
        breakpoints=None,
    ):
        self.asset_id = asset_id

        self.path = Path(path)

        self.checksum = checksum

        self.runtime_seconds = runtime_seconds

        self.file_size = file_size

        self.video_codec = video_codec
        self.audio_codec = audio_codec
        self.container = container

        self.width = width
        self.height = height

        self.frame_rate = frame_rate

        self.verified = verified

        # --------------------------------------------------------------
        # Intelligent Content Management (runtime availability state)
        # --------------------------------------------------------------

        # Where the file currently is in its download lifecycle.
        self.download_status = download_status

        # ISO-8601 timestamp string of the last time this asset aired.
        self.last_played = last_played

        # Ranked list of places this file can be (re)fetched from. Each
        # entry is a dict, e.g.:
        #   {"provider": "internet_archive",
        #    "reference": "entiretyofeva/endofevaalldub.mkv",
        #    "quality": ""}
        # Order = preference; resolver tries them top-down on failure.
        self.sources = list(sources) if sources else []

        # Retention pin: if True, eviction must never remove this asset
        # regardless of scores (used for at-risk / hard-to-replace media).
        self.pinned = pinned

        # Broadcast score: how likely this asset is to be selected for
        # streaming (drives broadcast frequency ONLY). Never mixed with
        # storage cost.
        self.broadcast_score = broadcast_score

        # Retention score: combined with file_size to decide what stays
        # on the drive. Kept separate from broadcast_score on purpose.
        self.retention_score = retention_score

        # Perceptual/keyframe fingerprint used to find replacement media
        # when a source disappears. Populated in a later stage.
        self.fingerprint = fingerprint

        # Commercial-break offsets (seconds into the file) where Mid-Program
        # mode may insert a Broadcast Event. Detected at download time from
        # container chapters or black+silence analysis; [] means none known.
        self.breakpoints = list(breakpoints) if breakpoints else []

    # ------------------------------------------------------------------
    # Identification
    # ------------------------------------------------------------------

    def get_asset_id(self):
        """Return the asset identifier."""

        return self.asset_id

    # ------------------------------------------------------------------
    # File Information
    # ------------------------------------------------------------------

    def get_path(self):
        """Return the asset path."""

        return self.path

    def get_filename(self):
        """Return the asset filename."""

        return self.path.name

    def get_extension(self):
        """Return the asset extension."""

        return self.path.suffix.lower()

    # ------------------------------------------------------------------
    # Technical Information
    # ------------------------------------------------------------------

    def get_runtime_seconds(self):
        """Return runtime in seconds."""

        return self.runtime_seconds

    def get_file_size(self):
        """Return file size in bytes."""

        return self.file_size

    def get_video_codec(self):
        """Return the video codec."""

        return self.video_codec

    def get_audio_codec(self):
        """Return the audio codec."""

        return self.audio_codec

    def get_container(self):
        """Return the media container."""

        return self.container

    def get_resolution(self):
        """Return (width, height)."""

        return (self.width, self.height)

    def get_frame_rate(self):
        """Return frame rate."""

        return self.frame_rate

    def get_checksum(self):
        """Return checksum."""

        return self.checksum

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    def is_verified(self):
        """Return whether the asset has been verified."""

        return self.verified

    def set_verified(self, verified: bool):
        """Set verification status."""

        self.verified = verified

    # ------------------------------------------------------------------
    # Download Status
    # ------------------------------------------------------------------

    def get_download_status(self):
        """Return the current download status."""

        return self.download_status

    def set_download_status(self, status: DownloadStatus):
        """Set the current download status."""

        self.download_status = status

    def is_available(self):
        """Return whether the file is downloaded and present."""

        return self.download_status == DownloadStatus.DOWNLOADED

    def needs_download(self):
        """Return whether this asset should be (re)fetched."""

        return self.download_status in (
            DownloadStatus.NOT_DOWNLOADED,
            DownloadStatus.MISSING,
            DownloadStatus.FAILED,
        )

    # ------------------------------------------------------------------
    # Playback Bookkeeping
    # ------------------------------------------------------------------

    def get_last_played(self):
        """Return the last-played timestamp string."""

        return self.last_played

    def set_last_played(self, timestamp: str):
        """Set the last-played timestamp string."""

        self.last_played = timestamp

    # ------------------------------------------------------------------
    # Sources (for re-acquisition across multiple archives)
    # ------------------------------------------------------------------

    def add_source(
        self,
        provider: str,
        reference: str,
        quality: str = "",
        date_posted: str = "",
    ):
        """Add a ranked fetch source for this asset.

        date_posted is an ISO-8601 date/datetime string for when the
        source first appeared (e.g. an Internet Archive upload date).
        Older postings are less likely to be taken down, which lowers
        the asset's takedown risk / retention fragility.
        """

        self.sources.append(
            {
                "provider": provider,
                "reference": reference,
                "quality": quality,
                "date_posted": date_posted,
            }
        )

    def get_sources(self):
        """Return the ranked list of fetch sources."""

        return self.sources

    def set_sources(self, sources):
        """Replace the full ranked source list."""

        self.sources = list(sources) if sources else []

    def has_source(self):
        """Return whether any fetch source is known."""

        return len(self.sources) > 0

    def get_source_age_days(self):
        """Return the age in days of the longest-standing source posting.

        Uses the oldest `date_posted` across all sources (the longer a
        copy has survived, the lower its takedown risk). Sources with a
        missing or unparseable date are ignored. Returns 0 if no source
        has a usable date_posted.
        """

        from datetime import datetime

        oldest = None

        for source in self.sources:
            raw = source.get("date_posted", "")

            if not raw:
                continue

            try:
                posted = datetime.fromisoformat(raw)
            except ValueError:
                continue

            # Normalize to naive for a consistent comparison/subtraction.
            if posted.tzinfo is not None:
                posted = posted.replace(tzinfo=None)

            if oldest is None or posted < oldest:
                oldest = posted

        if oldest is None:
            return 0

        return (datetime.now() - oldest).days

    # ------------------------------------------------------------------
    # Retention / Scoring
    # ------------------------------------------------------------------

    def is_pinned(self):
        """Return whether this asset is pinned against eviction."""

        return self.pinned

    def set_pinned(self, pinned: bool):
        """Set the retention pin."""

        self.pinned = pinned

    def get_broadcast_score(self):
        """Return the broadcast-frequency score."""

        return self.broadcast_score

    def set_broadcast_score(self, score: float):
        """Set the broadcast-frequency score."""

        self.broadcast_score = score

    def get_retention_score(self):
        """Return the on-disk retention score."""

        return self.retention_score

    def set_retention_score(self, score: float):
        """Set the on-disk retention score."""

        self.retention_score = score

    def get_fingerprint(self):
        """Return the keyframe fingerprint (may be empty)."""

        return self.fingerprint

    def set_fingerprint(self, fingerprint: str):
        """Set the keyframe fingerprint."""

        self.fingerprint = fingerprint

    def get_breakpoints(self):
        """Return the detected commercial-break offsets (seconds)."""

        return self.breakpoints

    def set_breakpoints(self, breakpoints):
        """Set the detected commercial-break offsets (seconds)."""

        self.breakpoints = list(breakpoints) if breakpoints else []

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dictionary(self):
        """Flatten this asset to a JSON-safe dictionary."""

        return {
            "asset_id": self.asset_id,
            "path": str(self.path),
            "checksum": self.checksum,
            "runtime_seconds": self.runtime_seconds,
            "file_size": self.file_size,
            "video_codec": self.video_codec,
            "audio_codec": self.audio_codec,
            "container": self.container,
            "width": self.width,
            "height": self.height,
            "frame_rate": self.frame_rate,
            "verified": self.verified,
            "download_status": self.download_status.name,
            "last_played": self.last_played,
            "sources": [dict(s) for s in self.sources],
            "pinned": self.pinned,
            "broadcast_score": self.broadcast_score,
            "retention_score": self.retention_score,
            "fingerprint": self.fingerprint,
            "breakpoints": list(self.breakpoints),
        }

    @classmethod
    def from_dictionary(cls, data):
        """Rebuild a MediaAsset from a to_dictionary() record."""

        status_name = data.get("download_status", DownloadStatus.NOT_DOWNLOADED.name)

        try:
            status = DownloadStatus[status_name]
        except KeyError:
            status = DownloadStatus.NOT_DOWNLOADED

        return cls(
            asset_id=data["asset_id"],
            path=data.get("path", ""),
            checksum=data.get("checksum", ""),
            runtime_seconds=data.get("runtime_seconds", 0),
            file_size=data.get("file_size", 0),
            video_codec=data.get("video_codec", ""),
            audio_codec=data.get("audio_codec", ""),
            container=data.get("container", ""),
            width=data.get("width", 0),
            height=data.get("height", 0),
            frame_rate=data.get("frame_rate", 0.0),
            verified=data.get("verified", False),
            download_status=status,
            last_played=data.get("last_played", ""),
            sources=data.get("sources", []),
            pinned=data.get("pinned", False),
            broadcast_score=data.get("broadcast_score", 0.0),
            retention_score=data.get("retention_score", 0.0),
            fingerprint=data.get("fingerprint", ""),
            breakpoints=data.get("breakpoints", []),
        )

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def exists(self):
        """Return whether the asset exists."""

        return self.path.exists()

    def __str__(self):
        return self.get_filename()
