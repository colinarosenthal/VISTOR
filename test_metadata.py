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