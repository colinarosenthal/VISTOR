"""
VISTOR Franchise
"""


class Franchise:
    """Represents a shared intellectual property."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        name: str,
        description: str = "",
    ):
        self.id = id

        self.name = name

        self.description = description

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_id(self):
        """Return the franchise identifier."""

        return self.id

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