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
# Final Result
# ------------------------------------------------------------------

print("\n================================")
print("Metadata System Test Complete")
print("All tests passed successfully.")
print("================================")

from metadata.services.metadata_population import MetadataPopulation


print("=== Testing Metadata Population ===")

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

from metadata.services.metadata_population import MetadataPopulation  
  
population = MetadataPopulation()  
library = population.build_library()  
  
print("Movies:", len(library.get_movies()))  
print("Episodes:", len(library.get_episodes()))  
print("Music videos:", len(library.get_music_videos()))  
print("Total:", library.get_total_media_count())  
  
# Reference-sharing check  
advertisers = population.create_advertisers()  
commercials = population.create_commercials(  
    advertisers,  
    population.create_products(advertisers),  
    population.create_campaigns(population.create_products(advertisers)),  
)  
assert commercials[0].get_advertiser() is advertisers["coca_cola"] 
print("Reference sharing verified.")

print("Commercials:", len(library.get_commercials()))  
assert len(library.get_commercials()) >= 1