"""
VISTOR Product
"""

from metadata.models.relationships.advertiser import Advertiser


class Product:
    """Represents a product or service being promoted."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        name: str,
        advertiser: Advertiser,
        description: str = "",
    ):
        self.name = name

        self.advertiser = advertiser

        self.description = description

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_name(self):
        """Return the product name."""

        return self.name

    def get_advertiser(self):
        """Return the advertiser."""

        return self.advertiser

    def get_description(self):
        """Return the product description."""

        return self.description

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name