"""
VISTOR Weather Segment

Represents a weather broadcast segment.

Weather segments are unique within VISTOR because they may be generated dynamically using modern weather data rather than relying exclusively on archived broadcast footage.

The presentation layer should recreate the style of historical weather broadcasts while allowing current weather information to be displayed.
"""

from metadata.media.television.media_item import MediaItem


class WeatherSegment(MediaItem):
    """Represents a television weather broadcast segment."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        title: str,
        location: str = "",
        runtime_minutes: int = 0,
        description: str = "",
        generated: bool = False,
    ):
        super().__init__(
            id=id,
            title=title,
            runtime_minutes=runtime_minutes,
        )

        self.location = location
        self.description = description
        self.generated = generated

    # ------------------------------------------------------------------
    # Weather Information
    # ------------------------------------------------------------------

    def get_location(self):
        """Return the weather location."""

        return self.location

    def get_description(self):
        """Return the weather segment description."""

        return self.description

    def is_generated(self):
        """Return whether the segment uses generated weather data."""

        return self.generated

    def set_description(self, description: str):
        """Set the weather segment description."""

        self.description = description

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title