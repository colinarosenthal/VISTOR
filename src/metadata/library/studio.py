"""
VISTOR Studio
"""


class Studio:
    """Represents a film or television production studio or distributor."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        name: str,
        country: str = "",
        founded_year: int = 0,
        description: str = "",
    ):
        self.id = id

        self.name = name

        self.country = country

        self.founded_year = founded_year

        self.description = description

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_country(self):
        return self.country

    def get_founded_year(self):
        return self.founded_year

    def get_description(self):
        return self.description

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name
