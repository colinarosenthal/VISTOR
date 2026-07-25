import sys

sys.path.append("src")

from metadata.enums import *
from metadata.vocabulary import *
from metadata.library import *
from metadata.media import *
from metadata.relationships import *


print("Metadata imports successful")


print("Testing library models...")

person = Person(
    id="person_000001",
    name="Test Person"
)

print(person)


print("Testing media item...")

program = MediaItem(
    id="media_000001",
    title="Test Program"
)

print(program)


print("Testing appearance relationship...")

appearance = Appearance(
    id="appearance_000001",
    person=person,
    media_item=program,
    role=RoleType.ACTOR,
)

print(appearance)


print("Testing collection...")

collection = Collection(
    title="Test Collection"
)

collection.add_item(program)

print(collection)
print(f"Collection items: {collection.get_item_count()}")


print("Testing media library...")

media_library = MediaLibrary()

media_library.add_movie(program)

print(media_library)
print(f"Movies: {len(media_library.get_movies())}")


print("Metadata architecture test complete")

from metadata.services import MetadataLibrary


print("Testing MetadataLibrary...")

metadata_library = MetadataLibrary()

metadata_library.add_person(person)

print(metadata_library)

print(
    "People:",
    len(metadata_library.get_people())
)

from metadata.services import MetadataSearch


print("Testing MetadataSearch...")

search = MetadataSearch(metadata_library)

results = search.find_person("Test Person")

print("Search Results:", results)

from metadata.services import MetadataSerializer


print("Testing MetadataSerializer...")

serializer = MetadataSerializer(metadata_library)

metadata_data = serializer.to_dictionary()

print(metadata_data)

from metadata.services import MetadataValidator


print("Testing MetadataValidator...")

validator = MetadataValidator()

validation_results = validator.validate(media_library)

print(validation_results)