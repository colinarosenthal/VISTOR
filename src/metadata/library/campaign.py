"""
VISTOR Campaign
"""

from metadata.library.product import Product


class Campaign:
    """Represents an advertising campaign."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        name: str,
        product: Product,
        start_year: int = 0,
        end_year: int = 0,
        description: str = "",
        slogan: str = "",
    ):
        self.id = id

        self.name = name

        self.product = product

        self.start_year = start_year
        self.end_year = end_year

        self.description = description

        self.slogan = slogan

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_id(self):
        """Return the campaign identifier."""

        return self.id

    def get_name(self):
        """Return the campaign name."""

        return self.name

    def get_product(self):
        """Return the associated product."""

        return self.product

    def get_advertiser(self):
        """Return the associated advertiser."""

        return self.product.get_advertiser()

    def get_start_year(self):
        """Return the campaign start year."""

        return self.start_year

    def get_end_year(self):
        """Return the campaign end year."""

        return self.end_year

    def get_description(self):
        """Return the campaign description."""

        return self.description

    def get_slogan(self):
        """Return the campaign slogan."""

        return self.slogan

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def is_active(self, year: int):
        """Return whether the campaign was active during a given year."""

        if self.start_year == 0:
            return True

        if self.end_year == 0:
            return year >= self.start_year

        return self.start_year <= year <= self.end_year

    def __str__(self):
        return self.name