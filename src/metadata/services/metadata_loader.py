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
  
# Vocabulary  
from metadata.vocabulary.genre import Genre  
from metadata.vocabulary.country import Country  
from metadata.vocabulary.theme import Theme  
from metadata.vocabulary.tag import Tag  
from metadata.vocabulary.language import Language  
from metadata.vocabulary.content_rating import ContentRating  
  
# Library entities  
from metadata.library.network import Network  
from metadata.library.studio import Studio  
from metadata.library.person import Person  
from metadata.library.franchise import Franchise  
from metadata.library.series import Series  
from metadata.library.season import Season  
from metadata.library.advertiser import Advertiser  
from metadata.library.product import Product  
from metadata.library.campaign import Campaign  
  
# Media types  
from metadata.media.film.movie import Movie  
from metadata.media.television.episode import Episode  
from metadata.media.advertising.commercial import Commercial  
from metadata.media.music.music_video import MusicVideo


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

    def _load_library(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load library-level metadata."""  
  
        self._load_networks(library, metadata_path)  
        self._load_studios(library, metadata_path)

    def _load_networks(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """  
        Load network metadata.  
        """  
  
        path = metadata_path / "networks.json"  
  
        if not path.exists():  
            return  
  
        with open(path, "r", encoding="utf-8") as file:  
  
            data = json.load(file)  
  
        for item in data:  
  
            network = Network(  
                id=item["id"],  
                name=item["name"],  
                abbreviation=item.get("abbreviation", ""),  
                description=item.get("description", ""),  
            )  
  
            library.add_network(network)  
  
  
    def _load_studios(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """  
        Load studio metadata.  
        """  
  
        path = metadata_path / "studios.json"  
  
        if not path.exists():  
            return  
  
        with open(path, "r", encoding="utf-8") as file:  
  
            data = json.load(file)  
  
        for item in data:  
  
            studio = Studio(  
                id=item["id"],  
                name=item["name"],  
                country=item.get("country", ""),  
                founded_year=item.get("founded_year", 0),  
                description=item.get("description", ""),  
            )  
  
            library.add_studio(studio)

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
        self._load_languages(library, metadata_path)


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

    def _load_languages(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """  
        Load language metadata.  
        """  
  
        path = metadata_path / "languages.json"  
  
        if not path.exists():  
            return  
  
        with open(path, "r", encoding="utf-8") as file:  
  
            data = json.load(file)  
  
        for item in data:  
  
            language = Language(  
                name=item["name"],  
                iso_639_1=item.get("iso_639_1", ""),  
                iso_639_2=item.get("iso_639_2", ""),  
                native_name=item.get("native_name", ""),  
            )  
  
            library.add_language(language)

    # ------------------------------------------------------------------
    # Loading Stages
    # ------------------------------------------------------------------

    def _load_people(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load people metadata."""  
  
        path = metadata_path / "people.json"  
  
        if not path.exists():  
            return  
  
        with open(path, "r", encoding="utf-8") as file:  
            data = json.load(file)  
  
        for item in data:  
  
            person = Person(  
                id=item["id"],  
                name=item["name"],  
                stage_name=item.get("stage_name", ""),  
                aliases=item.get("aliases", []),  
                birth_date=item.get("birth_date", ""),  
                death_date=item.get("death_date", ""),  
                nationality=item.get("nationality", ""),  
                biography=item.get("biography", ""),  
            )  
  
            library.add_person(person)  
  
  
    def _load_series(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load series metadata."""  
  
        # Franchises first, so series can resolve their franchise ref.  
        self._load_franchises(library, metadata_path)  
  
        path = metadata_path / "series.json"  
  
        if not path.exists():  
            return  
  
        with open(path, "r", encoding="utf-8") as file:  
            data = json.load(file)  
  
        franchises = {f.get_id(): f for f in library.get_franchises()}  
  
        for item in data:  
  
            franchise = None  
            franchise_id = item.get("franchise")  
  
            if franchise_id is not None:  
                franchise = franchises.get(franchise_id)  
  
            series = Series(  
                id=item["id"],  
                title=item["title"],  
                franchise=franchise,  
                description=item.get("description", ""),  
                premiere_year=item.get("premiere_year", 0),  
                finale_year=item.get("finale_year", 0),  
            )  
  
            library.add_series(series)  
  
  
    def _load_franchises(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load franchise metadata."""  
  
        path = metadata_path / "franchises.json"  
  
        if not path.exists():  
            return  
  
        with open(path, "r", encoding="utf-8") as file:  
            data = json.load(file)  
  
        for item in data:  
  
            franchise = Franchise(  
                id=item["id"],  
                name=item["name"],  
                description=item.get("description", ""),  
            )  
  
            library.add_franchise(franchise)  
  
  
    def _load_seasons(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load season metadata."""  
  
        path = metadata_path / "seasons.json"  
  
        if not path.exists():  
            return  
  
        with open(path, "r", encoding="utf-8") as file:  
            data = json.load(file)  
  
        series_lookup = {s.get_id(): s for s in library.get_series()}  
  
        for item in data:  
  
            series = series_lookup.get(item.get("series"))  
  
            if series is None:  
                # Season requires a series; skip if its parent  
                # was not serialized.  
                continue  
  
            season = Season(  
                id=item["id"],  
                series=series,  
                season_number=item.get("season_number", 0),  
                title=item.get("title", ""),  
                description=item.get("description", ""),  
                premiere_year=item.get("premiere_year", 0),  
            )  
  
            library.add_season(season)  
  
  
    def _load_media(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load all media objects."""  
  
        path = metadata_path / "media.json"  
  
        if not path.exists():  
            return  
  
        with open(path, "r", encoding="utf-8") as file:  
            data = json.load(file)  
  
        seasons = {s.get_id(): s for s in library.get_seasons()}  
  
        for item in data:  
  
            media_type = item.get("type")  
  
            if media_type == "Movie":  
                obj = Movie(  
                    id=item["id"],  
                    title=item["title"],  
                    release_year=item.get("release_year", 0),  
                    runtime_minutes=item.get("runtime_minutes", 0),  
                )  
            elif media_type == "Commercial":  
                obj = Commercial(  
                    id=item["id"],  
                    title=item["title"],  
                    release_year=item.get("release_year", 0),  
                    runtime_minutes=item.get("runtime_minutes", 30),  
                )  
            elif media_type == "MusicVideo":  
                obj = MusicVideo(  
                    id=item["id"],  
                    title=item["title"],  
                    release_year=item.get("release_year", 0),  
                    runtime_minutes=item.get("runtime_minutes", 0),  
                )  
            elif media_type == "Episode":  
                season = seasons.get(item.get("season"))  
  
                if season is None:  
                    # Parent season not available; cannot reconstruct.  
                    continue  
  
                obj = Episode(  
                    id=item["id"],  
                    title=item["title"],  
                    season=season,  
                    episode_number=item.get("episode_number", 0),  
                    release_year=item.get("release_year", 0),  
                    runtime_minutes=item.get("runtime_minutes", 0),  
                )  
            else:  
                continue  
  
            obj.description = item.get("description", "")  
  
            # Stash flattened refs for _resolve_relationships.  
            obj._pending = item  
  
            library.add_media(obj)  
  
  
    def _resolve_relationships(  
        self,  
        library: MetadataLibrary,  
    ):  
        """  
        Resolve object references after loading.  
  
        Re-links the flattened id/name references stashed on each  
        media object during _load_media back into shared instances.  
        """  
  
        # id-keyed lookups  
        networks = {n.get_id(): n for n in library.get_networks()}  
        studios = {s.get_id(): s for s in library.get_studios()}  
  
        # name-keyed lookups  
        genres = {g.get_name(): g for g in library.get_genres()}  
        themes = {t.get_name(): t for t in library.get_themes()}  
        tags = {t.get_name(): t for t in library.get_tags()}  
        countries = {c.get_name(): c for c in library.get_countries()}  
        languages = {l.get_name(): l for l in library.get_languages()}  
  
        for obj in library.get_media():  
  
            pending = getattr(obj, "_pending", None)  
  
            if not pending:  
                continue  
  
            network_id = pending.get("original_network")  
            if network_id is not None:  
                obj.original_network = networks.get(network_id)  
  
            country_name = pending.get("production_country")  
            if country_name is not None:  
                obj.production_country = countries.get(country_name)  
  
            obj.genres = [  
                genres[name]  
                for name in pending.get("genres", [])  
                if name in genres  
            ]  
  
            obj.themes = [  
                themes[name]  
                for name in pending.get("themes", [])  
                if name in themes  
            ]  
  
            obj.tags = [  
                tags[name]  
                for name in pending.get("tags", [])  
                if name in tags  
            ]  
  
            obj.languages = [  
                languages[name]  
                for name in pending.get("languages", [])  
                if name in languages  
            ]  
  
            # Clean up the temporary payload.  
            del obj._pending

    def _resolve_relationships(  
        self,  
        library: MetadataLibrary,  
    ):  
        """Resolve object references after loading."""  
  
        genres = {g.get_name(): g for g in library.get_genres()}  
        tags = {t.get_name(): t for t in library.get_tags()}  
        themes = {t.get_name(): t for t in library.get_themes()}  
        countries = {c.get_name(): c for c in library.get_countries()}  
        languages = {l.get_name(): l for l in library.get_languages()}  
        networks = {n.get_id(): n for n in library.get_networks()}  
  
        for item in library.get_media():  
  
            pending = getattr(item, "_pending", None)  
  
            if not pending:  
                continue  
  
            for name in pending.get("genres", []):  
                if name in genres:  
                    item.add_genre(genres[name])  
  
            for name in pending.get("tags", []):  
                if name in tags:  
                    item.add_tag(tags[name])  
  
            for name in pending.get("themes", []):  
                if name in themes:  
                    item.add_theme(themes[name])  
  
            for name in pending.get("languages", []):  
                if name in languages:  
                    item.add_language(languages[name])  
  
            country = pending.get("production_country")  
            if country in countries:  
                item.set_production_country(countries[country])  
  
            network = pending.get("original_network")  
            if network in networks:  
                item.set_original_network(networks[network])  
  
            del item._pending