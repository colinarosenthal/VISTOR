"""
VISTOR Campaign
"""

from metadata.models.relationships.product import Product


class Campaign:
    """Represents an advertising campaign."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        name: str,
        product: Product,
        start_year: int = 0,
        end_year: int = 0,
        description: str = "",
    ):
        self.name = name

        self.product = product

        self.start_year = start_year
        self.end_year = end_year

        self.description = description

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_name(self):
        """Return the campaign name."""

        return self.name

    def get_product(self):
        """Return the associated product."""

        return self.product

    def get_start_year(self):
        """Return the campaign start year."""

        return self.start_year

    def get_end_year(self):
        """Return the campaign end year."""

        return self.end_year

    def get_description(self):
        """Return the campaign description."""

        return self.description

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def is_active_in_year(self, year: int):
        """Return whether the campaign was active during a given year."""

        if self.start_year == 0:
            return False

        if self.end_year == 0:
            return year >= self.start_year

        return self.start_year <= year <= self.end_year

    def __str__(self):
        return self.name