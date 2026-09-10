"""
VISTOR Commercial Type

Defines the classification of broadcast advertising and promotional material.
"""

from enum import Enum, auto


class CommercialType(Enum):
    """Defines the purpose and format of a broadcast advertisement."""

    # ------------------------------------------------------------------
    # Traditional Advertising
    # ------------------------------------------------------------------

    COMMERCIAL = auto()

    LOCAL_COMMERCIAL = auto()

    NATIONAL_COMMERCIAL = auto()

    POLITICAL_ADVERTISEMENT = auto()

    # ------------------------------------------------------------------
    # Promotional Material
    # ------------------------------------------------------------------

    NETWORK_PROMO = auto()

    CABLE_PROVIDER_PROMO = auto()

    PROGRAM_PROMO = auto()

    CROSS_CHANNEL_PROMO = auto()

    # ------------------------------------------------------------------
    # Extended Advertising Formats
    # ------------------------------------------------------------------

    INFOMERCIAL = auto()

    SPONSORED_SEGMENT = auto()

    PRODUCT_PLACEMENT = auto()

    # ------------------------------------------------------------------
    # Broadcast Identity
    # ------------------------------------------------------------------

    STATION_ID = auto()

    LEGAL_ID = auto()
