"""
VISTOR Season
"""

from metadata.library.series import Series


class Season:
    """Represents a season within a television series."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        series: Series,
        season_number: int,
        title: str = "",
        description: str = "",
        premiere_year: int = 0,
    ):
        self.id = id

        self.series = series

        self.season_number = season_number

        self.title = title

        self.description = description

        self.premiere_year = premiere_year

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_id(self):
        """Return the season identifier."""

        return self.id

    def get_series(self):
        """Return the parent series."""

        return self.series

    def get_season_number(self):
        """Return the season number."""

        return self.season_number

    def get_title(self):
        """Return the season title."""

        return self.title

    def get_description(self):
        """Return the season description."""

        return self.description

    def get_premiere_year(self):
        """Return the premiere year."""

        return self.premiere_year

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def has_title(self):
        """Return whether the season has a custom title."""

        return bool(self.title)

    def get_display_name(self):
        """Return a display-friendly season name."""

        if self.title:
            return self.title

        return f"Season {self.season_number}"

    def __str__(self):
        return self.get_display_name()
