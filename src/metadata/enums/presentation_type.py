"""
VISTOR Presentation Type

Defines how a media item is presented to the viewer.
"""

from enum import Enum, auto


class PresentationType(Enum):
    """Defines the presentation format of a media item."""

    # ------------------------------------------------------------------
    # Language Presentation
    # ------------------------------------------------------------------

    ORIGINAL_AUDIO = auto()

    DUBBED = auto()

    SUBTITLED = auto()

    MULTILINGUAL = auto()

    # ------------------------------------------------------------------
    # Broadcast Presentation
    # ------------------------------------------------------------------

    BROADCAST = auto()

    BROADCAST_RECORDING = auto()

    TELEVISION_EDIT = auto()

    SYNDICATED_VERSION = auto()

    # ------------------------------------------------------------------
    # Release Presentation
    # ------------------------------------------------------------------

    THEATRICAL = auto()

    HOME_VIDEO = auto()

    STREAMING_RELEASE = auto()

    # ------------------------------------------------------------------
    # Special Formats
    # ------------------------------------------------------------------

    DIRECTORS_CUT = auto()

    EXTENDED_CUT = auto()

    CENSORED = auto()