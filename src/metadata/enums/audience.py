"""
VISTOR Audience

Defines the intended target audience for media content.
"""

from enum import Enum, auto


class Audience(Enum):
    """Defines the general intended audience of a media item."""

    # ------------------------------------------------------------------
    # General Audience
    # ------------------------------------------------------------------

    GENERAL = auto()

    FAMILY = auto()

    ALL_AGES = auto()

    # ------------------------------------------------------------------
    # Age Demographics
    # ------------------------------------------------------------------

    CHILDREN = auto()

    TEEN = auto()

    YOUNG_ADULT = auto()

    ADULT = auto()

    SENIOR = auto()