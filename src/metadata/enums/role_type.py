"""
VISTOR Role Type
"""

from enum import Enum, auto


class RoleType(Enum):
    """Defines how a person participates in a media item."""

    # ------------------------------------------------------------------
    # Performance
    # ------------------------------------------------------------------

    ACTOR = auto()
    VOICE_ACTOR = auto()
    STUNT_PERFORMER = auto()

    # ------------------------------------------------------------------
    # Production
    # ------------------------------------------------------------------

    DIRECTOR = auto()
    PRODUCER = auto()
    EXECUTIVE_PRODUCER = auto()
    WRITER = auto()
    SCREENWRITER = auto()
    COMPOSER = auto()
    CONDUCTOR = auto()
    CINEMATOGRAPHER = auto()
    EDITOR = auto()

    # ------------------------------------------------------------------
    # Broadcast
    # ------------------------------------------------------------------

    HOST = auto()
    CO_HOST = auto()
    ANNOUNCER = auto()
    COMMENTATOR = auto()
    REPORTER = auto()
    ANCHOR = auto()
    WEATHERCASTER = auto()
    NARRATOR = auto()

    # ------------------------------------------------------------------
    # Sports
    # ------------------------------------------------------------------

    ATHLETE = auto()
    COACH = auto()
    REFEREE = auto()

    # ------------------------------------------------------------------
    # Commercial
    # ------------------------------------------------------------------

    SPOKESPERSON = auto()

    # ------------------------------------------------------------------
    # Music
    # ------------------------------------------------------------------

    SINGER = auto()
    MUSICIAN = auto()
    BAND = auto()

    # ------------------------------------------------------------------
    # Miscellaneous
    # ------------------------------------------------------------------

    GUEST = auto()
    CONTESTANT = auto()
    INTERVIEWEE = auto()
