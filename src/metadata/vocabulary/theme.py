"""
VISTOR Theme

Defines thematic metadata values used throughout VISTOR.
"""


class Theme:
    """Represents a thematic concept associated with media."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        name: str,
        description: str = "",
        parent_theme=None,
    ):
        self.name = name

        self.description = description

        self.parent_theme = parent_theme

    # ------------------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------------------

    def get_name(self):
        """Return the theme name."""

        return self.name

    def get_description(self):
        """Return the theme description."""

        return self.description

    def get_parent_theme(self):
        """Return the parent theme."""

        return self.parent_theme

    # ------------------------------------------------------------------
    # Modification
    # ------------------------------------------------------------------

    def set_description(self, description: str):
        """Set the theme description."""

        self.description = description

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name