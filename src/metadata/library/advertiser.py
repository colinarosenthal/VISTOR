"""
VISTOR Advertiser
"""


class Advertiser:
    """Represents a company or organization that advertises."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        name: str,
        description: str = "",
        country: str = "",
    ):
        self.name = name

        self.description = description

        self.country = country

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_name(self):
        """Return the advertiser name."""

        return self.name

    def get_description(self):
        """Return the advertiser description."""

        return self.description

    def get_country(self):
        """Return the advertiser's country."""

        return self.country

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name