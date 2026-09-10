"""
VISTOR Metadata Services

Provides loading, validation, searching, and serialization
for the VISTOR metadata system.
"""

from metadata.services.metadata_library import MetadataLibrary
from metadata.services.metadata_loader import MetadataLoader
from metadata.services.metadata_validator import MetadataValidator
from metadata.services.metadata_search import MetadataSearch
from metadata.services.metadata_serializer import MetadataSerializer
from metadata.services.source_resolver import SourceResolver, FetchResult
from metadata.services.fetchers import (
    BaseFetcher,
    InternetArchiveFetcher,
    YouTubeFetcher,
    HttpFetcher,
    ProviderRegistry,
    RealFetcher,
    MetadataProbe,
)

__all__ = [
    "MetadataLibrary",
    "MetadataLoader",
    "MetadataValidator",
    "MetadataSearch",
    "MetadataSerializer",
    "SourceResolver",
    "FetchResult",
    "BaseFetcher",
    "InternetArchiveFetcher",
    "YouTubeFetcher",
    "HttpFetcher",
    "ProviderRegistry",
    "RealFetcher",
    "MetadataProbe",
]
