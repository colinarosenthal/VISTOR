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
  
from core.logger import Logger  
  
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
from metadata.media.miscellaneous.ambient import Ambient  
  
from metadata.relationships.media_asset import MediaAsset  
from metadata.enums.download_status import DownloadStatus  
  
  
class MetadataLoader:  
    """Loads VISTOR metadata into memory."""  
  
    # ------------------------------------------------------------------  
    # Construction  
    # ------------------------------------------------------------------  
  
    def __init__(self):  
        pass  
  
    # ------------------------------------------------------------------  
    # File Reading Helper  
    # ------------------------------------------------------------------  
  
    def _read_json(self, path: Path):  
        """  
        Read a metadata JSON file safely.  
  
        Returns a list of records, or an empty list if the file is  
        missing or malformed. Missing files are treated as "nothing  
        to load" (info); malformed files are logged as errors and  
        skipped so loading can continue.  
        """  
  
        if not path.exists():  
            Logger.info(f"Metadata file not found, skipping: {path.name}")  
            return []  
  
        try:  
            with open(path, "r", encoding="utf-8") as file:  
                data = json.load(file)  
        except json.JSONDecodeError as error:  
            Logger.error(f"Malformed metadata file {path.name}: {error}")  
            return []  
        except OSError as error:  
            Logger.error(f"Could not read metadata file {path.name}: {error}")  
            return []  
  
        if not isinstance(data, list):  
            Logger.error(  
                f"Metadata file {path.name} must contain a list, "  
                f"got {type(data).__name__}; skipping."  
            )  
            return []  
  
        return data  
  
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
        self._load_franchises(library, metadata_path)  
        self._load_series(library, metadata_path)  
        self._load_seasons(library, metadata_path)  
  
        self._load_advertisers(library, metadata_path)  
        self._load_products(library, metadata_path)  
        self._load_campaigns(library, metadata_path)  
  
        self._load_media(library, metadata_path)  
  
        self._resolve_relationships(library)  
  
        return library  
  
    # ------------------------------------------------------------------  
    # Library-Level Loading  
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
        """Load network metadata."""  
  
        path = metadata_path / "networks.json"  
  
        for item in self._read_json(path):  
  
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
        """Load studio metadata."""  
  
        path = metadata_path / "studios.json"  
  
        for item in self._read_json(path):  
  
            studio = Studio(  
                id=item["id"],  
                name=item["name"],  
                country=item.get("country", ""),  
                founded_year=item.get("founded_year", 0),  
                description=item.get("description", ""),  
            )  
  
            library.add_studio(studio)  
  
    # ------------------------------------------------------------------  
    # Vocabulary Loading  
    # ------------------------------------------------------------------  
  
    def _load_vocabulary(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load vocabulary metadata."""  
  
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
        """Load genre metadata."""  
  
        path = metadata_path / "genres.json"  
  
        for item in self._read_json(path):  
  
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
        """Load country metadata."""  
  
        path = metadata_path / "countries.json"  
  
        for item in self._read_json(path):  
  
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
        """Load theme metadata."""  
  
        path = metadata_path / "themes.json"  
  
        records = self._read_json(path)  
  
        # First pass: create every theme without its parent link.  
        for item in records:  
  
            theme = Theme(  
                name=item["name"],  
                description=item.get("description", ""),  
            )  
  
            library.add_theme(theme)  
  
        # Second pass: resolve parent_theme references by name.  
        theme_lookup = {t.get_name(): t for t in library.get_themes()}  
  
        for item in records:  
  
            parent_name = item.get("parent_theme")  
  
            if parent_name is None:  
                continue  
  
            child = theme_lookup.get(item["name"])  
            parent = theme_lookup.get(parent_name)  
  
            if child is not None and parent is not None:  
                child.parent_theme = parent  
  
    def _load_tags(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load tag metadata."""  
  
        path = metadata_path / "tags.json"  
  
        for item in self._read_json(path):  
  
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
        """Load language metadata."""  
  
        path = metadata_path / "languages.json"  
  
        for item in self._read_json(path):  
  
            language = Language(  
                name=item["name"],  
                iso_639_1=item.get("iso_639_1", ""),  
                iso_639_2=item.get("iso_639_2", ""),  
                native_name=item.get("native_name", ""),  
            )  
  
            library.add_language(language)  
  
    # ------------------------------------------------------------------  
    # People  
    # ------------------------------------------------------------------  
  
    def _load_people(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load people metadata."""  
  
        path = metadata_path / "people.json"  
  
        for item in self._read_json(path):  
  
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
  
    # ------------------------------------------------------------------  
    # Franchises / Series / Seasons  
    # ------------------------------------------------------------------  
  
    def _load_franchises(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load franchise metadata."""  
  
        path = metadata_path / "franchises.json"  
  
        for item in self._read_json(path):  
  
            franchise = Franchise(  
                id=item["id"],  
                name=item["name"],  
                description=item.get("description", ""),  
            )  
  
            library.add_franchise(franchise)  
  
    def _load_series(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load series metadata."""  
  
        path = metadata_path / "series.json"  
  
        franchises = {f.get_id(): f for f in library.get_franchises()}  
  
        for item in self._read_json(path):  
  
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
  
    def _load_seasons(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load season metadata."""  
  
        path = metadata_path / "seasons.json"  
  
        series_lookup = {s.get_id(): s for s in library.get_series()}  
  
        for item in self._read_json(path):  
  
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
  
    # ------------------------------------------------------------------  
    # Advertising Entities  
    # ------------------------------------------------------------------  
  
    def _load_advertisers(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load advertiser metadata."""  
  
        path = metadata_path / "advertisers.json"  
  
        for item in self._read_json(path):  
  
            advertiser = Advertiser(  
                id=item["id"],  
                name=item["name"],  
                description=item.get("description", ""),  
                country=item.get("country", ""),  
            )  
  
            library.add_advertiser(advertiser)  
  
    def _load_products(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load product metadata."""  
  
        path = metadata_path / "products.json"  
  
        advertiser_lookup = {a.get_id(): a for a in library.get_advertisers()}  
  
        for item in self._read_json(path):  
  
            advertiser = advertiser_lookup.get(item.get("advertiser"))  
  
            if advertiser is None:  
                # Product requires an advertiser; skip if its parent  
                # was not serialized.  
                continue  
  
            product = Product(  
                id=item["id"],  
                name=item["name"],  
                advertiser=advertiser,  
                description=item.get("description", ""),  
                category=item.get("category", ""),  
                release_year=item.get("release_year", 0),  
            )  
  
            library.add_product(product)  
  
    def _load_campaigns(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load campaign metadata."""  
  
        path = metadata_path / "campaigns.json"  
  
        product_lookup = {p.get_id(): p for p in library.get_products()}  
  
        for item in self._read_json(path):  
  
            product = product_lookup.get(item.get("product"))  
  
            if product is None:  
                # Campaign requires a product; skip if its parent  
                # was not serialized.  
                continue  
  
            campaign = Campaign(  
                id=item["id"],  
                name=item["name"],  
                product=product,  
                start_year=item.get("start_year", 0),  
                end_year=item.get("end_year", 0),  
                description=item.get("description", ""),  
                slogan=item.get("slogan", ""),  
            )  
  
            library.add_campaign(campaign)  
  
    # ------------------------------------------------------------------  
    # Media  
    # ------------------------------------------------------------------  
  
    def _load_media(  
        self,  
        library: MetadataLibrary,  
        metadata_path: Path,  
    ):  
        """Load all media objects."""  
  
        path = metadata_path / "media.json"  
  
        seasons = {s.get_id(): s for s in library.get_seasons()}  
  
        for item in self._read_json(path):  
  
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
            elif media_type == "Ambient":  
                obj = Ambient(  
                    id=item["id"],  
                    title=item["title"],  
                    release_year=item.get("release_year", 0),  
                    runtime_minutes=item.get("runtime_minutes", 30),  
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
            obj.scheduling_priority = item.get("scheduling_priority", 0)  
  
            for asset_data in item.get("assets", []):  
                obj.add_media_asset(MediaAsset.from_dictionary(asset_data))  
  
            # Stash flattened refs for _resolve_relationships.  
            obj._pending = item  
  
            library.add_media(obj)  
  
    # ------------------------------------------------------------------  
    # Relationship Resolution  
    # ------------------------------------------------------------------  
  
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
        advertisers = {a.get_id(): a for a in library.get_advertisers()}  
        products = {p.get_id(): p for p in library.get_products()}  
        campaigns = {c.get_id(): c for c in library.get_campaigns()}  
        franchises = {f.get_id(): f for f in library.get_franchises()}  
        music_genres = {g.get_name(): g for g in library.get_music_genres()}  
        people = {p.get_id(): p for p in library.get_people()}  
        studios = {s.get_id(): s for s in library.get_studios()}  
  
        for item in library.get_media():  
  
            pending = getattr(item, "_pending", None)  
  
            if not pending:  
                continue  
  
            advertiser = pending.get("advertiser")  
            if advertiser in advertisers:  
                item.set_advertiser(advertisers[advertiser])  
  
            product = pending.get("product")  
            if product in products:  
                item.set_product(products[product])  
  
            campaign = pending.get("campaign")  
            if campaign in campaigns:  
                item.set_campaign(campaigns[campaign])  
  
            franchise = pending.get("franchise")  
            if franchise in franchises:  
                item.set_franchise(franchises[franchise])  
  
            music_genre = pending.get("music_genre")  
            if music_genre in music_genres:  
                item.set_music_genre(music_genres[music_genre])  
  
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
  
            for sid in pending.get("studios", []):  
                if sid in studios:  
                    item.add_studio(studios[sid])  
  
            from metadata.relationships.appearance import Appearance  
            from metadata.enums.role_type import RoleType  
  
            for app in pending.get("appearances", []):  
                person = people.get(app.get("person"))  
                if person is None:  
                    continue  
                try:  
                    role = RoleType[app.get("role", "ACTOR")]  
                except KeyError:  
                    role = RoleType.ACTOR  
  
                app_id = app.get("id") or (  
                    f"{item.get_id()}-{app.get('person')}-{role.name.lower()}"  
                )  
  
                item.add_appearance(Appearance(  
                    id=app_id,  
                    person=person,  
                    media_item=item,  
                    role=role,  
                    role_name=app.get("role_name", ""),  
                    billing_order=app.get("billing_order", 0),  
                    credited=app.get("credited", True),  
                ))  
  
            del item._pending