"""
VISTOR Media Type
"""

from enum import Enum, auto


class MediaType(Enum):
    """Defines the primary classification of a media item."""

    # ------------------------------------------------------------------
    # Television
    # ------------------------------------------------------------------

    TV_SHOW = auto()

    NEWS_SEGMENT = auto()

    SPORTS_EVENT = auto()

    SPORTS_TALK = auto()

    WEATHER_SEGMENT = auto()

    # ------------------------------------------------------------------
    # Film
    # ------------------------------------------------------------------

    MOVIE = auto()

    DOCUMENTARY = auto()

    # ------------------------------------------------------------------
    # Music
    # ------------------------------------------------------------------

    MUSIC_VIDEO = auto()

    CONCERT = auto()

    # ------------------------------------------------------------------
    # Advertising
    # ------------------------------------------------------------------

    COMMERCIAL = auto()

    PROMO = auto()

    STATION_ID = auto()

    INFOMERCIAL = auto()

    # ------------------------------------------------------------------
    # Miscellaneous
    # ------------------------------------------------------------------

    AMBIENT = auto()