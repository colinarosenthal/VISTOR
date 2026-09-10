"""
VISTOR Acquisition Tests

Multi-archive source resolution, the provider registry / RealFetcher,
MediaIngestor write-back, and channel discovery. Offline-safe (no network,
no yt-dlp). Run standalone: python src/tests/test_acquisition.py
"""

import sys
import json
import os
import shutil
import tempfile
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from metadata.services.source_resolver import SourceResolver, FetchResult
from metadata.relationships.media_asset import MediaAsset
from metadata.enums.download_status import DownloadStatus
from metadata.services.channel_discovery import ChannelDiscovery
from metadata.enums.audience import Audience
from metadata.services.fetchers.provider_registry import ProviderRegistry
from metadata.services.fetchers.real_fetcher import RealFetcher
from metadata.services.fetchers.http_fetcher import HttpFetcher
from metadata.services.media_ingestor import MediaIngestor


class _FakeFetcher:
    """Canned fetcher: maps 'provider:reference' -> FetchResult."""

    def __init__(self, responses):
        self._responses = responses

    def fetch(self, provider, reference):
        key = f"{provider}:{reference}"
        return self._responses.get(key, FetchResult.failure(404))


print("\n=== Testing Multi-Archive Resolver ===")

# --- First source 404s, second source succeeds (takedown rebind) ---
primary = MediaAsset(asset_id="res_primary", path="Media/res.mkv")
primary.add_source("internet_archive", "dead/reference.mkv")
primary.add_source("mirror_archive", "live/reference.mkv")

fetcher = _FakeFetcher({
    "internet_archive:dead/reference.mkv": FetchResult.failure(404),
    "mirror_archive:live/reference.mkv": FetchResult.success(),
})

resolver = SourceResolver(fetcher)
report = resolver.resolve(primary)

assert report["resolved"] is True
assert report["used_source"]["provider"] == "mirror_archive"
assert primary.get_download_status() == DownloadStatus.DOWNLOADED
assert len(report["attempts"]) == 2

# --- All sources fail (403), fingerprint replacement substitutes ---
missing = MediaAsset(asset_id="res_missing", path="Media/missing.mkv")
missing.add_source("internet_archive", "gone/reference.mkv")
missing.set_fingerprint("abc123")

twin = MediaAsset(asset_id="res_twin", path="Media/twin.mkv")
twin.set_fingerprint("abc123")
twin.set_download_status(DownloadStatus.DOWNLOADED)

dead_fetcher = _FakeFetcher({
    "internet_archive:gone/reference.mkv": FetchResult.failure(403),
})

report2 = SourceResolver(dead_fetcher).resolve(missing, candidates=[missing, twin])

assert report2["resolved"] is False
assert report2["replacement"] == "res_twin"
assert missing.get_download_status() == DownloadStatus.FAILED

# --- No sources, no candidates -> clean failure ---
orphan = MediaAsset(asset_id="res_orphan", path="Media/orphan.mkv")
report3 = SourceResolver(_FakeFetcher({})).resolve(orphan)
assert report3["resolved"] is False
assert report3["replacement"] is None
assert orphan.get_download_status() == DownloadStatus.FAILED

print("Multi-archive resolver verified.")


print("\n=== Testing Channel Discovery ===")


class _StubNamed:
    """Minimal genre/tag stand-in exposing get_name()."""

    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name


class _StubItem:
    """Catalog item exposing only the accessors ChannelDiscovery uses."""

    def __init__(self, item_id, genres=None, audience=None, tags=None):
        self._id = item_id
        self._genres = [_StubNamed(g) for g in (genres or [])]
        self._audience = audience
        self._tags = [_StubNamed(t) for t in (tags or [])]

    def get_id(self):
        return self._id

    def get_genres(self):
        return self._genres

    def get_audience(self):
        return self._audience

    def get_tags(self):
        return self._tags


class _StubChannel:
    """Channel stand-in exposing the spec accessors used for matching."""

    def __init__(self, name, primary_genre, target_audience,
                 programming_sources=None):
        self.name = name
        self._primary_genre = primary_genre
        self._target_audience = target_audience
        self._programming_sources = programming_sources or []

    def get_primary_genre(self):
        return self._primary_genre

    def get_target_audience(self):
        return self._target_audience

    def get_programming_sources(self):
        return self._programming_sources


discovery = ChannelDiscovery()

kids_channel = _StubChannel(
    name="Cartoon Zone",
    primary_genre="Animation",
    target_audience="KIDS",
)

strong = _StubItem(
    "toon_strong",
    genres=["Animation"],
    audience=Audience.KIDS,
    tags=["animation-block"],
)
weak = _StubItem("toon_weak", genres=["Animation"], audience=Audience.ADULT)
miss = _StubItem("news_item", genres=["News"], audience=Audience.ADULT)
no_aud = _StubItem("toon_no_aud", genres=["Animation"], audience=None)

ranked = discovery.discover(kids_channel, [miss, weak, strong, no_aud])
ids = [i.get_id() for i in ranked]

assert "news_item" not in ids
assert ids[0] == "toon_strong"
assert "toon_weak" in ids
assert "toon_no_aud" in ids

gated_channel = _StubChannel(
    name="Gated Toons",
    primary_genre="Animation",
    target_audience="KIDS",
    programming_sources=["toon_strong"],
)
gated_ids = [i.get_id() for i in discovery.discover(gated_channel, [strong, weak, miss])]
assert gated_ids == ["toon_strong"]

print("Channel discovery verified.")


print("\n=== Testing Provider Registry + RealFetcher (offline) ===")


class _StubProviderFetcher:
    """Stand-in provider fetcher: never touches the network."""

    def __init__(self, result):
        self._result = result
        self.current_asset = None

    def fetch(self, provider, reference):
        return self._result


registry = ProviderRegistry()
registry.register("internet_archive", _StubProviderFetcher(FetchResult.failure(404)))
registry.register("youtube", _StubProviderFetcher(FetchResult.success()))

real = RealFetcher(registry=registry)

rf_asset = MediaAsset(asset_id="rf_asset", path="Media/rf.mkv")
rf_asset.add_source("internet_archive", "dead/ref.mkv")
rf_asset.add_source("youtube", "fzHD04_OwyQ")

real.bind(rf_asset)
rf_report = SourceResolver(real).resolve(rf_asset)

assert rf_report["resolved"] is True
assert rf_report["used_source"]["provider"] == "youtube"
assert rf_asset.get_download_status() == DownloadStatus.DOWNLOADED

# Unknown provider falls back to the generic HTTP fetcher instance.
assert isinstance(ProviderRegistry().get("some_random_site"), HttpFetcher)

print("Provider routing + RealFetcher delegation verified.")


print("\n=== Testing MediaIngestor Write-Back (offline) ===")

# Point the ingestor at a throwaway copy of the metadata dir.
wb_dir = tempfile.mkdtemp(prefix="vistor_wb_")
wb_media = os.path.join(wb_dir, "media.json")
with open(wb_media, "w", encoding="utf-8") as f:
    json.dump([], f)

drop_in = os.path.join(wb_dir, "wb_demo.json")
with open(drop_in, "w", encoding="utf-8") as f:
    json.dump({
        "type": "Movie",
        "id": "wb_demo",
        "title": "WB Demo",
        "assets": [{
            "asset_id": "wb_demo-asset-1",
            "path": os.path.join(wb_dir, "wb_demo.mkv"),
            "sources": [{"provider": "youtube", "reference": "wb_ref"}],
        }],
    }, f)

# Canned success for this one source -> no network, no yt-dlp.
fake = _FakeFetcher({"youtube:wb_ref": FetchResult.success()})

ingestor = MediaIngestor(metadata_path=wb_dir)
report = ingestor.ingest_file(drop_in, download=True, fetcher=fake)

with open(wb_media, "r", encoding="utf-8") as f:
    persisted = json.load(f)

asset = persisted[0]["assets"][0]
assert asset.get("download_status") == "DOWNLOADED"

shutil.rmtree(wb_dir, ignore_errors=True)
print("MediaIngestor write-back (download_status persisted) verified.")
print("\nAcquisition tests passed.")
