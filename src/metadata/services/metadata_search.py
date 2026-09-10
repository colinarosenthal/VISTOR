"""
VISTOR Metadata Search Service

Provides searching and lookup functions for
the VISTOR metadata library.
"""


class MetadataSearch:
    """
    Searches metadata stored inside a MetadataLibrary.
    """

    def __init__(self, metadata_library):

        self.library = metadata_library

    # ------------------------------------------------------------------
    # Generic Search
    # ------------------------------------------------------------------

    def find_by_id(self, object_id):
        """
        Find metadata object by ID.
        """

        collections = [
            self.library.get_media(),
            self.library.get_people(),
            self.library.get_networks(),
            self.library.get_studios(),
            self.library.get_relationships(),
        ]

        for collection in collections:

            for item in collection:

                if getattr(item, "id", None) == object_id:

                    return item

        return None

    # ------------------------------------------------------------------
    # People
    # ------------------------------------------------------------------

    def find_person(self, name):
        """
        Find people by name.
        """

        results = []

        for person in self.library.get_people():

            if person.name.lower() == name.lower():

                results.append(person)

        return results

    # ------------------------------------------------------------------
    # Media
    # ------------------------------------------------------------------

    def find_media(self, title):
        """
        Find media by title.
        """

        results = []

        for item in self.library.get_media():

            if item.title.lower() == title.lower():

                results.append(item)

        return results
