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
        self.franchises = []  
        self.series = []  
        self.seasons = []
  
        # Vocabulary  
        self.genres = []  
        self.tags = []  
        self.themes = []  
        self.countries = []  
        self.languages = []  
        self.content_ratings = []  
        self.music_genres = []  
  
        # Library entities referenced by media  
        self.franchises = []  
        self.series = []  
        self.seasons = []  
        self.advertisers = []  
        self.products = []  
        self.campaigns = []  
  
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

    # Vocabulary additions  
    def add_content_rating(self, rating):  
        self.content_ratings.append(rating)  
  
    def get_content_ratings(self):  
        return self.content_ratings  
  
    def add_music_genre(self, genre):  
        self.music_genres.append(genre)  
  
    def get_music_genres(self):  
        return self.music_genres  
  
    # Library entities  
    def add_franchise(self, franchise):  
        self.franchises.append(franchise)  
  
    def get_franchises(self):  
        return self.franchises  
  
    def add_series(self, series):  
        self.series.append(series)  
  
    def get_series(self):  
        return self.series  
  
    def add_season(self, season):  
        self.seasons.append(season)  
  
    def get_seasons(self):  
        return self.seasons  
  
    def add_advertiser(self, advertiser):  
        self.advertisers.append(advertiser)  
  
    def get_advertisers(self):  
        return self.advertisers  
  
    def add_product(self, product):  
        self.products.append(product)  
  
    def get_products(self):  
        return self.products  
  
    def add_campaign(self, campaign):  
        self.campaigns.append(campaign)  
  
    def get_campaigns(self):  
        return self.campaigns  
  
    # Convenience media getters (filter self.media by type)  
    def get_movies(self):  
        from metadata.media.film.movie import Movie  
        return [m for m in self.media if isinstance(m, Movie)]  
  
    def get_episodes(self):  
        from metadata.media.television.episode import Episode  
        return [m for m in self.media if isinstance(m, Episode)]  
  
    def get_music_videos(self):  
        from metadata.media.music.music_video import MusicVideo  
        return [m for m in self.media if isinstance(m, MusicVideo)]  
  
    def get_commercials(self):  
        from metadata.media.advertising.commercial import Commercial  
        return [m for m in self.media if isinstance(m, Commercial)]  
  
    def get_total_media_count(self):  
        return len(self.media)

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

    def add_franchise(self, franchise):  
        """Add franchise."""  
  
        self.franchises.append(franchise)  
  
    def get_franchises(self):  
        return self.franchises  
  
  
    def add_series(self, series):  
        """Add series."""  
  
        self.series.append(series)  
  
    def get_series(self):  
        return self.series  
  
  
    def add_season(self, season):  
        """Add season."""  
  
        self.seasons.append(season)  
  
    def get_seasons(self):  
        return self.seasons
    
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