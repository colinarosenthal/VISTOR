"""
VISTOR Tag

Defines flexible descriptive metadata tags used throughout VISTOR.
"""


class Tag:
    """Represents a flexible metadata tag."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        name: str,
        description: str = "",
        category: str = "",
    ):
        self.name = name

        self.description = description

        self.category = category

    # ------------------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------------------

    def get_name(self):
        """Return the tag name."""

        return self.name

    def get_description(self):
        """Return the tag description."""

        return self.description

    def get_category(self):
        """Return the tag category."""

        return self.category

    # ------------------------------------------------------------------
    # Modification
    # ------------------------------------------------------------------

    def set_description(self, description: str):
        """Set the tag description."""

        self.description = description

    def set_category(self, category: str):
        """Set the tag category."""

        self.category = category

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name
