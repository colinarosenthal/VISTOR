"""
VISTOR Playback Rendering Test Suite

Exercises the Player -> Renderer wiring headlessly (NullRenderer /
RecordingRenderer). Test 5 attempts real mpv playback and auto-skips when
libmpv is unavailable.

Run from the repo root: python test_playback.py
"""

import sys
import time
import tempfile
from pathlib import Path

sys.path.append("src")

from player.player import Player, PlaybackState
from player.renderer import NullRenderer, MpvRenderer, create_renderer


# ------------------------------------------------------------------
# Test doubles
# ------------------------------------------------------------------

class RecordingRenderer(NullRenderer):
    """Records every call so we can assert the Player drives it correctly."""

    def __init__(self):
        self.calls = []
        self.loaded_path = None

    def load(self, path):
        self.loaded_path = path
        self.calls.append(("load", path))

    def play(self):
        self.calls.append(("play",))

    def pause(self):
        self.calls.append(("pause",))

    def stop(self):
        self.calls.append(("stop",))

    def set_volume(self, level):
        self.calls.append(("set_volume", level))

    def set_mute(self, flag):
        self.calls.append(("set_mute", flag))

    def seek(self, seconds):
        self.calls.append(("seek", seconds))

    def names(self):
        return [c[0] for c in self.calls]


class _FakeAsset:
    """Minimal stand-in for MediaAsset (path + exists + runtime)."""

    def __init__(self, path):
        self.path = Path(path)

    def exists(self):
        return self.path.exists()

    def get_path(self):
        return self.path

    def get_runtime_seconds(self):
        return 5


class _FakeItem:
    """Minimal stand-in for a MediaItem the Player can play."""

    def __init__(self, title, assets):
        self._title = title
        self._assets = assets

    def get_title(self):
        return self._title

    def get_media_assets(self):
        return self._assets

    def get_runtime_minutes(self):
        return 1


class _OneShotSource:
    """MediaSource that hands out a single item once."""

    def __init__(self, item):
        self._item = item
        self._served = False

    def has_next(self):
        return not self._served

    def get_next(self):
        if self._served:
            return None
        self._served = True
        return self._item


class _FakeOverlay:
    """Minimal stand-in for an OSDOverlay enum member (has a .value)."""

    def __init__(self, value):
        self.value = value


# ------------------------------------------------------------------
# Test 1: Player drives the renderer through the transport lifecycle
# ------------------------------------------------------------------

print("\n=== Test 1: Player -> Renderer wiring ===")

# A real temp file so asset.exists() is True and the path resolves.
tmp = Path(tempfile.mkdtemp()) / "clip.mkv"
tmp.write_bytes(b"not a real video, just bytes for exists()")

item = _FakeItem("Test Clip", [_FakeAsset(tmp)])
renderer = RecordingRenderer()
player = Player(source=_OneShotSource(item), renderer=renderer)

# load_next -> load_item should open the resolved path on the renderer.
assert player.load_next() is True
assert renderer.loaded_path == str(tmp)
assert ("load", str(tmp)) in renderer.calls
assert player.get_state() == PlaybackState.STOPPED

# play / pause / stop must be mirrored onto the renderer.
player.play()
assert player.is_playing() is True
assert ("play",) in renderer.calls

player.pause()
assert ("pause",) in renderer.calls

player.play()
player.stop()
assert ("stop",) in renderer.calls
assert player.get_current_item() is None

print("Player -> Renderer wiring verified.")


# ------------------------------------------------------------------
# Test 2: volume + mute propagate to the renderer
# ------------------------------------------------------------------

print("\n=== Test 2: audio propagation to renderer ===")

renderer2 = RecordingRenderer()
player2 = Player(renderer=renderer2)

player2.set_volume(70)
assert ("set_volume", 70) in renderer2.calls
assert player2.get_volume() == 70

player2.set_mute(True)
assert ("set_mute", True) in renderer2.calls
assert player2.is_muted() is True

print("Audio propagation verified.")


# ------------------------------------------------------------------
# Test 3: missing-file items don't crash (renderer gets no load)
# ------------------------------------------------------------------

print("\n=== Test 3: missing-asset safety ===")

missing_item = _FakeItem("Gone", [_FakeAsset("Media/does_not_exist.mkv")])
renderer3 = RecordingRenderer()
player3 = Player(renderer=renderer3)

assert player3.load_item(missing_item) is True     # headless load still succeeds
assert "load" not in renderer3.names()             # but nothing was opened

print("Missing-asset safety verified.")


# ------------------------------------------------------------------
# Test 4: NullRenderer + create_renderer fallback are headless-safe
# ------------------------------------------------------------------

print("\n=== Test 4: headless renderer fallback ===")

null = NullRenderer()
null.load("anything.mkv")
null.play()
null.render_osd(None)
null.shutdown()

# On a box with no libmpv/display this returns a NullRenderer, not a crash.
auto = create_renderer(fullscreen=False)
auto.set_volume(50)
auto.render_osd(None)
auto.shutdown()

print("Headless renderer fallback verified.")


# ------------------------------------------------------------------
# Test 5: real mpv playback (auto-skips if unavailable)
# ------------------------------------------------------------------

print("\n=== Test 5: real mpv playback (auto-skips if unavailable) ===")

try:
    renderer5 = create_renderer(fullscreen=False)
except Exception as exc:
    renderer5 = None
    print(f"SKIP: could not build a renderer ({exc}).")

if not isinstance(renderer5, MpvRenderer):
    print("SKIP: mpv unavailable; create_renderer() fell back to NullRenderer.")
else:
    media_root = Path("Media")
    exts = {".mkv", ".mp4", ".webm", ".avi", ".mov", ".mp3", ".m4a", ".flac"}
    candidates = [
        p for p in media_root.rglob("*") if p.suffix.lower() in exts
    ] if media_root.exists() else []

    if not candidates:
        print("SKIP: no media files found under Media/ to play.")
        renderer5.shutdown()
    else:
        target = candidates[0]
        print(f"Playing: {target}")

        renderer5.load(str(target))
        renderer5.play()
        time.sleep(2.0)

        backend = getattr(renderer5, "_mpv", None)
        pos = backend.time_pos if backend is not None else None
        print(f"time_pos after ~2s: {pos}")

        renderer5.set_volume(60)
        renderer5.set_mute(True)
        renderer5.stop()
        renderer5.shutdown()

        assert pos is not None, "mpv did not report a playback position."
        print("Real mpv playback verified.")


# ------------------------------------------------------------------
# Test 6: MpvRenderer._format_overlay (pure function)
# ------------------------------------------------------------------

print("\n=== Test 6: MpvRenderer._format_overlay (pure function) ===")

# _format_overlay is a pure method; call it unbound so no libmpv is needed.
fmt = MpvRenderer._format_overlay

banner = fmt(None, _FakeOverlay("channel_banner"),
             {"number": 3, "name": "VISTOR Toons", "program": "Rugrats"})
assert "VISTOR Toons" in banner and "Rugrats" in banner

info = fmt(None, _FakeOverlay("program_info"),
          {"title": "Doug", "channel_name": "VISTOR Toons"})
assert "Doug" in info and "VISTOR Toons" in info

assert fmt(None, _FakeOverlay("volume"), {"level": 40, "muted": False}) == "Volume 40"
assert fmt(None, _FakeOverlay("volume"), {"level": 40, "muted": True}) == "Muted"
assert fmt(None, _FakeOverlay("mute"), {"muted": True}) == "Muted"
assert fmt(None, _FakeOverlay("clock"), {"time": "8:30 PM"}) == "8:30 PM"

settings_text = fmt(None, _FakeOverlay("settings"),
                    {"rows": [{"label": "Captions", "value": "On", "selected": True}]})
assert "SETTINGS" in settings_text
assert "Captions" in settings_text and "On" in settings_text

print("Overlay formatting verified.")

# ------------------------------------------------------------------
# Test 7: set_renderer swaps backend + resurfaces the in-progress item
# ------------------------------------------------------------------

print("\n=== Test 7: set_renderer swaps backend + resurfaces item ===")

# A real temp file so _resolve_source_path resolves and the item resurfaces.
resurface_tmp = Path(tempfile.mkdtemp()) / "live.mkv"
resurface_tmp.write_bytes(b"not a real video, just bytes for exists()")

player7 = Player()
player7.set_source(_OneShotSource(_FakeItem("Live Show", [_FakeAsset(resurface_tmp)])))
assert player7.load_next() is True
player7.set_volume(65)
player7.set_mute(True)
player7.play()

new_renderer = RecordingRenderer()
player7.set_renderer(new_renderer)

# Audio state pushed onto the new backend.
assert ("set_volume", 65) in new_renderer.calls
assert ("set_mute", True) in new_renderer.calls

# In-progress item resurfaced (load + play, since state is PLAYING).
assert any(c[0] == "load" for c in new_renderer.calls)
assert ("play",) in new_renderer.calls

print("set_renderer resurface verified.")


print("\nAll playback rendering tests passed.")

# ------------------------------------------------------------------
# Test 8: set_renderer resumes mid-program (position-sync)
# ------------------------------------------------------------------

print("\n=== Test 8: set_renderer resumes mid-program (position-sync) ===")

sync_tmp = Path(tempfile.mkdtemp()) / "midprogram.mkv"
sync_tmp.write_bytes(b"not a real video, just bytes for exists()")

player8 = Player()
player8.set_source(_OneShotSource(_FakeItem("Mid Show", [_FakeAsset(sync_tmp)])))
assert player8.load_next() is True
player8.play()
player8.tick(3)                       # advance 3s into the program (duration 5s)
assert player8.get_position() == 3

resume_renderer = RecordingRenderer()
player8.set_renderer(resume_renderer)

# The new backend is loaded, sought to the tracked position, then played.
assert ("load", str(sync_tmp)) in resume_renderer.calls
assert ("seek", 3) in resume_renderer.calls
assert ("play",) in resume_renderer.calls

print("Position-sync verified.")
