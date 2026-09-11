"""
VISTOR Scheduling Tests

Breakpoint detection, broadcast modes, seasonal schedule selection, and
metadata-only authored schedule loading. Run standalone:
python src/tests/test_scheduling.py
"""

import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parent.parent))

from metadata.relationships.media_asset import MediaAsset
from metadata.services.fetchers.breakpoint_detector import BreakpointDetector
from scheduler.broadcast_modes import (
    OffMode,
    BetweenProgramsMode,
    MidProgramMode,
    create_broadcast_mode,
)
from scheduler.broadcast_event import BroadcastEvent
from core.clock import Clock
from scheduler.schedule_type import ScheduleType
from scheduler.schedule_loader import ScheduleLoader
from scheduler.scheduled_item import ScheduledItem


print("\n=== Testing Breakpoint Detection ===")

# Round-trip: breakpoints survive to_dictionary/from_dictionary.
asset = MediaAsset("bp1", "Media/Episodes/ep.mkv", runtime_seconds=1800)
asset.set_breakpoints([540, 1080])
restored = MediaAsset.from_dictionary(asset.to_dictionary())
assert restored.get_breakpoints() == [540, 1080]

# Parsers are pure: black+silence midpoints intersect within proximity.
det = BreakpointDetector()
log = (
    "black_start:539.5 black_end:541.0\n"
    "silence_start: 539.8\nsilence_end: 541.2\n"
    "black_start:1200.0 black_end:1201.0\n"   # no matching silence -> dropped
)
blacks = det._black_midpoints(log)
silences = det._silence_midpoints(log)
assert any(abs(b - s) <= det.PROXIMITY_SECONDS for b in blacks for s in silences)

# Tier 3 runtime fallback: even ~10-min spacing when no signals exist.
empty = MediaAsset("bp2", "Media/Episodes/ep2.mkv", runtime_seconds=1800)
fallback = det._runtime_fallback(empty)
assert fallback == [600, 1200]
# Short clip -> no fabricated breaks.
short_asset = MediaAsset("bp3", "Media/Episodes/ep3.mkv", runtime_seconds=300)
assert det._runtime_fallback(short_asset) == []

print("Breakpoint Detection verified.")


print("\n=== Testing Broadcast Modes ===")


class _FakeProgram:
    """Minimal program stand-in exposing breakpoints + runtime."""

    def __init__(self, name, breakpoints=None, runtime_seconds=0):
        self.name = name
        self._breakpoints = list(breakpoints or [])
        self._runtime = runtime_seconds

    def get_breakpoints(self):
        return self._breakpoints

    def get_runtime_seconds(self):
        return self._runtime

    def __str__(self):
        return self.name


def _is_event(item):
    return isinstance(item, BroadcastEvent)


programs = [_FakeProgram("A"), _FakeProgram("B")]

# Off: unchanged order, no events.
off = OffMode().build_sequence(programs)
assert off == programs
assert not any(_is_event(i) for i in off)
print("OffMode airs programs in order with no events.")

# Between Programs: one commercial block after each program.
between = BetweenProgramsMode().build_sequence(programs)
assert len(between) == 4
assert not _is_event(between[0]) and _is_event(between[1])
assert not _is_event(between[2]) and _is_event(between[3])
print("BetweenProgramsMode inserts a block after each program.")

# Mid-Program with stored breakpoints: one block per breakpoint.
with_breaks = [_FakeProgram("C", breakpoints=[300, 600])]
mid = MidProgramMode().build_sequence(with_breaks)
assert not _is_event(mid[0])
assert sum(1 for i in mid if _is_event(i)) == 2
print("MidProgramMode inserts one block per stored breakpoint.")

# Mid-Program fallback: no breakpoints, 25 min -> breaks at 600 & 1200.
no_breaks = [_FakeProgram("D", runtime_seconds=25 * 60)]
mid_fallback = MidProgramMode().build_sequence(no_breaks)
assert sum(1 for i in mid_fallback if _is_event(i)) == 2
print("MidProgramMode falls back to runtime-spaced blocks.")

# Mid-Program short program: no breakpoints, airs whole.
short_prog = [_FakeProgram("E", runtime_seconds=5 * 60)]
mid_short = MidProgramMode().build_sequence(short_prog)
assert not any(_is_event(i) for i in mid_short)
print("MidProgramMode airs short programs whole.")

# Factory maps each Config string (and defaults unknowns to Off).
assert isinstance(create_broadcast_mode("off"), OffMode)
assert isinstance(create_broadcast_mode("between_programs"), BetweenProgramsMode)
assert isinstance(create_broadcast_mode("mid_program"), MidProgramMode)
assert isinstance(create_broadcast_mode("garbage"), OffMode)
print("create_broadcast_mode maps every Config value.")

print("Broadcast mode tests passed.")


print("\n=== Testing Seasonal Schedule Selection ===")

_clock = Clock()


def _sched_for(year, month, day):
    _clock.current_time = datetime(year, month, day, 12, 0, 0)
    return _clock.get_schedule_type()


# Fixed-date holidays.
assert _sched_for(2026, 1, 1) == ScheduleType.NEW_YEARS_DAY
assert _sched_for(2026, 2, 14) == ScheduleType.VALENTINES_DAY
assert _sched_for(2026, 3, 17) == ScheduleType.ST_PATRICKS_DAY
assert _sched_for(2026, 7, 4) == ScheduleType.INDEPENDENCE_DAY
assert _sched_for(2026, 10, 31) == ScheduleType.HALLOWEEN
assert _sched_for(2026, 12, 24) == ScheduleType.CHRISTMAS_EVE
assert _sched_for(2026, 12, 25) == ScheduleType.CHRISTMAS_DAY
assert _sched_for(2026, 12, 31) == ScheduleType.NEW_YEARS_EVE

# Thanksgiving = the fourth Thursday of November (found dynamically).
_nov_thursdays = [d for d in range(1, 31) if datetime(2026, 11, d).weekday() == 3]
_fourth_thursday = _nov_thursdays[3]
assert _sched_for(2026, 11, _fourth_thursday) == ScheduleType.THANKSGIVING

# Summer months (June-August) select the SUMMER lineup.  
assert _sched_for(2026, 6, 15) == ScheduleType.SUMMER  
assert _sched_for(2026, 8, 1) == ScheduleType.SUMMER  
  
# A holiday-free, non-summer month (April) resolves by weekday/weekend.  
for _d in range(1, 8):  
    _st = _sched_for(2026, 4, _d)  
    if datetime(2026, 4, _d).weekday() < 5:  
        assert _st == ScheduleType.WEEKDAY  
    else:  
        assert _st == ScheduleType.WEEKEND

print("Seasonal schedule selection verified.")


print("\n=== Testing Authored Schedule Loading ===")

_tmp_sched = Path(tempfile.mkdtemp())
(_tmp_sched / "weekday.json").write_text(
    json.dumps({
        "schedule_type": "weekday",
        "name": "Weekday",
        "blocks": [
            {
                "name": "Primetime",
                "start_hour": 20, "start_minute": 0,
                "end_hour": 22, "end_minute": 0,
                "items": ["ep_test_001", "mv_test_002"],
            }
        ],
    }),
    encoding="utf-8",
)

_loader = ScheduleLoader(schedules_directory=_tmp_sched)
_loader.load()

_weekday = _loader.get_schedule(ScheduleType.WEEKDAY)
assert _weekday is not None

_blocks = _weekday.get_blocks()
assert len(_blocks) == 1

_items = _blocks[0].get_items()
assert len(_items) == 2
assert all(isinstance(i, ScheduledItem) for i in _items)
assert _items[0].get_media_id() == "ep_test_001"
assert _items[1].get_media_id() == "mv_test_002"
print("Authored schedule loading (media-by-id) verified.")

# An absent / empty directory falls back to the code defaults.
_empty = Path(tempfile.mkdtemp())
_loader2 = ScheduleLoader(schedules_directory=_empty)
_loader2.load()
assert _loader2.get_schedule(ScheduleType.WEEKDAY) is not None
assert _loader2.get_schedule(ScheduleType.HALLOWEEN) is not None
print("Default schedule fallback verified.")

print("Scheduling content tests passed.")
