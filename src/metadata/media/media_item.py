"""
VISTOR Media Item
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from metadata.relationships.media_asset import MediaAsset
    from metadata.relationships.appearance import Appearance

    from metadata.vocabulary.genre import Genre
    from metadata.vocabulary.tag import Tag
    from metadata.vocabulary.theme import Theme
    from metadata.vocabulary.network import Network
    from metadata.vocabulary.country import Country
    from metadata.vocabulary.language import Language

    from metadata.enums.media_type import MediaType
    from metadata.enums.presentation_type import PresentationType
    from metadata.enums.content_rating import ContentRating
    from metadata.enums.audience import Audience


class MediaItem:
    """
    Base class for every playable broadcast asset.

    All movies, episodes, concerts, commercials,
    sports events, documentaries, music videos,
    ambient programming, and future broadcast
    types inherit from MediaItem.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        title: str,
        release_year: int = 0,
        runtime_minutes: int = 0,
        media_type: MediaType | None = None,
        presentation_type: PresentationType | None = None,
    ):
        self.id = id

        self.title = title

        self.description: str = ""

        self.release_year = release_year

        self.runtime_minutes = runtime_minutes

        self.media_type = media_type

        self.presentation_type = presentation_type

        self.content_rating: ContentRating | None = None
        self.audience: Audience | None = None

        self.original_network: Network | None = None

        self.production_country: Country | None = None

        self.languages: list[Language] = []

        self.genres: list[Genre] = []
        self.tags: list[Tag] = []
        self.themes: list[Theme] = []

        self.appearances: list[Appearance] = []

        self.media_assets: list[MediaAsset] = []

    # ------------------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------------------

    def get_id(self):
        """Return the media identifier."""

        return self.id

    def get_title(self):
        """Return the media title."""

        return self.title

    def get_description(self):
        """Return the description."""

        return self.description

    def set_description(self, description: str):
        """Set the description."""

        self.description = description

    def get_release_year(self):
        """Return the release year."""

        return self.release_year

    def get_runtime_minutes(self):
        """Return the runtime."""

        return self.runtime_minutes

    def set_runtime_minutes(self, runtime: int):
        """Set the runtime."""

        self.runtime_minutes = runtime

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    def get_media_type(self):
        """Return the media type."""

        return self.media_type

    def get_presentation_type(self):
        """Return the presentation type."""

        return self.presentation_type

    def set_content_rating(self, rating: ContentRating):
        """Set the content rating."""

        self.content_rating = rating

    def get_content_rating(self):
        """Return the content rating."""

        return self.content_rating

    def set_audience(self, audience: Audience):
        """Set the target audience."""

        self.audience = audience

    def get_audience(self):
        """Return the target audience."""

        return self.audience

    # ------------------------------------------------------------------
    # Broadcast Information
    # ------------------------------------------------------------------

    def set_original_network(self, network: Network):
        """Set the original broadcast network."""

        self.original_network = network

    def get_original_network(self):
        """Return the original broadcast network."""

        return self.original_network

    def set_production_country(self, country: Country):
        """Set the production country."""

        self.production_country = country

    def get_production_country(self):
        """Return the production country."""

        return self.production_country

    # ------------------------------------------------------------------
    # Languages
    # ------------------------------------------------------------------

    def add_language(self, language: Language):
        """Add an available language."""

        if language not in self.languages:
            self.languages.append(language)

    def get_languages(self):
        """Return all available languages."""

        return self.languages

    # ------------------------------------------------------------------
    # Genres
    # ------------------------------------------------------------------

    def add_genre(self, genre: Genre):
        """Add a genre."""

        if genre not in self.genres:
            self.genres.append(genre)

    def get_genres(self):
        """Return all genres."""

        return self.genres

    # ------------------------------------------------------------------
    # Tags
    # ------------------------------------------------------------------

    def add_tag(self, tag: Tag):
        """Add a tag."""

        if tag not in self.tags:
            self.tags.append(tag)

    def get_tags(self):
        """Return all tags."""

        return self.tags

    # ------------------------------------------------------------------
    # Themes
    # ------------------------------------------------------------------

    def add_theme(self, theme: Theme):
        """Add a theme."""

        if theme not in self.themes:
            self.themes.append(theme)

    def get_themes(self):
        """Return all themes."""

        return self.themes

    # ------------------------------------------------------------------
    # Appearances
    # ------------------------------------------------------------------

    def add_appearance(self, appearance: Appearance):
        """Add an appearance."""

        self.appearances.append(appearance)

    def get_appearances(self):
        """Return all appearances."""

        return self.appearances

    # ------------------------------------------------------------------
    # Media Assets
    # ------------------------------------------------------------------

    def add_media_asset(self, asset: MediaAsset):
        """Add a media asset."""

        self.media_assets.append(asset)

    def get_media_assets(self):
        """Return all media assets."""

        return self.media_assets

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title