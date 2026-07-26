"""
VISTOR Station ID
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from metadata.media.media_item import MediaItem

if TYPE_CHECKING:
    from metadata.library.network import Network


class StationID(MediaItem):
    """Represents a television station or network identification."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        title: str,
        release_year: int = 0,
        runtime_minutes: int = 10,
    ):
        super().__init__(
            id=id,
            title=title,
            release_year=release_year,
            runtime_minutes=runtime_minutes,
        )

        self.network: Network | None = None

        self.branding_text: str = ""

    # ------------------------------------------------------------------
    # Network
    # ------------------------------------------------------------------

    def get_network(self):
        """Return the associated network."""

        return self.network

    def set_network(self, network: Network):
        """Set the associated network."""

        self.network = network

    # ------------------------------------------------------------------
    # Branding
    # ------------------------------------------------------------------

    def get_branding_text(self):
        """Return the branding or station identification text."""

        return self.branding_text

    def set_branding_text(self, text: str):
        """Set the branding or station identification text."""

        self.branding_text = text

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title