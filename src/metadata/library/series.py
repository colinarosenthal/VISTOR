"""
VISTOR Series
"""

from metadata.library.franchise import Franchise


class Series:
    """Represents a television series."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        title: str,
        franchise: Franchise | None = None,
        description: str = "",
        premiere_year: int = 0,
        finale_year: int = 0,
    ):
        self.id = id

        self.title = title

        self.franchise = franchise

        self.description = description

        self.premiere_year = premiere_year
        self.finale_year = finale_year

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_id(self):
        """Return the series identifier."""

        return self.id

    def get_title(self):
        """Return the series title."""

        return self.title

    def get_franchise(self):
        """Return the associated franchise."""

        return self.franchise

    def get_description(self):
        """Return the series description."""

        return self.description

    def get_premiere_year(self):
        """Return the premiere year."""

        return self.premiere_year

    def get_finale_year(self):
        """Return the finale year."""

        return self.finale_year

    # ------------------------------------------------------------------
    # Setters
    # ------------------------------------------------------------------

    def set_franchise(self, franchise: Franchise):
        """Assign the associated franchise."""

        self.franchise = franchise

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def belongs_to_franchise(self):
        """Return whether this series belongs to a franchise."""

        return self.franchise is not None

    def __str__(self):
        return self.title
