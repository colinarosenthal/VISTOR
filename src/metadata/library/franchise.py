"""
VISTOR Franchise
"""


class Franchise:
    """Represents a collection of related media."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        name: str,
        description: str = "",
    ):
        self.name = name

        self.description = description

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_name(self):
        """Return the franchise name."""

        return self.name

    def get_description(self):
        """Return the franchise description."""

        return self.description

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name