"""
VISTOR Authoritative Enrichment

Refines a scraped/best-guess media record against an external authoritative
catalog to close the classification gap. Every backend implements:

    lookup(title, year=None, media_type=None) -> dict | None

Backends are offline-safe: with no network/key they return None, so enrich()
becomes a no-op and the smoke test runs offline with no keys configured.
"""

from metadata.services.enrichment.authoritative_source import AuthoritativeSource
from metadata.services.enrichment.tmdb_source import TMDBSource
from metadata.services.enrichment.musicbrainz_source import MusicBrainzSource
from metadata.services.enrichment.enrichment_router import EnrichmentRouter
from metadata.services.enrichment.metadata_enricher import MetadataEnricher


def default_source():
    """Type-routed authoritative source: one backend per media type
    (TMDB film/TV, MusicBrainz music, SportsSource sports, Wikipedia
    fallback). Offline-safe: every backend no-ops without keys/network."""
    return EnrichmentRouter()


__all__ = [
    "AuthoritativeSource",
    "TMDBSource",
    "MusicBrainzSource",
    "EnrichmentRouter",
    "MetadataEnricher",
    "default_source",
]
