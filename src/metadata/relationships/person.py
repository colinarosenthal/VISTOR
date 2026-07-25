"""
VISTOR Person
"""


class Person:
    """Represents an individual associated with media."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        name: str,
        stage_name: str = "",
        birth_date: str = "",
        death_date: str = "",
        country: str = "",
        biography: str = "",
    ):
        self.name = name

        self.stage_name = stage_name

        self.birth_date = birth_date
        self.death_date = death_date

        self.country = country

        self.biography = biography

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_name(self):
        """Return the person's legal name."""

        return self.name

    def get_stage_name(self):
        """Return the person's professional name."""

        return self.stage_name

    def get_display_name(self):
        """Return the preferred display name."""

        if self.stage_name:
            return self.stage_name

        return self.name

    def get_birth_date(self):
        """Return the birth date."""

        return self.birth_date

    def get_death_date(self):
        """Return the death date."""

        return self.death_date

    def get_country(self):
        """Return the person's country."""

        return self.country

    def get_biography(self):
        """Return the biography."""

        return self.biography

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def is_deceased(self):
        """Return whether the person is deceased."""

        return bool(self.death_date)

    def __str__(self):
        return self.get_display_name()