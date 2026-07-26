"""
VISTOR Media Collection

Represents a franchise or curated grouping of related media items that share a common
creative, thematic, historical, or broadcast relationship.
"""

from typing import List

from metadata.media.media_item import MediaItem


class Collection:
    """Represents a collection of related media items."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        title: str,
        description: str = "",
        items: List[MediaItem] | None = None,
        collection_type: str = "",
    ):
        self.title = title

        self.description = description

        self.items = items if items is not None else []

        self.collection_type = collection_type

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_title(self):
        """Return collection title."""

        return self.title

    def get_description(self):
        """Return collection description."""

        return self.description

    def get_items(self):
        """Return media items in collection."""

        return self.items

    def get_collection_type(self):
        """
        Return collection type.

        Examples:
        - Franchise
        - Holiday
        - Marathon
        - Theme
        - Event
        """

        return self.collection_type

    # ------------------------------------------------------------------
    # Modification
    # ------------------------------------------------------------------

    def add_item(self, item: MediaItem):
        """Add a media item to the collection."""

        self.items.append(item)

    def remove_item(self, item: MediaItem):
        """Remove a media item from the collection."""

        if item in self.items:
            self.items.remove(item)

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def get_item_count(self):
        """Return number of items."""

        return len(self.items)

    def __str__(self):
        return self.title