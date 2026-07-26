"""
VISTOR Concert
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from metadata.media.media_item import MediaItem

if TYPE_CHECKING:
    from metadata.library.person import Person


class Concert(MediaItem):
    """Represents a recorded musical performance."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        title: str,
        release_year: int = 0,
        runtime_minutes: int = 0,
    ):
        super().__init__(
            id=id,
            title=title,
            release_year=release_year,
            runtime_minutes=runtime_minutes,
        )

        self.performers: list[Person] = []

        self.venue: str = ""

        self.performance_date: str = ""

        self.tour_name: str = ""

        self.setlist: list[str] = []

        self.festival: str = ""

    # ------------------------------------------------------------------
    # Performers
    # ------------------------------------------------------------------

    def get_performers(self):
        """Return the performing artists."""

        return self.performers

    def add_performer(self, performer: Person):
        """Add a performer."""

        self.performers.append(performer)

    # ------------------------------------------------------------------
    # Venue
    # ------------------------------------------------------------------

    def get_venue(self):
        """Return the performance venue."""

        return self.venue

    def set_venue(self, venue: str):
        """Set the performance venue."""

        self.venue = venue

    # ------------------------------------------------------------------
    # Performance Date
    # ------------------------------------------------------------------

    def get_performance_date(self):
        """Return the original performance date."""

        return self.performance_date

    def set_performance_date(self, date: str):
        """Set the original performance date."""

        self.performance_date = date

    # ------------------------------------------------------------------
    # Tour
    # ------------------------------------------------------------------

    def get_tour_name(self):
        """Return the tour name."""

        return self.tour_name

    def set_tour_name(self, tour_name: str):
        """Set the tour name."""

        self.tour_name = tour_name

    # ------------------------------------------------------------------
    # Setlist
    # ------------------------------------------------------------------

    def get_setlist(self):
        """Return the concert setlist."""

        return self.setlist

    def add_song(self, song: str):
        """Add a song to the setlist."""

        self.setlist.append(song)

    # ------------------------------------------------------------------
    # Festival
    # ------------------------------------------------------------------

    def get_festival(self):
        """Return the associated festival."""

        return self.festival

    def set_festival(self, festival: str):
        """Set the festival name."""

        self.festival = festival

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title