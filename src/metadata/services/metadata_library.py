"""
VISTOR Metadata Library Service

Central container and manager for all VISTOR metadata.
"""


class MetadataLibrary:
    """
    Stores and manages loaded metadata objects.

    This service acts as the central metadata database
    used by loading, validation, searching, and serialization.
    """

    def __init__(self):

        # Media objects
        self.media = []

        # People and organizations
        self.people = []
        self.networks = []
        self.studios = []

        # Vocabulary
        self.genres = []
        self.tags = []
        self.themes = []
        self.countries = []
        self.languages = []

        # Relationships
        self.relationships = []

    # ------------------------------------------------------------------
    # Media
    # ------------------------------------------------------------------

    def add_media(self, item):
        """Add media metadata object."""

        self.media.append(item)

    def get_media(self):
        """Return all media objects."""

        return self.media

    # ------------------------------------------------------------------
    # People
    # ------------------------------------------------------------------

    def add_person(self, person):
        """Add person."""

        self.people.append(person)

    def get_people(self):
        """Return people."""

        return self.people

    # ------------------------------------------------------------------
    # Organizations
    # ------------------------------------------------------------------

    def add_network(self, network):
        """Add network."""

        self.networks.append(network)

    def get_networks(self):
        return self.networks


    def add_studio(self, studio):
        """Add studio."""

        self.studios.append(studio)

    def get_studios(self):
        return self.studios

    # ------------------------------------------------------------------
    # Vocabulary
    # ------------------------------------------------------------------

    def add_genre(self, genre):

        self.genres.append(genre)

    def get_genres(self):

        return self.genres


    def add_tag(self, tag):

        self.tags.append(tag)

    def get_tags(self):

        return self.tags


    def add_theme(self, theme):

        self.themes.append(theme)

    def get_themes(self):

        return self.themes


    def add_country(self, country):

        self.countries.append(country)

    def get_countries(self):

        return self.countries


    def add_language(self, language):

        self.languages.append(language)

    def get_languages(self):

        return self.languages

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    def add_relationship(self, relationship):

        self.relationships.append(relationship)

    def get_relationships(self):

        return self.relationships

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def get_total_count(self):
        """
        Return total metadata objects stored.
        """

        return (
            len(self.media)
            + len(self.people)
            + len(self.networks)
            + len(self.studios)
            + len(self.genres)
            + len(self.tags)
            + len(self.themes)
            + len(self.countries)
            + len(self.languages)
            + len(self.relationships)
        )

    def __str__(self):

        return (
            f"Metadata Library "
            f"({self.get_total_count()} objects)"
        )