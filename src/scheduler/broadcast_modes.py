"""  
VISTOR Broadcast Modes  
  
Concrete airing strategies injected into the BroadcastController. Each  
mode takes the programs in the Scheduler's current block and returns the  
full airing sequence, interleaving BroadcastEvents (commercial blocks,  
station IDs, network promos) per the viewer's chosen broadcast structure.  
  
  off              -> programs in order, no interruptions  
  between_programs -> a commercial block after each completed program  
  mid_program      -> commercial blocks at authentic breakpoints inside  
                      each program (falls back to runtime-spaced breaks)  
  
Each mode may be given optional PoolSelectors that fill its breaks from a  
channel's pools. When a selector is None (or its pool is empty), that  
content is simply omitted, so a channel with empty pools reproduces the  
unchanged legacy behavior (one empty placeholder commercial block per  
break).  
  
See Docs/VISTOR_Design_Bible.md -> Broadcast Modes.  
"""  
  
from core.logger import Logger  
  
from scheduler.broadcast_event import (  
    make_commercial_block,  
    make_network_promo,  
    make_station_id,  
)  
  
  
# Runtime-spacing fallback when a program has no detected breakpoints.  
_FALLBACK_BREAK_SPACING_SECONDS = 10 * 60  
  
  
class BroadcastMode:  
    """Base contract: turn a block's programs into an airing sequence."""  
  
    def __init__(self, selector=None, promo_selector=None,  
                 station_id_selector=None):  
        # Optional PoolSelectors used to fill breaks. When None, the  
        # corresponding content is omitted (legacy behavior for commercials  
        # is an empty placeholder block).  
        self.selector = selector  
        self.promo_selector = promo_selector  
        self.station_id_selector = station_id_selector  
  
    def build_sequence(self, items):  
        """Return the full airing order for `items` (programs)."""  
        raise NotImplementedError  
  
    def _break(self):  
        """Build the events for one break from this mode's selectors."""  
        return _make_break(  
            self.selector,  
            self.promo_selector,  
            self.station_id_selector,  
        )  
  
  
class OffMode(BroadcastMode):  
    """Air programs in order with no interruptions (parity with mode=None)."""  
  
    def build_sequence(self, items):  
        return list(items)  
  
  
class BetweenProgramsMode(BroadcastMode):  
    """Insert one commercial block after each completed program."""  
  
    def build_sequence(self, items):  
        sequence = []  
  
        for item in items:  
            sequence.append(item)  
            sequence.extend(self._break())  
  
        return sequence  
  
  
class MidProgramMode(BroadcastMode):  
    """Split each program at its breakpoints, inserting commercial blocks.  
  
    Uses breakpoints detected at download time (BreakpointDetector). A  
    program with no known breakpoints falls back to runtime-spaced breaks;  
    a program that exposes neither breakpoints nor a runtime airs whole,  
    degrading gracefully to Off behavior for that item.  
  
    NOTE: the item-based Player/PlaybackQueue cannot split a single file  
    mid-play yet (ROADMAP KNOWN LIMITATION). Until it can, the program is  
    enqueued once and the breakpoints drive how many commercial blocks  
    follow it, which keeps the sequence correct for scheduling/testing.  
    """  
  
    def build_sequence(self, items):  
        sequence = []  
  
        for item in items:  
            breakpoints = _extract_breakpoints(item)  
  
            if not breakpoints:  
                breakpoints = _generate_runtime_breakpoints(item)  
  
            sequence.append(item)  
  
            for _offset in breakpoints:  
                sequence.extend(self._break())  
  
        return sequence  
  
  
def _make_break(selector=None, promo_selector=None, station_id_selector=None):  
    """Build the events for one break.  
  
    Always emits a commercial block (filled from `selector` when present,  
    otherwise an empty placeholder) so the break count matches legacy  
    behavior. A station ID is added before, and a network promo after, only  
    when their selector actually yields items.  
    """  
    events = []  
  
    if station_id_selector is not None:  
        station_ids = station_id_selector.select()  
        if station_ids:  
            events.append(make_station_id(items=station_ids))  
  
    commercials = selector.select() if selector is not None else None  
    events.append(make_commercial_block(items=commercials))  
  
    if promo_selector is not None:  
        promos = promo_selector.select()  
        if promos:  
            events.append(make_network_promo(items=promos))  
  
    return events  
  
  
def create_broadcast_mode(mode_name, selector=None, promo_selector=None,  
                          station_id_selector=None):  
    """Map a Config.broadcast_mode string to a concrete mode instance.  
  
    `selector`, `promo_selector`, and `station_id_selector` are optional  
    PoolSelectors the mode uses to fill its breaks. When None, that content  
    is omitted (empty placeholder commercial blocks; no station IDs/promos).  
    """  
  
    modes = {  
        "off": OffMode,  
        "between_programs": BetweenProgramsMode,  
        "mid_program": MidProgramMode,  
    }  
  
    mode_class = modes.get(mode_name)  
  
    if mode_class is None:  
        Logger.warning(  
            f"Unknown broadcast mode '{mode_name}'; defaulting to Off."  
        )  
        mode_class = OffMode  
  
    return mode_class(  
        selector,  
        promo_selector=promo_selector,  
        station_id_selector=station_id_selector,  
    )  
  
  
# ----------------------------------------------------------------------  
# Item introspection helpers (duck-typed so any program item works)  
# ----------------------------------------------------------------------  
  
def _extract_breakpoints(item):  
    """Best-effort read of an item's detected breakpoint offsets."""  
  
    if hasattr(item, "get_breakpoints"):  
        try:  
            return list(item.get_breakpoints() or [])  
        except Exception:  # noqa: BLE001  
            pass  
  
    asset = _extract_asset(item)  
    if asset is not None and hasattr(asset, "get_breakpoints"):  
        try:  
            return list(asset.get_breakpoints() or [])  
        except Exception:  # noqa: BLE001  
            pass  
  
    return []  
  
  
def _extract_runtime(item):  
    """Best-effort read of an item's runtime in seconds (0 if unknown)."""  
  
    for getter in ("get_runtime_seconds", "get_runtime", "get_duration"):  
        if hasattr(item, getter):  
            try:  
                value = getattr(item, getter)()  
                if value:  
                    return int(value)  
            except Exception:  # noqa: BLE001  
                pass  
  
    asset = _extract_asset(item)  
    if asset is not None and hasattr(asset, "get_runtime_seconds"):  
        try:  
            return int(asset.get_runtime_seconds() or 0)  
        except Exception:  # noqa: BLE001  
            pass  
  
    return 0  
  
  
def _extract_asset(item):  
    """Return an item's MediaAsset if it exposes one, else None."""  
  
    if hasattr(item, "get_asset"):  
        try:  
            return item.get_asset()  
        except Exception:  # noqa: BLE001  
            return None  
  
    return None  
  
  
def _generate_runtime_breakpoints(item):  
    """Evenly spaced fallback breakpoints (~every 10 min) inside a program."""  
  
    runtime = _extract_runtime(item)  
  
    if runtime <= _FALLBACK_BREAK_SPACING_SECONDS:  
        return []  
  
    offsets = []  
    offset = _FALLBACK_BREAK_SPACING_SECONDS  
  
    while offset < runtime:  
        offsets.append(offset)  
        offset += _FALLBACK_BREAK_SPACING_SECONDS  
  
    return offsets