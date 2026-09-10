"""
VISTOR Appearance

Represents a person's participation within a media item.
"""

from typing import TYPE_CHECKING

from metadata.enums.role_type import RoleType

if TYPE_CHECKING:
    from metadata.library.person import Person
    from metadata.media.media_item import MediaItem


class Appearance:
    """Represents a person's participation within a media item."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        person: "Person",
        media_item: "MediaItem",
        role: RoleType,
        credit_name: str = "",
        role_name: str = "",
        organization: str = "",
        billing_order: int = 0,
        credited: bool = True,
        notes: str = "",
    ):
        self.id = id

        self.person = person

        self.media_item = media_item

        self.role = role

        self.credit_name = credit_name

        self.role_name = role_name

        self.organization = organization

        self.billing_order = billing_order

        self.credited = credited

        self.notes = notes

    # ------------------------------------------------------------------
    # Identification
    # ------------------------------------------------------------------

    def get_id(self):
        """Return the appearance identifier."""

        return self.id

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    def get_person(self):
        """Return the associated person."""

        return self.person

    def get_media_item(self):
        """Return the associated media item."""

        return self.media_item

    # ------------------------------------------------------------------
    # Credit Information
    # ------------------------------------------------------------------

    def get_role(self):
        """Return the participation role."""

        return self.role

    def get_credit_name(self):
        """Return the displayed credit name."""

        if self.credit_name:
            return self.credit_name

        return self.person.get_display_name()

    def get_role_name(self):
        """
        Return the role-specific name.

        Examples:
        - Character name for actors
        - Stage role for musicians
        - Position or title for other appearances
        """

        return self.role_name

    def get_organization(self):
        """
        Return the associated organization.

        Examples:
        - Sports team
        - News organization
        - Musical group
        - Company
        """

        return self.organization

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

    def __str__(self):
        return f"{self.get_credit_name()} ({self.role.name})"
