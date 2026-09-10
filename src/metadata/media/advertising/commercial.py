"""
VISTOR Commercial
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from metadata.media.media_item import MediaItem

if TYPE_CHECKING:
    from metadata.library.advertiser import Advertiser
    from metadata.library.product import Product
    from metadata.library.campaign import Campaign


class Commercial(MediaItem):
    """Represents a television commercial."""

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

        self.advertiser: Advertiser | None = None

        self.product: Product | None = None

        self.campaign: Campaign | None = None

        self.is_local = False

    # ------------------------------------------------------------------
    # Advertiser
    # ------------------------------------------------------------------

    def get_advertiser(self):
        """Return the advertiser."""

        return self.advertiser

    def set_advertiser(self, advertiser: Advertiser):
        """Set the advertiser."""

        self.advertiser = advertiser

    # ------------------------------------------------------------------
    # Product
    # ------------------------------------------------------------------

    def get_product(self):
        """Return the advertised product."""

        return self.product

    def set_product(self, product: Product):
        """Set the advertised product."""

        self.product = product

    # ------------------------------------------------------------------
    # Campaign
    # ------------------------------------------------------------------

    def get_campaign(self):
        """Return the campaign."""

        return self.campaign

    def set_campaign(self, campaign: Campaign):
        """Set the campaign."""

        self.campaign = campaign

    # ------------------------------------------------------------------
    # Broadcast
    # ------------------------------------------------------------------

    def is_local_commercial(self):
        """Return whether the commercial is local."""

        return self.is_local

    def set_local(self, local: bool):
        """Set whether the commercial is local."""

        self.is_local = local

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title
