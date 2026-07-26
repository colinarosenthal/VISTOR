"""
VISTOR Ambient Media
"""

from __future__ import annotations

from metadata.media.media_item import MediaItem


class Ambient(MediaItem):
    """Represents continuous ambient broadcast programming."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        title: str,
        release_year: int = 0,
        runtime_minutes: int = 30,
    ):
        super().__init__(
            id=id,
            title=title,
            release_year=release_year,
            runtime_minutes=runtime_minutes,
        )

        self.environment_type: str = ""

        self.is_looping = True

        self.seasonal = False

    # ------------------------------------------------------------------
    # Environment
    # ------------------------------------------------------------------

    def get_environment_type(self):
        """Return the ambient environment type."""

        return self.environment_type

    def set_environment_type(self, environment_type: str):
        """Set the ambient environment type."""

        self.environment_type = environment_type

    # ------------------------------------------------------------------
    # Playback
    # ------------------------------------------------------------------

    def is_looping_media(self):
        """Return whether the media is intended to loop."""

        return self.is_looping

    def set_looping(self, looping: bool):
        """Set whether the media loops."""

        self.is_looping = looping

    # ------------------------------------------------------------------
    # Seasonal
    # ------------------------------------------------------------------

    def is_seasonal_media(self):
        """Return whether the ambient content is seasonal."""

        return self.seasonal

    def set_seasonal(self, seasonal: bool):
        """Set whether the ambient content is seasonal."""

        self.seasonal = seasonal

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title