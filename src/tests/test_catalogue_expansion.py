"""
VISTOR Catalogue Expansion Tests

Assisted / automatic discovery modes and the offline-safe Source URL
Discovery backend. No network, no downloads. Run standalone:
python src/tests/test_catalogue_expansion.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.config import Config
from metadata.services.discovery_loop import DiscoveryLoop
from metadata.services.enrichment.archive_search_source import ArchiveSearchSource


print("\n=== Testing Catalogue Expansion (assisted/automatic) ===")


class _FakeRecommender:
    def __init__(self, cands):
        self._cands = cands

    def recommend(self, tmdb_id, media_type="Movie", limit=8):
        return list(self._cands)


class _FakeSearch:
    """Deterministic Source URL Discovery stand-in (no network)."""

    def __init__(self, url):
        self._url = url

    def find_source_url(self, title, year=None, media_type="Movie"):
        return self._url


class _RecordingIngestor:
    def __init__(self):
        self.calls = 0

    def ingest_records(self, records, download=False):
        self.calls += 1
        return {"committed": len(records)}


class _StubBuilder:
    def build(self, url, overrides=None):
        return {"url": url, "overrides": overrides or {}}


def _make_loop(mode, cands, url, cap=0):
    cfg = Config()
    cfg.recommended_media = True
    cfg.recommendation_mode = mode
    cfg.max_auto_additions_per_week = cap
    loop = DiscoveryLoop(config=cfg, source_search=_FakeSearch(url))
    loop.recommender = _FakeRecommender(cands)
    loop.builder = _StubBuilder()
    loop.ingestor = _RecordingIngestor()
    return loop


_cands = [
    {"tmdb_id": 1, "title": "Alpha", "release_year": 1990, "media_type": "Movie"},
    {"tmdb_id": 2, "title": "Beta", "release_year": 1991, "media_type": "Movie"},
]

# Disabled by default -> no-op.
_off = DiscoveryLoop(config=Config(), source_search=_FakeSearch("x"))
_off.recommender = _FakeRecommender(_cands)
_r_off = _off.run_from_seed(123)
assert _r_off["suggested"] == [] and _r_off["committed"] == []
print("Discovery is a no-op when recommended_media is off.")

# suggest_only -> suggestions surface, nothing acquired.
_r_sug = _make_loop("suggest_only", _cands, "url").run_from_seed(123)
assert len(_r_sug["suggested"]) == 2
assert _r_sug["committed"] == [] and _r_sug["needs_confirm"] == []
print("suggest_only surfaces suggestions and acquires nothing.")

# assisted -> each candidate with a found URL is queued for confirm.
_loop_a = _make_loop("assisted", _cands, "https://archive.org/details/alpha")
_r_a = _loop_a.run_from_seed(123)
assert len(_r_a["needs_confirm"]) == 2
assert _loop_a.ingestor.calls == 0
assert all("source_url" in c for c in _r_a["needs_confirm"])
print("assisted queues candidates for confirm without downloading.")

# assisted with no URL found -> nothing queued.
_loop_none = _make_loop("assisted", _cands, None)
assert _loop_none.run_from_seed(123)["needs_confirm"] == []
print("assisted queues nothing when no source URL is found.")

# automatic -> ingests up to the weekly cap, rest skipped.
_loop_auto = _make_loop("automatic", _cands, "https://archive.org/details/a", cap=1)
_r_auto = _loop_auto.run_from_seed(123)
assert len(_r_auto["committed"]) == 1
assert len(_r_auto["skipped_cap"]) == 1
assert _loop_auto.ingestor.calls == 1
print("automatic honors max_auto_additions_per_week.")

# Source URL Discovery backend is offline-safe.
assert ArchiveSearchSource().find_source_url("") is None
print("ArchiveSearchSource returns None for empty input.")

print("Catalogue expansion tests passed.")
