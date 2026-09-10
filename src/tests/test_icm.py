"""
VISTOR Intelligent Content Management Tests

Asset persistence, keyframe fingerprinting, source age, scoring, and the
rolling cache. Run standalone: python src/tests/test_icm.py
"""

import sys
import tempfile
from pathlib import Path
from pathlib import Path as _Path
from datetime import datetime, timedelta

sys.path.append(str(Path(__file__).resolve().parent.parent))

from metadata.services.metadata_population import MetadataPopulation
from metadata.relationships.media_asset import MediaAsset
from metadata.enums.download_status import DownloadStatus
from metadata.services.metadata_serializer import MetadataSerializer
from metadata.services.metadata_loader import MetadataLoader
from metadata.services.keyframe_fingerprint import KeyframeFingerprintService
from metadata.services.asset_scorer import AssetScorer
from metadata.services.rolling_cache import RollingCache

# Shared fixture: a populated library and a real media item to attach assets to.
population = MetadataPopulation()
built = population.build_library()
sample = built.get_media()[0]


print("\n=== Testing Intelligent Content Management (asset persistence) ===")

asset = MediaAsset(asset_id="cm_test_asset", path="Media/cm_test.mkv")
asset.set_download_status(DownloadStatus.DOWNLOADED)
asset.add_source("internet_archive", "entiretyofeva/endofevaalldub.mkv")
asset.set_pinned(True)
asset.set_broadcast_score(7.5)
asset.set_retention_score(3.2)
asset.set_last_played("1999-10-04T20:00:00")
sample.add_media_asset(asset)

# Round-trip through disk.
tmp_dir = _Path(tempfile.mkdtemp())
MetadataSerializer(built).save_to_directory(tmp_dir)
loaded = MetadataLoader().load(tmp_dir)

reloaded = next(m for m in loaded.get_media() if m.get_id() == sample.get_id())
assets = reloaded.get_media_assets()
assert len(assets) >= 1

reloaded_asset = next(a for a in assets if a.get_asset_id() == "cm_test_asset")
assert reloaded_asset.get_download_status() == DownloadStatus.DOWNLOADED
assert reloaded_asset.is_available() is True
assert reloaded_asset.is_pinned() is True
assert reloaded_asset.get_broadcast_score() == 7.5
assert reloaded_asset.get_retention_score() == 3.2
assert reloaded_asset.get_last_played() == "1999-10-04T20:00:00"
assert any(
    s["provider"] == "internet_archive" for s in reloaded_asset.get_sources()
)

# A fresh asset with no file should report as needing download.
fresh = MediaAsset(asset_id="cm_fresh", path="Media/missing.mkv")
assert fresh.needs_download() is True
assert fresh.is_available() is False

print("Intelligent content management asset persistence verified.")


print("\n=== Testing Keyframe Fingerprinting ===")

fingerprinter = KeyframeFingerprintService()

# Deterministic, fixed-length generation.
fp_asset = MediaAsset(
    asset_id="fp_original",
    path="Media/fp_original.mkv",
    checksum="abc123",
    runtime_seconds=1500,
    width=1920,
    height=1080,
)
fp1 = fingerprinter.generate(fp_asset)
assert fp1 == fp_asset.get_fingerprint()
assert len(fp1) == 32

# Same visual identity -> identical fingerprint (distance 0).
fp_twin = MediaAsset(
    asset_id="fp_twin",
    path="Media/fp_original.mkv",
    checksum="abc123",
    runtime_seconds=1500,
    width=1920,
    height=1080,
)
fingerprinter.generate(fp_twin)
assert fingerprinter.distance(
    fp_asset.get_fingerprint(), fp_twin.get_fingerprint()
) == 0.0

# Different content -> non-zero distance.
fp_other = MediaAsset(
    asset_id="fp_other",
    path="Media/other.mkv",
    checksum="zzz999",
    runtime_seconds=90,
    width=640,
    height=480,
)
fingerprinter.generate(fp_other)
assert fingerprinter.distance(
    fp_asset.get_fingerprint(), fp_other.get_fingerprint()
) > 0.0

# ensure_fingerprint must not overwrite an existing fingerprint.
before = fp_asset.get_fingerprint()
fingerprinter.ensure_fingerprint(fp_asset)
assert fp_asset.get_fingerprint() == before

# Replacement search finds the visual twin, not the unrelated file.
match = fingerprinter.find_match(
    fp_asset.get_fingerprint(),
    [fp_other, fp_twin],
)
assert match is not None
matched_asset, matched_distance = match
assert matched_asset.get_asset_id() == "fp_twin"
assert matched_distance == 0.0

# Fingerprint survives eviction (persists through serialization).
fp_asset.set_download_status(DownloadStatus.DOWNLOADED)
sample.add_media_asset(fp_asset)

tmp_dir_fp = _Path(tempfile.mkdtemp())
MetadataSerializer(built).save_to_directory(tmp_dir_fp)
loaded_fp = MetadataLoader().load(tmp_dir_fp)
reloaded_fp_media = next(
    m for m in loaded_fp.get_media() if m.get_id() == sample.get_id()
)
reloaded_fp_asset = next(
    a for a in reloaded_fp_media.get_media_assets()
    if a.get_asset_id() == "fp_original"
)
assert reloaded_fp_asset.get_fingerprint() == fp1

print("Keyframe fingerprinting verified.")


print("\n=== Testing Source Age (takedown risk) ===")

aged_asset = MediaAsset(asset_id="aged", path="Media/aged.mkv")
three_years_ago = (datetime.now() - timedelta(days=365 * 3)).isoformat()
ten_days_ago = (datetime.now() - timedelta(days=10)).isoformat()
aged_asset.add_source(
    "internet_archive", "old/ref.mkv", date_posted=three_years_ago
)
aged_asset.add_source("mirror", "new/ref.mkv", date_posted=ten_days_ago)

# Oldest source drives the age -> ~3 years -> low takedown risk.
assert aged_asset.get_source_age_days() > 365 * 2

# date_posted survives serialization on the source records.
sample.add_media_asset(aged_asset)
tmp_dir_age = _Path(tempfile.mkdtemp())
MetadataSerializer(built).save_to_directory(tmp_dir_age)
loaded_age = MetadataLoader().load(tmp_dir_age)
reloaded_age_media = next(
    m for m in loaded_age.get_media() if m.get_id() == sample.get_id()
)
reloaded_aged = next(
    a for a in reloaded_age_media.get_media_assets()
    if a.get_asset_id() == "aged"
)
assert any(s.get("date_posted") for s in reloaded_aged.get_sources())

print("Source age verified.")


print("\n=== Testing Scoring ===")

scorer = AssetScorer()

# A highly repurposable, non-seasonal, high-appeal asset should score
# HIGHER for broadcast than a seasonal, single-channel, low-appeal one.
evergreen = MediaAsset(asset_id="score_evergreen", path="Media/evergreen.mkv")
seasonal = MediaAsset(asset_id="score_seasonal", path="Media/seasonal.mkv")

hi = scorer.compute_broadcast_score(
    evergreen, channel_count=4, is_seasonal=False, appeal=9.0
)
lo = scorer.compute_broadcast_score(
    seasonal, channel_count=1, is_seasonal=True, appeal=2.0
)

assert hi > lo
assert 0.0 <= lo <= 10.0 and 0.0 <= hi <= 10.0
assert evergreen.get_broadcast_score() == hi

# Retention: a fragile (single young source), small item should be kept
# more aggressively than a durable (many old sources), huge item even at
# the same broadcast score.
fragile = MediaAsset(asset_id="score_fragile", path="Media/fragile.mkv", file_size=100)
fragile.set_broadcast_score(6.0)
fragile.add_source(provider="internet_archive", reference="only/one.mkv")

durable = MediaAsset(
    asset_id="score_durable",
    path="Media/durable.mkv",
    file_size=8 * 1024 * 1024 * 1024,  # 8 GiB, above the large-file cap
)
durable.set_broadcast_score(6.0)
durable.add_source(provider="internet_archive", reference="a.mkv")
durable.add_source(provider="mirror_archive", reference="b.mkv")
durable.add_source(provider="mirror_two", reference="c.mkv")
durable.add_source(provider="mirror_three", reference="d.mkv")

frag_ret = scorer.compute_retention_score(fragile)
dur_ret = scorer.compute_retention_score(durable)

assert frag_ret > dur_ret
assert fragile.get_retention_score() == frag_ret

# Pinning is a hard override.
pinned_asset = MediaAsset(asset_id="score_pinned", path="Media/pinned.mkv")
pinned_asset.set_retention_score(0.0)
pinned_asset.set_pinned(True)
assert scorer.should_evict(pinned_asset) is False

evictable = MediaAsset(asset_id="score_evictable", path="Media/evictable.mkv")
evictable.set_retention_score(0.0)
assert scorer.should_evict(evictable) is True

keeper = MediaAsset(asset_id="score_keeper", path="Media/keeper.mkv")
keeper.set_retention_score(9.0)
assert scorer.should_evict(keeper) is False

print("Scoring verified.")


print("\n=== Testing Rolling Cache ===")


class _StubEpisode:
    """Minimal stand-in with just the accessors RollingCache uses."""

    def __init__(self, ep_id, available):
        self._id = ep_id
        asset = MediaAsset(asset_id=ep_id, path=f"Media/{ep_id}.mkv")
        if available:
            asset.set_download_status(DownloadStatus.DOWNLOADED)
        self._assets = [asset]

    def get_media_assets(self):
        return self._assets


# Episodes 1..6; first 3 aired, ep 3-4-5 should be the window.
episodes = [_StubEpisode(f"ep{n}", available=(n <= 5)) for n in range(1, 7)]

cache = RollingCache(window_size=3)
plan = cache.plan_window(episodes, aired_count=2)

# Window = episodes[2:5] -> ep3, ep4, ep5 (all available -> keep).
assert [e._id for e in plan["keep"]] == ["ep3", "ep4", "ep5"]
assert plan["fetch"] == []
# Already aired and available -> ep1, ep2 are evictable.
assert [e._id for e in plan["evict"]] == ["ep1", "ep2"]

# A window episode with no file should land in "fetch", not "keep".
episodes2 = [_StubEpisode(f"fx{n}", available=(n != 3)) for n in range(1, 7)]
plan2 = cache.plan_window(episodes2, aired_count=2)
assert [e._id for e in plan2["fetch"]] == ["fx3"]


def _resident(asset_id, retention, size, pinned=False):
    a = MediaAsset(asset_id=asset_id, path=f"Media/{asset_id}.mkv")
    a.set_download_status(DownloadStatus.DOWNLOADED)
    a.set_retention_score(retention)
    a.file_size = size
    a.set_pinned(pinned)
    return a


low = _resident("rc_low", retention=1.0, size=100)
mid = _resident("rc_mid", retention=5.0, size=100)
high = _resident("rc_high", retention=9.0, size=100)
pinned = _resident("rc_pinned", retention=0.0, size=100, pinned=True)

assets = [high, low, pinned, mid]

# Total 400 bytes, budget 250 -> must free >=150 bytes (>=2 files).
evicted = cache.evict_to_budget(assets, budget_bytes=250)

assert "rc_low" in evicted
assert "rc_mid" in evicted
assert "rc_pinned" not in evicted
assert low.get_download_status() == DownloadStatus.MISSING
assert pinned.get_download_status() == DownloadStatus.DOWNLOADED

assert low.get_retention_score() == 1.0
assert low.needs_download() is True

assert cache.evict_to_budget([high], budget_bytes=1000) == []

print("Rolling cache verified.")
print("\nIntelligent content management tests passed.")
