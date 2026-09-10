"""
VISTOR Product
"""

from metadata.library.advertiser import Advertiser


class Product:
    """Represents a reusable product or service."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        name: str,
        advertiser: Advertiser,
        description: str = "",
        category: str = "",
        release_year: int = 0,
    ):
        self.id = id

        self.name = name

        self.advertiser = advertiser

        self.description = description

        self.category = category

        self.release_year = release_year

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_id(self):
        """Return the product identifier."""

        return self.id

    def get_name(self):
        """Return the product name."""

        return self.name

    def get_advertiser(self):
        """Return the advertiser."""

        return self.advertiser

    def get_description(self):
        """Return the product description."""

        return self.description

    def get_category(self):
        """Return the product category."""

        return self.category

    def get_release_year(self):
        """Return the release year."""

        return self.release_year

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name
