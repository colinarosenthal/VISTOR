"""
VISTOR Metadata Loader

Responsible for loading metadata from disk and constructing
the VISTOR metadata library.

The MetadataLoader discovers metadata files, creates metadata
objects, resolves relationships between objects, and returns
a fully populated MetadataLibrary instance.
"""

import json

from pathlib import Path

from metadata.services.metadata_library import MetadataLibrary

from metadata.vocabulary.genre import Genre
from metadata.vocabulary.country import Country
from metadata.vocabulary.theme import Theme
from metadata.vocabulary.tag import Tag


class MetadataLoader:
    """Loads VISTOR metadata into memory."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Public Interface
    # ------------------------------------------------------------------

    def load(self, metadata_path: Path) -> MetadataLibrary:
        """
        Load the complete metadata library.

        Parameters
        ----------
        metadata_path
            Root metadata directory.

        Returns
        -------
        MetadataLibrary
            Fully populated metadata library.
        """

        library = MetadataLibrary()

        self._load_vocabulary(library, metadata_path)

        self._load_library(library, metadata_path)
        self._load_people(library, metadata_path)
        self._load_series(library, metadata_path)
        self._load_seasons(library, metadata_path)
        self._load_media(library, metadata_path)

        self._resolve_relationships(library)

        return library

    # ------------------------------------------------------------------
    # Vocabulary Loading
    # ------------------------------------------------------------------

    def _load_vocabulary(
        self,
        library: MetadataLibrary,
        metadata_path: Path,
    ):
        """
        Load vocabulary metadata.
        """

        self._load_genres(library, metadata_path)
        self._load_countries(library, metadata_path)
        self._load_themes(library, metadata_path)
        self._load_tags(library, metadata_path)


    def _load_genres(
        self,
        library: MetadataLibrary,
        metadata_path: Path,
    ):
        """
        Load genre metadata.
        """

        path = metadata_path / "genres.json"

        if not path.exists():
            return

        with open(path, "r", encoding="utf-8") as file:

            data = json.load(file)

        for item in data:

            genre = Genre(
                name=item["name"],
                description=item.get("description", ""),
            )

            library.add_genre(genre)


    def _load_countries(
        self,
        library: MetadataLibrary,
        metadata_path: Path,
    ):
        """
        Load country metadata.
        """

        path = metadata_path / "countries.json"

        if not path.exists():
            return

        with open(path, "r", encoding="utf-8") as file:

            data = json.load(file)

        for item in data:

            country = Country(
                name=item["name"],
                iso_alpha2=item.get("iso_alpha2", ""),
                iso_alpha3=item.get("iso_alpha3", ""),
                region=item.get("region", ""),
            )

            library.add_country(country)


    def _load_themes(
        self,
        library: MetadataLibrary,
        metadata_path: Path,
    ):
        """
        Load theme metadata.
        """

        path = metadata_path / "themes.json"

        if not path.exists():
            return

        with open(path, "r", encoding="utf-8") as file:

            data = json.load(file)

        for item in data:

            theme = Theme(
                name=item["name"],
                description=item.get("description", ""),
            )

            library.add_theme(theme)


    def _load_tags(
        self,
        library: MetadataLibrary,
        metadata_path: Path,
    ):
        """
        Load tag metadata.
        """

        path = metadata_path / "tags.json"

        if not path.exists():
            return

        with open(path, "r", encoding="utf-8") as file:

            data = json.load(file)

        for item in data:

            tag = Tag(
                name=item["name"],
                description=item.get("description", ""),
                category=item.get("category", ""),
            )

            library.add_tag(tag)

    # ------------------------------------------------------------------
    # Loading Stages
    # ------------------------------------------------------------------

    def _load_library(
        self,
        library: MetadataLibrary,
        metadata_path: Path,
    ):
        """Load library-level metadata."""
        pass


    def _load_people(
        self,
        library: MetadataLibrary,
        metadata_path: Path,
    ):
        """Load people metadata."""
        pass


    def _load_series(
        self,
        library: MetadataLibrary,
        metadata_path: Path,
    ):
        """Load series metadata."""
        pass


    def _load_seasons(
        self,
        library: MetadataLibrary,
        metadata_path: Path,
    ):
        """Load season metadata."""
        pass


    def _load_media(
        self,
        library: MetadataLibrary,
        metadata_path: Path,
    ):
        """Load all media objects."""
        pass


    def _resolve_relationships(
        self,
        library: MetadataLibrary,
    ):
        """
        Resolve object references after loading.

        Examples:
        - Episode → Season
        - Season → Series
        - Appearance → Person
        """

        pass