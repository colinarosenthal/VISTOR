"""
VISTOR Sports Highlight

Represents a recorded sports recap, highlight package, or condensed
presentation of athletic events.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from metadata.media.media_item import MediaItem

if TYPE_CHECKING:
    from metadata.media.sports.sports_event import SportsEvent


class SportsHighlight(MediaItem):
    """Represents a sports highlight package or recap program."""

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

        self.sport: str = ""

        self.league: str = ""

        self.related_events: list[SportsEvent] = []

        self.description: str = ""

    # ------------------------------------------------------------------
    # Sport
    # ------------------------------------------------------------------

    def get_sport(self):
        """Return the sport type."""

        return self.sport

    def set_sport(self, sport: str):
        """Set the sport type."""

        self.sport = sport

    # ------------------------------------------------------------------
    # League
    # ------------------------------------------------------------------

    def get_league(self):
        """Return the associated league."""

        return self.league

    def set_league(self, league: str):
        """Set the associated league."""

        self.league = league

    # ------------------------------------------------------------------
    # Related Events
    # ------------------------------------------------------------------

    def get_related_events(self):
        """Return the sporting events covered."""

        return self.related_events

    def add_related_event(self, event: SportsEvent):
        """Add a related sporting event."""

        self.related_events.append(event)

    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------

    def get_description(self):
        """Return the highlight description."""

        return self.description

    def set_description(self, description: str):
        """Set the highlight description."""

        self.description = description

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title
