"""
VISTOR Genre

Defines standardized genre metadata values used throughout VISTOR.
"""


class Genre:
    """Represents a media genre classification."""

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
        """Return the genre name."""

        return self.name

    def get_description(self):
        """Return the genre description."""

        return self.description

    def get_parent_genre(self):
        """Return the parent genre."""

        return self.parent_genre

    # ------------------------------------------------------------------
    # Modification
    # ------------------------------------------------------------------

    def set_description(self, description: str):
        """Set the genre description."""

        self.description = description

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name
