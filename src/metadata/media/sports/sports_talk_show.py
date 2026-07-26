"""
VISTOR Sports Talk Show

Represents a sports discussion program, analysis show, or commentary broadcast.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from metadata.media.media_item import MediaItem

if TYPE_CHECKING:
    from metadata.library.person import Person


class SportsTalkShow(MediaItem):
    """Represents a sports discussion or analysis program."""

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

        self.hosts: list[Person] = []

        self.guests: list[Person] = []

        self.sport_focus: str = ""

        self.league_focus: str = ""

        self.network: str = ""

    # ------------------------------------------------------------------
    # Hosts
    # ------------------------------------------------------------------

    def get_hosts(self):
        """Return the show hosts."""

        return self.hosts

    def add_host(self, host: Person):
        """Add a host."""

        self.hosts.append(host)

    # ------------------------------------------------------------------
    # Guests
    # ------------------------------------------------------------------

    def get_guests(self):
        """Return the show guests."""

        return self.guests

    def add_guest(self, guest: Person):
        """Add a guest."""

        self.guests.append(guest)

    # ------------------------------------------------------------------
    # Sport Focus
    # ------------------------------------------------------------------

    def get_sport_focus(self):
        """Return the primary sport focus."""

        return self.sport_focus

    def set_sport_focus(self, sport: str):
        """Set the primary sport focus."""

        self.sport_focus = sport

    # ------------------------------------------------------------------
    # League Focus
    # ------------------------------------------------------------------

    def get_league_focus(self):
        """Return the primary league focus."""

        return self.league_focus

    def set_league_focus(self, league: str):
        """Set the primary league focus."""

        self.league_focus = league

    # ------------------------------------------------------------------
    # Network
    # ------------------------------------------------------------------

    def get_network(self):
        """Return the originating network."""

        return self.network

    def set_network(self, network: str):
        """Set the originating network."""

        self.network = network

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title