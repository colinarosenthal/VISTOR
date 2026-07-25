"""
VISTOR Network
"""


class Network:
    """Represents a television network or broadcast provider."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        name: str,
        abbreviation: str = "",
        description: str = "",
    ):
        self.id = id

        self.name = name

        self.abbreviation = abbreviation

        self.description = description

    # ------------------------------------------------------------------
    # Identification
    # ------------------------------------------------------------------

    def get_id(self):
        """Return the network identifier."""

        return self.id

    # ------------------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------------------

    def get_name(self):
        """Return the network name."""

        return self.name

    def get_abbreviation(self):
        """Return the network abbreviation."""

        return self.abbreviation

    def set_abbreviation(self, abbreviation: str):
        """Set the network abbreviation."""

        self.abbreviation = abbreviation

    def get_description(self):
        """Return the network description."""

        return self.description

    def set_description(self, description: str):
        """Set the network description."""

        self.description = description

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name