"""
VISTOR Live Performance
Represents a recorded musical performance 
originally broadcast as part of
another television program, live event, or special 
presentation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from metadata.media.media_item import MediaItem

if TYPE_CHECKING:
    from metadata.library.person import Person


class LivePerformance(MediaItem):
    """Represents a recorded live musical performance."""

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

        self.program_name: str = ""

        self.host: str = ""

        self.venue: str = ""

        self.performance_date: str = ""

        self.song_title: str = ""

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
    # Program
    # ------------------------------------------------------------------

    def get_program_name(self):
        """Return the originating program."""

        return self.program_name

    def set_program_name(self, program_name: str):
        """Set the originating program."""

        self.program_name = program_name

    # ------------------------------------------------------------------
    # Host
    # ------------------------------------------------------------------

    def get_host(self):
        """Return the host."""

        return self.host

    def set_host(self, host: str):
        """Set the host."""

        self.host = host

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
    # Song
    # ------------------------------------------------------------------

    def get_song_title(self):
        """Return the performed song."""

        return self.song_title

    def set_song_title(self, song: str):
        """Set the performed song."""

        self.song_title = song

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title