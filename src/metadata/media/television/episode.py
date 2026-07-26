"""
VISTOR Episode
"""

from metadata.media.media_item import MediaItem
from metadata.library.season import Season


class Episode(MediaItem):
    """Represents a television episode."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        title: str,
        season: Season,
        episode_number: int,
        **kwargs,
    ):
        super().__init__(
            id=id,
            title=title,
            **kwargs,
        )

        self.season = season

        self.episode_number = episode_number

        self.production_code: str = ""

        self.absolute_episode_number: int | None = None

        self.original_air_date: str = ""

    # ------------------------------------------------------------------
    # Season Information
    # ------------------------------------------------------------------

    def get_season(self):
        """Return the parent season."""

        return self.season

    def get_series(self):
        """Return the parent series."""

        return self.season.get_series()

    def get_franchise(self):
        """Return the parent franchise."""

        return self.get_series().get_franchise()

    # ------------------------------------------------------------------
    # Episode Information
    # ------------------------------------------------------------------

    def get_episode_number(self):
        """Return the episode number."""

        return self.episode_number

    def get_absolute_episode_number(self):
        """Return the absolute episode number."""

        return self.absolute_episode_number

    def set_absolute_episode_number(self, number: int):
        """Set the absolute episode number."""

        self.absolute_episode_number = number

    # ------------------------------------------------------------------
    # Production
    # ------------------------------------------------------------------

    def get_production_code(self):
        """Return the production code."""

        return self.production_code

    def set_production_code(self, code: str):
        """Set the production code."""

        self.production_code = code

    # ------------------------------------------------------------------
    # Broadcast
    # ------------------------------------------------------------------

    def get_original_air_date(self):
        """Return the original air date."""

        return self.original_air_date

    def set_original_air_date(self, air_date: str):
        """Set the original air date."""

        self.original_air_date = air_date

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def get_display_name(self):
        """Return a formatted episode identifier."""

        season_number = self.season.get_season_number()

        return (
            f"S{season_number:02}"
            f"E{self.episode_number:02}"
            f" - {self.title}"
        )

    def __str__(self):
        return self.get_display_name()