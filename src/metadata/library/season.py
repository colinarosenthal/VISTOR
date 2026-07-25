"""
VISTOR Season
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from metadata.models.programming.series import Series
    from metadata.models.programming.episode import Episode


class Season:
    """Represents a season within a television series."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        series: Series,
        season_number: int,
        title: str = "",
        premiere_year: int = 0,
    ):
        self.series = series

        self.season_number = season_number

        self.title = title

        self.premiere_year = premiere_year

        self.episodes: list[Episode] = []

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_series(self):
        """Return the parent series."""

        return self.series

    def get_season_number(self):
        """Return the season number."""

        return self.season_number

    def get_title(self):
        """Return the season title."""

        return self.title

    def get_premiere_year(self):
        """Return the premiere year."""

        return self.premiere_year

    def get_episodes(self):
        """Return all episodes."""

        return self.episodes

    # ------------------------------------------------------------------
    # Episodes
    # ------------------------------------------------------------------

    def add_episode(self, episode: Episode):
        """Add an episode."""

        self.episodes.append(episode)

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def get_display_name(self):
        """Return a display-friendly season name."""

        if self.title:
            return self.title

        return f"Season {self.season_number}"

    def __str__(self):
        return self.get_display_name()