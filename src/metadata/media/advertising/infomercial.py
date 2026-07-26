"""
VISTOR Infomercial
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from metadata.media.media_item import MediaItem

if TYPE_CHECKING:
    from metadata.library.advertiser import Advertiser
    from metadata.library.product import Product
    from metadata.library.campaign import Campaign
    from metadata.relationships.appearance import Appearance


class Infomercial(MediaItem):
    """Represents a long-form paid advertising program."""

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

        self.hosts: list[Appearance] = []

        self.is_paid_programming = True

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
        """Return the promoted product."""

        return self.product

    def set_product(self, product: Product):
        """Set the promoted product."""

        self.product = product

    # ------------------------------------------------------------------
    # Campaign
    # ------------------------------------------------------------------

    def get_campaign(self):
        """Return the associated campaign."""

        return self.campaign

    def set_campaign(self, campaign: Campaign):
        """Set the associated campaign."""

        self.campaign = campaign

    # ------------------------------------------------------------------
    # Hosts
    # ------------------------------------------------------------------

    def get_hosts(self):
        """Return the infomercial hosts."""

        return self.hosts

    def add_host(self, host: Appearance):
        """Add a host appearance."""

        self.hosts.append(host)

    # ------------------------------------------------------------------
    # Programming
    # ------------------------------------------------------------------

    def is_paid_program(self):
        """Return whether this is paid programming."""

        return self.is_paid_programming

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title