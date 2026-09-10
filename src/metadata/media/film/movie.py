"""
VISTOR Movie
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from metadata.media.media_item import MediaItem

if TYPE_CHECKING:
    from metadata.library.franchise import Franchise
    from metadata.library.studio import Studio


class Movie(MediaItem):
    """Represents a feature film."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        title: str,
        release_year: int = 0,
        runtime_minutes: int = 0,
        franchise: Franchise | None = None,
    ):
        super().__init__(
            id=id,
            title=title,
            release_year=release_year,
            runtime_minutes=runtime_minutes,
        )

        self.franchise = franchise

        self.production_studio: Studio | None = None

        self.distributor: Studio | None = None

        self.box_office: float | None = None

    # ------------------------------------------------------------------
    # Franchise
    # ------------------------------------------------------------------

    def get_franchise(self):
        return self.franchise

    def set_franchise(self, franchise: Franchise):
        self.franchise = franchise

    # ------------------------------------------------------------------
    # Production
    # ------------------------------------------------------------------

    def get_production_studio(self):
        return self.production_studio

    def set_production_studio(self, studio: Studio):
        self.production_studio = studio

    def get_distributor(self):
        return self.distributor

    def set_distributor(self, studio: Studio):
        self.distributor = studio

    # ------------------------------------------------------------------
    # Financial
    # ------------------------------------------------------------------

    def get_box_office(self):
        return self.box_office

    def set_box_office(self, amount: float):
        self.box_office = amount

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title
