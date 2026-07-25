"""
VISTOR Media Type
"""

from enum import Enum, auto


class MediaType(Enum):
    """Defines the primary classification of a media item."""

    # ------------------------------------------------------------------
    # Programming
    # ------------------------------------------------------------------

    TV_SHOW = auto()

    MOVIE = auto()

    SPORTS_EVENT = auto()

    NEWS_SEGMENT = auto()

    DOCUMENTARY = auto()

    MUSIC_VIDEO = auto()

    # ------------------------------------------------------------------
    # Broadcast Support
    # ------------------------------------------------------------------

    COMMERCIAL = auto()

    PROMO = auto()

    STATION_ID = auto()

    WEATHER_SEGMENT = auto()

    INFOMERCIAL = auto()

    # ------------------------------------------------------------------
    # Continuous Programming
    # ------------------------------------------------------------------

    AMBIENT = auto()