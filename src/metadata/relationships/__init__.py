"""
VISTOR Relationships

Defines connections between metadata objects and physical media resources.
"""

from metadata.relationships.appearance import Appearance
from metadata.relationships.media_asset import MediaAsset

__all__ = [
    "Appearance",
    "MediaAsset",
]
