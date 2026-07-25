"""
VISTOR Media Asset
"""

from pathlib import Path


class MediaAsset:
    """Represents a single physical media file."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
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
    ):
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

    # ------------------------------------------------------------------
    # Getters
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

    def is_verified(self):
        """Return whether the asset has been verified."""

        return self.verified

    # ------------------------------------------------------------------
    # Setters
    # ------------------------------------------------------------------

    def set_verified(self, verified: bool):
        """Set verification status."""

        self.verified = verified

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def exists(self):
        """Return whether the asset exists."""

        return self.path.exists()

    def __str__(self):
        return self.get_filename()