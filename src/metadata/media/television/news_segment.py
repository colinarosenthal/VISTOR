"""
VISTOR News Segment

Represents a recorded news report, broadcast segment, or journalistic
program component.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from metadata.media.media_item import MediaItem

if TYPE_CHECKING:
    from metadata.library.person import Person


class NewsSegment(MediaItem):
    """Represents a television news report or broadcast segment."""

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

        self.anchors: list[Person] = []

        self.reporters: list[Person] = []

        self.network: str = ""

        self.location: str = ""

        self.topic_category: str = ""

        self.original_air_date: str = ""

    # ------------------------------------------------------------------
    # Anchors
    # ------------------------------------------------------------------

    def get_anchors(self):
        """Return the news anchors."""

        return self.anchors

    def add_anchor(self, anchor: Person):
        """Add a news anchor."""

        self.anchors.append(anchor)

    # ------------------------------------------------------------------
    # Reporters
    # ------------------------------------------------------------------

    def get_reporters(self):
        """Return the reporters."""

        return self.reporters

    def add_reporter(self, reporter: Person):
        """Add a reporter."""

        self.reporters.append(reporter)

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
    # Location
    # ------------------------------------------------------------------

    def get_location(self):
        """Return the story location."""

        return self.location

    def set_location(self, location: str):
        """Set the story location."""

        self.location = location

    # ------------------------------------------------------------------
    # Topic
    # ------------------------------------------------------------------

    def get_topic_category(self):
        """Return the news topic category."""

        return self.topic_category

    def set_topic_category(self, category: str):
        """Set the news topic category."""

        self.topic_category = category

    # ------------------------------------------------------------------
    # Air Date
    # ------------------------------------------------------------------

    def get_original_air_date(self):
        """Return the original broadcast date."""

        return self.original_air_date

    def set_original_air_date(self, date: str):
        """Set the original broadcast date."""

        self.original_air_date = date

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title
