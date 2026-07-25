"""
VISTOR Music Genre

Defines standardized music genre metadata values used throughout VISTOR.
"""


class MusicGenre:
    """Represents a music genre classification."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        name: str,
        description: str = "",
        parent_genre=None,
    ):
        self.name = name

        self.description = description

        self.parent_genre = parent_genre

    # ------------------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------------------

    def get_name(self):
        """Return the music genre name."""

        return self.name

    def get_description(self):
        """Return the music genre description."""

        return self.description

    def get_parent_genre(self):
        """Return the parent music genre."""

        return self.parent_genre

    # ------------------------------------------------------------------
    # Modification
    # ------------------------------------------------------------------

    def set_description(self, description: str):
        """Set the music genre description."""

        self.description = description

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name