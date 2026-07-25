"""
VISTOR Vocabulary

Defines expandable descriptive metadata values used throughout VISTOR.
"""

from metadata.vocabulary.genre import Genre
from metadata.vocabulary.theme import Theme
from metadata.vocabulary.country import Country
from metadata.vocabulary.language import Language
from metadata.vocabulary.tag import Tag

__all__ = [
    "Genre",
    "Theme",
    "Country",
    "Language",
    "Tag",
]