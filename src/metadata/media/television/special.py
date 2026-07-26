"""
VISTOR Television Special

Represents a standalone television program that is not part of a regular episodic series.
"""

from metadata.media.media_item import MediaItem


class Special(MediaItem):
    """Represents a standalone television special."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        title: str,
        release_year: int = 0,
        runtime_minutes: int = 0,
        description: str = "",
    ):
        super().__init__(
            id=id,
            title=title,
            runtime_minutes=runtime_minutes,
        )

        self.release_year = release_year
        self.description = description

    # ------------------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------------------

    def get_release_year(self):
        """Return the original release year."""

        return self.release_year

    def get_description(self):
        """Return the special description."""

        return self.description

    def set_description(self, description: str):
        """Set the special description."""

        self.description = description

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title