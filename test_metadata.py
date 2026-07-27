import sys  
  
from pathlib import Path  
  
sys.path.append("src")  
  
  
# ------------------------------------------------------------------  
# Imports  
# ------------------------------------------------------------------  
  
from metadata.enums import *  
from metadata.vocabulary import *  
from metadata.library import *  
from metadata.media import *  
from metadata.relationships import *  
  
from metadata.services import (  
    MetadataLibrary,  
    MetadataSearch,  
    MetadataSerializer,  
    MetadataValidator,  
    MetadataLoader,  
)  
  
from metadata.services.metadata_population import MetadataPopulation  
  
from metadata.media.film.movie import Movie  
from metadata.media.television.episode import Episode  
from metadata.media.music.music_video import MusicVideo  
from metadata.media.advertising.commercial import Commercial  
  
  
print("\n=== Metadata Import Test ===")  
  
print("Metadata imports successful")  
  
  
# ------------------------------------------------------------------  
# Model Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing Metadata Models ===")  
  
  
print("Testing Person...")  
  
person = Person(  
    id="person_000001",  
    name="Test Person",  
)  
  
print(person)  
  
  
print("Testing Media Item...")  
  
program = MediaItem(  
    id="media_000001",  
    title="Test Program",  
)  
  
print(program)  
  
  
print("Testing Appearance Relationship...")  
  
appearance = Appearance(  
    id="appearance_000001",  
    person=person,  
    media_item=program,  
    role=RoleType.ACTOR,  
)  
  
print(appearance)  
  
  
# ------------------------------------------------------------------  
# Collection Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing Collections ===")  
  
  
collection = Collection(  
    title="Test Collection"  
)  
  
collection.add_item(program)  
  
print(collection)  
  
assert collection.get_item_count() == 1  
  
print(  
    "Collection items:",  
    collection.get_item_count()  
)  
  
  
# ------------------------------------------------------------------  
# Media Library Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing Media Library ===")  
  
  
media_library = MediaLibrary()  
  
media_library.add_movie(program)  
  
print(media_library)  
  
assert len(media_library.get_movies()) == 1  
  
print(  
    "Movies:",  
    len(media_library.get_movies())  
)  
  
  
# ------------------------------------------------------------------  
# Metadata Library Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing MetadataLibrary ===")  
  
  
metadata_library = MetadataLibrary()  
  
metadata_library.add_person(person)  
  
metadata_library.add_relationship(  
    appearance  
)  
  
print(metadata_library)  
  
assert len(metadata_library.get_people()) == 1  
  
assert len(metadata_library.get_relationships()) == 1  
  
print(  
    "People:",  
    len(metadata_library.get_people())  
)  
  
print(  
    "Relationships:",  
    len(metadata_library.get_relationships())  
)  
  
  
# ------------------------------------------------------------------  
# Metadata Search Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing MetadataSearch ===")  
  
  
search = MetadataSearch(  
    metadata_library  
)  
  
  
person_results = search.find_person(  
    "Test Person"  
)  
  
print(  
    "Person Search:",  
    person_results  
)  
  
  
assert len(person_results) == 1  
  
  
# ------------------------------------------------------------------  
# Metadata Serializer Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing MetadataSerializer ===")  
  
  
serializer = MetadataSerializer(  
    metadata_library  
)  
  
  
metadata_data = serializer.to_dictionary()  
  
  
print(metadata_data)  
  
  
assert "people" in metadata_data  
  
assert len(metadata_data["people"]) == 1  
  
  
# ------------------------------------------------------------------  
# Metadata Validator Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing MetadataValidator ===")  
  
  
validator = MetadataValidator()  
  
  
validation_result = validator.validate(  
    metadata_library  
)  
  
  
print(  
    "Validation Result:",  
    validation_result  
)  
  
  
assert validation_result is True  
  
  
# ------------------------------------------------------------------  
# Metadata Loader Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing MetadataLoader ===")  
  
  
loader = MetadataLoader()  
  
  
metadata_path = Path(  
    "Metadata/data"  
)
  
  
loaded_library = loader.load(  
    metadata_path  
)  
  
  
print(  
    loaded_library  
)  
  
  
assert loaded_library is not None  
  
  
print(  
    "Metadata loading pipeline complete"  
)  
  
  
# ------------------------------------------------------------------  
# Metadata Population  
# ------------------------------------------------------------------  
  
print("\n=== Testing Metadata Population ===")  
  
  
population = MetadataPopulation()  
  
genres = population.create_genres()  
  
print("Genres Created:", len(genres))  
  
for genre in genres:  
    print("-", genre)  
  
    print()  
  
print("Testing Music Genre Population...")  
  
music_genres = population.create_music_genres()  
  
print(  
    "Music Genres Created:",  
    len(music_genres)  
)  
  
for genre in music_genres:  
    print("-", genre)  
  
  
# ------------------------------------------------------------------  
# Library Assembly  
# ------------------------------------------------------------------  
  
print("\n=== Testing Library Assembly ===")  
  
  
library = population.build_library()  
  
media = library.get_media()  
  
movies = [m for m in media if isinstance(m, Movie)]  
episodes = [m for m in media if isinstance(m, Episode)]  
music_videos = [m for m in media if isinstance(m, MusicVideo)]  
commercials = [m for m in media if isinstance(m, Commercial)]  
  
print("Movies:", len(movies))  
print("Episodes:", len(episodes))  
print("Music videos:", len(music_videos))  
print("Commercials:", len(commercials))  
print("Total:", len(media))  
  
  
# Reference-sharing check  
advertisers = population.create_advertisers()  
products = population.create_products(advertisers)  
campaigns = population.create_campaigns(products)  
  
check_commercials = population.create_commercials(  
    advertisers,  
    products,  
    campaigns,  
)  
  
assert check_commercials[0].get_advertiser() is advertisers["coca_cola"]  
  
print("Reference sharing verified.")  
  
assert len(commercials) >= 1  
  
  
# ------------------------------------------------------------------  
# Serialization Round-Trip (media exercised)  
# ------------------------------------------------------------------  

from metadata.media.film.movie import Movie  
from metadata.media.television.episode import Episode  
from metadata.media.music.music_video import MusicVideo  
from metadata.media.advertising.commercial import Commercial

print("\n=== Testing Serialization Round-Trip ===")  
  
# Build a populated MetadataLibrary so the media buckets are actually written.  
round_trip_library = MetadataLibrary()  
  
# Carry the person over so people.json is still exercised too.  
round_trip_library.add_person(person)  
  
# build_library() returns a MediaLibrary; move its media into the  
# MetadataLibrary the serializer understands (get_media / add_media).  
built = population.build_library()  
  
for movie in built.get_movies():  
    round_trip_library.add_media(movie)  
  
for episode in built.get_episodes():  
    round_trip_library.add_media(episode)  
  
for video in built.get_music_videos():  
    round_trip_library.add_media(video)  
  
for commercial in built.get_commercials():  
    round_trip_library.add_media(commercial)

seen_seasons = {}  
seen_series = {}  
seen_franchises = {}  
  
for episode in built.get_episodes():  
    round_trip_library.add_media(episode)  
  
    season = episode.get_season()  
    if season and season.get_id() not in seen_seasons:  
        seen_seasons[season.get_id()] = season  
  
        series = season.get_series()  
        if series and series.get_id() not in seen_series:  
            seen_series[series.get_id()] = series  
  
            franchise = series.get_franchise()  
            if franchise and franchise.get_id() not in seen_franchises:  
                seen_franchises[franchise.get_id()] = franchise  
  
for franchise in seen_franchises.values():  
    round_trip_library.add_franchise(franchise)  
  
for series in seen_series.values():  
    round_trip_library.add_series(series)  
  
for season in seen_seasons.values():  
    round_trip_library.add_season(season)  
  
# Serialize to disk. Keep this path casing identical to the loader's.  
metadata_path = Path("Metadata/data")  
  
MetadataSerializer(round_trip_library).save_to_directory(metadata_path)  
  
print("Serialization round-trip complete")  
  
# Reload from disk.  
reloaded = MetadataLoader().load(metadata_path)  
  
loaded_media = reloaded.get_media()  
  
loaded_movies = [m for m in loaded_media if isinstance(m, Movie)]  
loaded_episodes = [m for m in loaded_media if isinstance(m, Episode)]  
loaded_music_videos = [m for m in loaded_media if isinstance(m, MusicVideo)]  
loaded_commercials = [m for m in loaded_media if isinstance(m, Commercial)]  
  
print("Loaded movies:", len(loaded_movies))  
print("Loaded episodes:", len(loaded_episodes))  
print("Loaded music videos:", len(loaded_music_videos))  
print("Loaded commercials:", len(loaded_commercials))  
print("Loaded total:", len(loaded_media))  
  
assert len(loaded_movies) >= 1  
assert len(loaded_music_videos) >= 1  
assert len(loaded_commercials) >= 1  
  
# Episodes need series/seasons serialized before they can reconstruct  
# (Episode.__init__ requires a Season). Enable once those buckets are written.  
assert len(loaded_episodes) >= 1  
  
# People bucket still round-trips.  
assert len(reloaded.get_people()) >= 1  
  
print("Serialization round-trip verified (media exercised).")  

# ----------------------------------------------------------------------  
# Media Verifier  
# ----------------------------------------------------------------------  
  
print("\n=== Testing MediaVerifier ===")  
  
from metadata.services.media_verifier import (  
    MediaVerifier,  
    normalize_filename,  
)  
from metadata.services.metadata_population import MetadataPopulation  
  
verifier_library = MetadataPopulation().build_library()  
  
verifier = MediaVerifier(verifier_library)  
report = verifier.verify()  
  
assert "total_media" in report  
assert "total_assets" in report  
assert isinstance(report["verified"], list)  
assert isinstance(report["missing"], list)  
  
print("Media items checked:", report["total_media"])  
print("Assets checked:", report["total_assets"])  
print("Verified:", len(report["verified"]))  
print("Missing:", len(report["missing"]))  
  
# Filename normalization checks  
assert normalize_filename("Friends S01E01 (Pilot).MKV") == "friends_s01e01_pilot.mkv"  
assert normalize_filename("  Weird##Name!!.MP4 ") == "weird_name.mp4"  
  
print("Filename normalization verified.")

# ----------------------------------------------------------------------  
# Media Scanner  
# ---------------------------------------------------------------------- 

from metadata.services.media_scanner import MediaScanner  
  
print("=== Testing MediaScanner ===")  
  
scan_report = MediaScanner().scan()  
  
print("Media files found:", scan_report["total_files"])  
  
# Scanning an empty/missing Media dir is valid; just assert shape.  
assert "files" in scan_report  
assert "total_files" in scan_report  
  
print("Media scan verified.")
  
# ------------------------------------------------------------------  
# Final Result  
# ------------------------------------------------------------------  

print("\n================================")  
print("Metadata System Test Complete")  
print("All tests passed successfully.")  
print("================================")