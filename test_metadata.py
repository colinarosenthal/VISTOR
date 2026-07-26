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
    "metadata/data"  
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
# Serialization Round-Trip (people bucket)  
# ------------------------------------------------------------------  
  
print("\n=== Testing Serialization Round-Trip ===")  
  
  
round_trip_library = MetadataLibrary()  
  
round_trip_library.add_person(person)  
  
  
round_trip_serializer = MetadataSerializer(  
    round_trip_library  
)  
  
  
out_dir = Path(  
    "metadata/data"  
)  
  
  
round_trip_serializer.save_to_directory(out_dir)  
  
  
reloaded = MetadataLoader().load(out_dir)  
  
  
assert reloaded is not None  
  
print("Serialization round-trip complete")  

from metadata.services.metadata_library import MetadataLibrary  
from metadata.services.metadata_serializer import MetadataSerializer  
from metadata.services.metadata_loader import MetadataLoader  
  
meta = MetadataLibrary()  
  
# Media counts verified against the in-memory built library  
# (media serialization/loading is not implemented yet — see TODO below)  
assert len(movies) >= 1  
assert len(episodes) >= 1  
assert len(music_videos) >= 1  
assert len(commercials) >= 1  
  
# People round-trip is the only bucket that survives save/load today  
assert len(reloaded.get_people()) >= 1  
  
print("Serialization round-trip verified (people bucket).")
  
# TODO: enable populated-media round-trip once media flattening  
# is implemented in MetadataSerializer. Until then, media items  
# hold nested custom objects that json.dump cannot serialize.  
  
  
# ------------------------------------------------------------------  
# Final Result  
# ------------------------------------------------------------------  

print("\n================================")  
print("Metadata System Test Complete")  
print("All tests passed successfully.")  
print("================================")