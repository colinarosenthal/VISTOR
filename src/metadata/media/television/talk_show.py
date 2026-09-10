"""
VISTOR Talk Show

Represents a television talk show, interview program, or discussion-based
broadcast.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from metadata.media.media_item import MediaItem

if TYPE_CHECKING:
    from metadata.library.person import Person


class TalkShow(MediaItem):
    """Represents a television talk show or discussion program."""

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

        self.format: str = ""

        self.network: str = ""

        self.topic_categories: list[str] = []

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
    # Format
    # ------------------------------------------------------------------

    def get_format(self):
        """Return the program format."""

        return self.format

    def set_format(self, format: str):
        """Set the program format."""

        self.format = format

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
    # Topics
    # ------------------------------------------------------------------

    def get_topic_categories(self):
        """Return the topic categories."""

        return self.topic_categories

    def add_topic_category(self, category: str):
        """Add a topic category."""

        self.topic_categories.append(category)

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title
