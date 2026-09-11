"""
VISTOR Broadcast Modes

Concrete airing strategies injected into the BroadcastController. Each
mode takes the programs in the Scheduler's current block and returns the
full airing sequence, interleaving BroadcastEvents (commercial blocks)
per the viewer's chosen broadcast structure.

  off              -> programs in order, no interruptions
  between_programs -> a commercial block after each completed program
  mid_program      -> commercial blocks at authentic breakpoints inside
                      each program (falls back to runtime-spaced breaks)

See Docs/VISTOR_Design_Bible.md -> Broadcast Modes.
"""

from core.logger import Logger

from scheduler.broadcast_event import make_commercial_block


# Runtime-spacing fallback when a program has no detected breakpoints.
_FALLBACK_BREAK_SPACING_SECONDS = 10 * 60


class BroadcastMode:
    """Base contract: turn a block's programs into an airing sequence."""

    def build_sequence(self, items):
        """Return the full airing order for `items` (programs)."""
        raise NotImplementedError


class OffMode(BroadcastMode):
    """Air programs in order with no interruptions (parity with mode=None)."""

    def build_sequence(self, items):
        return list(items)


class BetweenProgramsMode(BroadcastMode):  
    """Insert one commercial block after each completed program."""  
  
    def __init__(self, commercial_selector=None):  
        self.commercial_selector = commercial_selector  
  
    def build_sequence(self, items):  
        sequence = []  
  
        for item in items:  
            sequence.append(item)  
            sequence.append(_make_break(self.commercial_selector))  
  
        return sequence  
  
  
class MidProgramMode(BroadcastMode):  
    """Split each program at its breakpoints, inserting commercial blocks.  
    (docstring unchanged)  
    """  
  
    def __init__(self, commercial_selector=None):  
        self.commercial_selector = commercial_selector  
  
    def build_sequence(self, items):  
        sequence = []  
  
        for item in items:  
            breakpoints = _extract_breakpoints(item)  
  
            if not breakpoints:  
                breakpoints = _generate_runtime_breakpoints(item)  
  
            sequence.append(item)  
  
            for _offset in breakpoints:  
                sequence.append(_make_break(self.commercial_selector))  
  
        return sequence

def create_broadcast_mode(mode_name):
    """Map a Config.broadcast_mode string to a concrete mode instance."""

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
        return OffMode()

    return mode_class()


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

def _make_break(commercial_selector):  
    """Build a commercial block, filling it from the selector when present."""  
    commercials = (  
        commercial_selector.select()  
        if commercial_selector is not None else None  
    )  
    return make_commercial_block(items=commercials)

def create_broadcast_mode(mode_name, commercial_selector=None):  
    """Map a Config.broadcast_mode string to a concrete mode instance."""  
  
    if mode_name == "between_programs":  
        return BetweenProgramsMode(commercial_selector)  
    if mode_name == "mid_program":  
        return MidProgramMode(commercial_selector)  
    if mode_name == "off":  
        return OffMode()  
  
    Logger.warning(f"Unknown broadcast mode '{mode_name}'; defaulting to Off.")  
    return OffMode()
