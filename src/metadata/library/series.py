"""
VISTOR Series
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from metadata.models.relationships.franchise import Franchise
    from metadata.models.programming.season import Season


class Series:
    """Represents a television series."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        title: str,
        franchise: Franchise | None = None,
        description: str = "",
        premiere_year: int = 0,
        finale_year: int = 0,
    ):
        self.title = title

        self.franchise = franchise

        self.description = description

        self.premiere_year = premiere_year
        self.finale_year = finale_year

        self.seasons: list[Season] = []

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_title(self):
        """Return the series title."""

        return self.title

    def get_franchise(self):
        """Return the franchise."""

        return self.franchise

    def get_description(self):
        """Return the description."""

        return self.description

    def get_premiere_year(self):
        """Return the premiere year."""

        return self.premiere_year

    def get_finale_year(self):
        """Return the finale year."""

        return self.finale_year

    def get_seasons(self):
        """Return all seasons."""

        return self.seasons

    # ------------------------------------------------------------------
    # Setters
    # ------------------------------------------------------------------

    def set_franchise(self, franchise: Franchise):
        """Set the franchise."""

        self.franchise = franchise

    # ------------------------------------------------------------------
    # Seasons
    # ------------------------------------------------------------------

    def add_season(self, season: Season):
        """Add a season."""

        self.seasons.append(season)

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title