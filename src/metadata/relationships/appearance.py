"""
VISTOR Appearance
"""

from metadata.enums.role_type import RoleType
from metadata.library.person import Person


class Appearance:
    """Represents a person's participation in a media item."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        person: Person,
        role: RoleType,
        display_name: str = "",
        character_name: str = "",
        affiliation: str = "",
        billing_order: int = 0,
        credited: bool = True,
        notes: str = "",
    ):
        self.person = person

        self.role = role

        self.display_name = display_name

        self.character_name = character_name

        self.affiliation = affiliation

        self.billing_order = billing_order

        self.credited = credited

        self.notes = notes

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_person(self):
        """Return the associated person."""

        return self.person

    def get_role(self):
        """Return the participation role."""

        return self.role

    def get_display_name(self):
        """Return the displayed credit name."""

        if self.display_name:
            return self.display_name

        return self.person.get_display_name()

    def get_character_name(self):
        """Return the portrayed character."""

        return self.character_name

    def get_affiliation(self):
        """Return the associated affiliation."""

        return self.affiliation

    def get_billing_order(self):
        """Return billing order."""

        return self.billing_order

    def is_credited(self):
        """Return whether this appearance is credited."""

        return self.credited

    def get_notes(self):
        """Return appearance notes."""

        return self.notes

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def has_character(self):
        """Return whether this appearance portrays a character."""

        return bool(self.character_name)

    def has_affiliation(self):
        """Return whether an affiliation exists."""

        return bool(self.affiliation)

    def __str__(self):
        return f"{self.get_display_name()} ({self.role.name})"