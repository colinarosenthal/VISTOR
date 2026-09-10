"""
VISTOR Country

Defines standardized country metadata values used throughout VISTOR.
"""


class Country:
    """Represents a country associated with media metadata."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        name: str,
        iso_alpha2: str = "",
        iso_alpha3: str = "",
        region: str = "",
    ):
        self.name = name

        self.iso_alpha2 = iso_alpha2

        self.iso_alpha3 = iso_alpha3

        self.region = region

    # ------------------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------------------

    def get_name(self):
        """Return the country name."""

        return self.name

    def get_iso_alpha2(self):
        """Return the two-letter ISO country code."""

        return self.iso_alpha2

    def get_iso_alpha3(self):
        """Return the three-letter ISO country code."""

        return self.iso_alpha3

    def get_region(self):
        """Return the geographic region."""

        return self.region

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name
