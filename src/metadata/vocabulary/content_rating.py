"""
VISTOR Content Rating

Defines official content rating classifications.
"""

from enum import Enum, auto


class ContentRating(Enum):
    """
    Defines official media rating classifications.

    Ratings are separated by system because different countries
    and organizations use different classification standards.
    """

    # ------------------------------------------------------------------
    # Unrated
    # ------------------------------------------------------------------

    UNRATED = auto()

    UNKNOWN = auto()

    # ------------------------------------------------------------------
    # Motion Picture Association (United States)
    # ------------------------------------------------------------------

    MPAA_G = auto()

    MPAA_PG = auto()

    MPAA_PG_13 = auto()

    MPAA_R = auto()

    MPAA_NC_17 = auto()

    # ------------------------------------------------------------------
    # Television Parental Guidelines (United States)
    # ------------------------------------------------------------------

    TV_Y = auto()

    TV_Y7 = auto()

    TV_G = auto()

    TV_PG = auto()

    TV_14 = auto()

    TV_MA = auto()

    # ------------------------------------------------------------------
    # Other International Systems
    # ------------------------------------------------------------------

    BBFC_U = auto()

    BBFC_PG = auto()

    BBFC_12 = auto()

    BBFC_12A = auto()

    BBFC_15 = auto()

    BBFC_18 = auto()