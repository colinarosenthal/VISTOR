"""  
VISTOR Metadata Serializer Service  
  
Converts VISTOR metadata objects into  
storable formats.  
"""  
  
import json  
  
from pathlib import Path  
  
  
class MetadataSerializer:  
    """  
    Serializes metadata library objects.  
    """  
  
    def __init__(self, metadata_library):  
  
        self.library = metadata_library  
  
    # ------------------------------------------------------------------  
    # Public Interface  
    # ------------------------------------------------------------------  
  
    def to_dictionary(self):  
        """  
        Convert metadata library to a single combined dictionary.  
        Used by tests and validators that expect an in-memory view.  
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
  
    def save_to_directory(self, directory):  
        """  
        Write one JSON file per metadata bucket into `directory`.  
        """  
  
        directory = Path(directory)  
  
        directory.mkdir(parents=True, exist_ok=True)  
  
        # Flat objects (all attributes are primitives / lists of primitives)   
        flat = {  
            "genres": self.library.get_genres(),  
            "tags": self.library.get_tags(),  
            "countries": self.library.get_countries(),  
            "languages": self.library.get_languages(),  
            "content_ratings": self.library.get_content_ratings(),  
            "networks": self.library.get_networks(),  
            "studios": self.library.get_studios(),  
            "franchises": self.library.get_franchises(),  
            "advertisers": self.library.get_advertisers(),  
            "people": self.library.get_people(),  
        }
  
        for name, items in flat.items():  
            self._write_json(  
                directory / f"{name}.json",  
                [self._object_to_dictionary(item) for item in items],  
            )  
  
        # Objects with nested references need dedicated flatteners  
        self._write_json(  
            directory / "themes.json",  
            [self._theme_to_dictionary(t) for t in self.library.get_themes()],  
        )  
        self._write_json(  
            directory / "music_genres.json",  
            [self._music_genre_to_dictionary(g)  
             for g in self.library.get_music_genres()],  
        )
        self._write_json(  
            directory / "series.json",  
            [self._series_to_dictionary(s) for s in self.library.get_series()],  
        )  
        self._write_json(  
            directory / "seasons.json",  
            [self._season_to_dictionary(s) for s in self.library.get_seasons()],  
        )  
        self._write_json(  
            directory / "products.json",  
            [self._product_to_dictionary(p) for p in self.library.get_products()],  
        )  
        self._write_json(  
            directory / "campaigns.json",  
            [self._campaign_to_dictionary(c) for c in self.library.get_campaigns()],  
        )  
        self._write_json(  
            directory / "media.json",  
            [self._media_to_dictionary(m) for m in self.library.get_media()],  
        )  
  
    # ------------------------------------------------------------------  
    # Helpers  
    # ------------------------------------------------------------------  
  
    def _write_json(self, path, data):  
        """Write `data` to `path` as indented JSON."""  
  
        with open(path, "w", encoding="utf-8") as file:  
            json.dump(data, file, indent=4)  
  
    def _object_to_dictionary(self, obj):  
        """Convert flat object attributes into a dictionary."""  
  
        return {  
            key: value  
            for key, value in vars(obj).items()  
            if not key.startswith("_")  
        }  
  
    def _music_genre_to_dictionary(self, genre):  
        parent = genre.get_parent_genre()  
        return {  
            "name": genre.get_name(),  
            "description": genre.get_description(),  
            "parent_genre": parent.get_name() if parent else None,  
        }

    def _theme_to_dictionary(self, theme):  
        parent = theme.get_parent_theme()  
        return {  
            "name": theme.get_name(),  
            "description": theme.get_description(),  
            "parent_theme": parent.get_name() if parent else None,  
        }
  
    def _series_to_dictionary(self, series):  
        franchise = series.get_franchise()  
        return {  
            "id": series.get_id(),  
            "title": series.get_title(),  
            "franchise": franchise.get_id() if franchise else None,  
            "description": series.get_description(),  
            "premiere_year": series.get_premiere_year(),  
            "finale_year": series.get_finale_year(),  
        }  
  
    def _season_to_dictionary(self, season):  
        return {  
            "id": season.get_id(),  
            "series": season.get_series().get_id(),  
            "season_number": season.get_season_number(),  
            "title": season.get_title(),  
            "description": season.get_description(),  
            "premiere_year": season.get_premiere_year(),  
        }  
  
    def _product_to_dictionary(self, product):  
        return {  
            "id": product.get_id(),  
            "name": product.get_name(),  
            "advertiser": product.get_advertiser().get_id(),  
            "description": product.get_description(),  
            "category": product.get_category(),  
            "release_year": product.get_release_year(),  
        }  
  
    def _campaign_to_dictionary(self, campaign):  
        return {  
            "id": campaign.get_id(),  
            "name": campaign.get_name(),  
            "product": campaign.get_product().get_id(),  
            "start_year": campaign.get_start_year(),  
            "end_year": campaign.get_end_year(),  
            "description": campaign.get_description(),  
            "slogan": campaign.get_slogan(),  
        }  
  
    def _media_to_dictionary(self, item):  
        from metadata.media.film.movie import Movie  
        from metadata.media.television.episode import Episode  
        from metadata.media.advertising.commercial import Commercial  
        from metadata.media.music.music_video import MusicVideo  
  
        rating = item.get_content_rating()  
        network = item.get_original_network()  
        country = item.get_production_country()  
  
        data = {  
            "type": type(item).__name__,  
            "id": item.get_id(),  
            "title": item.get_title(),  
            "description": item.get_description(),  
            "release_year": item.get_release_year(),  
            "runtime_minutes": item.get_runtime_minutes(),  
            "scheduling_priority": item.get_scheduling_priority(),
            "content_rating": (  
                {"system": rating.get_system(), "name": rating.get_name()}  
                if rating else None  
            ),  
            "original_network": network.get_id() if network else None,  
            "production_country": country.get_name() if country else None,  
            "languages": [l.get_name() for l in item.get_languages()],  
            "genres": [g.get_name() for g in item.get_genres()],  
            "tags": [t.get_name() for t in item.get_tags()],  
            "themes": [t.get_name() for t in item.get_themes()],
            "appearances": [  
                {  
                    "id": a.get_id(),  
                    "person": a.get_person().get_id() if a.get_person() else None,  
                    "role": a.get_role().name,  
                    "role_name": a.get_role_name(),  
                    "billing_order": a.get_billing_order(),  
                    "credited": a.is_credited(),  
                }  
                for a in item.get_appearances()  
            ],
            "assets": [a.to_dictionary() for a in item.get_media_assets()],
            "studios": [s.get_id() for s in item.get_studios()],
        }  
  
        if isinstance(item, Episode):  
            season = item.get_season()  
            data["episode_number"] = item.get_episode_number()  
            data["season"] = season.get_id() if season else None  
        elif isinstance(item, Movie):  
            franchise = item.get_franchise()  
            data["franchise"] = franchise.get_id() if franchise else None  
        elif isinstance(item, Commercial):  
            advertiser = item.get_advertiser()  
            product = item.get_product()  
            campaign = item.get_campaign()  
            data["advertiser"] = advertiser.get_id() if advertiser else None  
            data["product"] = product.get_id() if product else None  
            data["campaign"] = campaign.get_id() if campaign else None  
        elif isinstance(item, MusicVideo):  
            music_genre = item.get_music_genre()  
            data["music_genre"] = music_genre.get_name() if music_genre else None  
  
        return data

    def _media_asset_to_dictionary(self, asset):  
        """Flatten a MediaAsset (Path -> str, enum -> name)."""  
  
        return {  
            "asset_id": asset.get_asset_id(),  
            "path": str(asset.get_path()),  
            "checksum": asset.get_checksum(),  
            "runtime_seconds": asset.get_runtime_seconds(),  
            "file_size": asset.get_file_size(),  
            "video_codec": asset.get_video_codec(),  
            "audio_codec": asset.get_audio_codec(),  
            "container": asset.get_container(),  
            "width": asset.get_resolution()[0],  
            "height": asset.get_resolution()[1],  
            "frame_rate": asset.get_frame_rate(),  
            "verified": asset.is_verified(),  
            "download_status": asset.get_download_status().name,  
            "last_played": asset.get_last_played(),  
            "sources": asset.get_sources(),  
            "pinned": asset.is_pinned(),  
            "broadcast_score": asset.get_broadcast_score(),  
            "retention_score": asset.get_retention_score(),  
            "fingerprint": asset.get_fingerprint(),
        }