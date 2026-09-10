"""
VISTOR Language

Defines standardized language metadata values used throughout VISTOR.
"""


class Language:
    """Represents a language associated with media metadata."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        name: str,
        iso_639_1: str = "",
        iso_639_2: str = "",
        native_name: str = "",
    ):
        self.name = name

        self.iso_639_1 = iso_639_1

        self.iso_639_2 = iso_639_2

        self.native_name = native_name

    # ------------------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------------------

    def get_name(self):
        """Return the language name."""

        return self.name

    def get_native_name(self):
        """Return the native language name."""

        return self.native_name

    def get_iso_639_1(self):
        """Return the ISO 639-1 language code."""

        return self.iso_639_1

    def get_iso_639_2(self):
        """Return the ISO 639-2 language code."""

        return self.iso_639_2

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name
