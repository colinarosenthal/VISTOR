"""
VISTOR Promo
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from metadata.media.media_item import MediaItem

if TYPE_CHECKING:
    from metadata.library.network import Network
    from metadata.library.franchise import Franchise


class Promo(MediaItem):
    """Represents a television network promotional advertisement."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        title: str,
        release_year: int = 0,
        runtime_minutes: int = 30,
    ):
        super().__init__(
            id=id,
            title=title,
            release_year=release_year,
            runtime_minutes=runtime_minutes,
        )

        self.network: Network | None = None

        self.promoted_franchise: Franchise | None = None

        self.promotion_text: str = ""

    # ------------------------------------------------------------------
    # Network
    # ------------------------------------------------------------------

    def get_network(self):
        """Return the promoting network."""

        return self.network

    def set_network(self, network: Network):
        """Set the promoting network."""

        self.network = network

    # ------------------------------------------------------------------
    # Promoted Content
    # ------------------------------------------------------------------

    def get_promoted_franchise(self):
        """Return the promoted franchise."""

        return self.promoted_franchise

    def set_promoted_franchise(self, franchise: Franchise):
        """Set the promoted franchise."""

        self.promoted_franchise = franchise

    # ------------------------------------------------------------------
    # Promotion
    # ------------------------------------------------------------------

    def get_promotion_text(self):
        """Return the promotional message."""

        return self.promotion_text

    def set_promotion_text(self, text: str):
        """Set the promotional message."""

        self.promotion_text = text

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title