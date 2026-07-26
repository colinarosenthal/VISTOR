"""
VISTOR Sports Event
"""

from __future__ import annotations

from metadata.media.media_item import MediaItem


class SportsEvent(MediaItem):
    """Represents a televised sporting event."""

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

        self.home_team: str = ""

        self.away_team: str = ""

        self.venue: str = ""

        self.season: str = ""

        self.event_type: str = ""

        self.is_live = False

    # ------------------------------------------------------------------
    # Sport
    # ------------------------------------------------------------------

    def get_sport(self):
        """Return the sport."""

        return self.sport

    def set_sport(self, sport: str):
        """Set the sport."""

        self.sport = sport

    # ------------------------------------------------------------------
    # League
    # ------------------------------------------------------------------

    def get_league(self):
        """Return the league."""

        return self.league

    def set_league(self, league: str):
        """Set the league."""

        self.league = league

    # ------------------------------------------------------------------
    # Teams
    # ------------------------------------------------------------------

    def get_home_team(self):
        """Return the home team."""

        return self.home_team

    def set_home_team(self, team: str):
        """Set the home team."""

        self.home_team = team

    def get_away_team(self):
        """Return the away team."""

        return self.away_team

    def set_away_team(self, team: str):
        """Set the away team."""

        self.away_team = team

    # ------------------------------------------------------------------
    # Venue
    # ------------------------------------------------------------------

    def get_venue(self):
        """Return the venue."""

        return self.venue

    def set_venue(self, venue: str):
        """Set the venue."""

        self.venue = venue

    # ------------------------------------------------------------------
    # Season
    # ------------------------------------------------------------------

    def get_season(self):
        """Return the sports season."""

        return self.season

    def set_season(self, season: str):
        """Set the sports season."""

        self.season = season

    # ------------------------------------------------------------------
    # Event Type
    # ------------------------------------------------------------------

    def get_event_type(self):
        """Return the event type."""

        return self.event_type

    def set_event_type(self, event_type: str):
        """Set the event type."""

        self.event_type = event_type

    # ------------------------------------------------------------------
    # Broadcast
    # ------------------------------------------------------------------

    def is_live_event(self):
        """Return whether the event is live."""

        return self.is_live

    def set_live(self, live: bool):
        """Set whether the event is live."""

        self.is_live = live

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title