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
        id: str,
        name: str,
        stage_name: str = "",
        aliases: list[str] | None = None,
        birth_date: str = "",
        death_date: str = "",
        nationality: str = "",
        biography: str = "",
    ):
        self.id = id

        self.name = name

        self.stage_name = stage_name

        self.aliases = aliases or []

        self.birth_date = birth_date
        self.death_date = death_date

        self.nationality = nationality

        self.biography = biography

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_id(self):
        """Return the unique person identifier."""

        return self.id

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

    def get_aliases(self):
        """Return all known aliases."""

        return self.aliases

    def get_birth_date(self):
        """Return the birth date."""

        return self.birth_date

    def get_death_date(self):
        """Return the death date."""

        return self.death_date

    def get_nationality(self):
        """Return the person's nationality."""

        return self.nationality

    def get_biography(self):
        """Return the biography."""

        return self.biography

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def is_deceased(self):
        """Return whether the person is deceased."""

        return bool(self.death_date)

    def has_stage_name(self):
        """Return whether a stage name exists."""

        return bool(self.stage_name)

    def has_aliases(self):
        """Return whether aliases exist."""

        return len(self.aliases) > 0

    def __str__(self):
        return self.get_display_name()
