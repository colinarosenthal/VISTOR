"""
VISTOR Metadata Serializer Service

Converts VISTOR metadata objects into
storable formats.
"""

import json


class MetadataSerializer:
    """
    Serializes metadata library objects.
    """

    def __init__(self, metadata_library):

        self.library = metadata_library

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dictionary(self):
        """
        Convert metadata library to dictionary.
        """

        return {

            "media": [
                self._object_to_dictionary(item)
                for item in self.library.get_media()
            ],

            "people": [
                self._object_to_dictionary(item)
                for item in self.library.get_people()
            ],

            "networks": [
                self._object_to_dictionary(item)
                for item in self.library.get_networks()
            ],

            "studios": [
                self._object_to_dictionary(item)
                for item in self.library.get_studios()
            ],
        }

    def save_json(self, path):
        """
        Save metadata library as JSON.
        """

        with open(path, "w", encoding="utf-8") as file:

            json.dump(
                self.to_dictionary(),
                file,
                indent=4,
            )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _object_to_dictionary(self, obj):
        """
        Convert object attributes into dictionary.
        """

        return {
            key: value
            for key, value in vars(obj).items()
            if not key.startswith("_")
        }