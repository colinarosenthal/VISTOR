"""
VISTOR Engine Tests

The full engine-driven pipeline: broadcast pipeline, channel manager
time-sync, remote controller, channel banner/OSD indicators, program
information, clock overlay, TV guide, and the settings menu.
"""

import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from metadata.services.metadata_population import MetadataPopulation
from engine.engine import Engine
from remote.remote_controller import RemoteController
from osd.osd_manager import OSDManager, OSDOverlay, OSDPhase


# Shared media library for the pipeline tests.
population = MetadataPopulation()
built = population.build_library()


# ------------------------------------------------------------------
# Engine Broadcast Pipeline
# ------------------------------------------------------------------

print("\n=== Testing Engine Broadcast Pipeline ===")

engine = Engine()
engine.initialize()

channel = engine.channel_manager.get_active_channel()

channel.scheduler.update()          # resolve current_block from the shared clock
current_block = channel.scheduler.get_current_block()
assert current_block is not None    # default block spans 00:00-23:59

for movie in built.get_movies():
    current_block.add_item(movie)

engine.update()
engine.update()

assert channel.queue.size() >= 1
print("Engine broadcast pipeline verified.")


# ------------------------------------------------------------------
# Channel Manager (time sync)
# ------------------------------------------------------------------

print("\n=== Testing Channel Manager (time sync) ===")

engine = Engine()
engine.initialize()   # builds clock, scheduler, channel_manager (from loader), osd

manager = engine.channel_manager
assert manager.count() >= 2

engine.update()
engine.update()

before = manager.get_active_channel().get_number()
manager.channel_up()
assert manager.get_active_channel().get_number() != before   # advanced
manager.previous_channel()
assert manager.get_active_channel().get_number() == before    # previous returns

print("Channel Manager verified.")


# ------------------------------------------------------------------
# Remote Controller
# ------------------------------------------------------------------

print("\n=== Testing Remote Controller ===")

manager = engine.channel_manager
remote = RemoteController(manager, engine)

remote.press("channel_up")
remote.press("channel_down")

remote.press("digit_4")
remote.press("enter")
assert manager.get_active_channel().get_number() == 4

remote.press("prev")
remote.press("power")    # unknown key should warn, not crash

remote.press("clock")
assert engine.osd.get_overlay() == OSDOverlay.CLOCK
assert engine.osd.is_visible() is True
engine.osd.hide()   # reset so later overlay assertions start clean

print("Remote Controller verified.")


# ------------------------------------------------------------------
# Channel Banner + OSD Indicators
# ------------------------------------------------------------------

print("\n=== Testing Channel Banner + OSD Indicators ===")

assert engine.channel_manager is not None
assert engine.osd is not None
assert engine.channel_manager.count() >= 1

# --- Channel Banner fires on channel change ---
engine.channel_up()
assert engine.osd.is_visible() is True
assert engine.osd.get_overlay() == OSDOverlay.CHANNEL_BANNER

banner = engine.osd.get_payload()
active = engine.channel_manager.get_active_channel()
assert banner["number"] == active.get_number()
assert banner["name"] == active.get_name()

# --- Auto-hide (tick advances one phase per call) ---
engine.osd.tick(engine.osd.fade_duration + 0.1)      # FADE_IN  -> VISIBLE
engine.osd.tick(engine.osd.visible_duration + 0.1)   # VISIBLE  -> FADE_OUT
engine.osd.tick(engine.osd.fade_duration + 0.1)      # FADE_OUT -> HIDDEN
assert engine.osd.is_visible() is False

# --- Volume Indicator ---
engine.volume_up()
assert engine.osd.get_overlay() == OSDOverlay.VOLUME
assert engine.osd.get_payload()["level"] == active.get_player().get_volume()
engine.osd.hide()

# --- Mute Indicator ---
engine.toggle_mute()
assert engine.osd.get_overlay() == OSDOverlay.MUTE
assert engine.osd.get_payload()["muted"] == active.get_player().is_muted()

print("Channel banner + OSD indicators verified.")


# ------------------------------------------------------------------
# Program Information
# ------------------------------------------------------------------

print("\n=== Testing Program Information ===")

active = engine.channel_manager.get_active_channel()
active_block = active.get_current_block()
assert active_block is not None

info_movie = built.get_movies()[0]
active_block.add_item(info_movie)

engine.update()
engine.update()

engine.show_info()
assert engine.osd.is_visible() is True
assert engine.osd.get_overlay() == OSDOverlay.PROGRAM_INFO

info = engine.osd.get_payload()
assert info["number"] == active.get_number()
assert info["channel_name"] == active.get_name()
if active.get_player().get_current_item() is not None:
    assert info["title"] == active.get_player().get_current_item().get_title()
assert "rating" in info
assert isinstance(info["genres"], list)

engine.osd.tick(engine.osd.fade_duration + 0.1)      # FADE_IN  -> VISIBLE
engine.osd.tick(engine.osd.visible_duration + 0.1)   # VISIBLE  -> FADE_OUT
engine.osd.tick(engine.osd.fade_duration + 0.1)      # FADE_OUT -> HIDDEN
assert engine.osd.is_visible() is False

print("Program Information verified.")


# ------------------------------------------------------------------
# Clock Overlay
# ------------------------------------------------------------------

print("\n=== Testing Clock Overlay ===")

engine.show_clock()
assert engine.osd.is_visible() is True
assert engine.osd.get_overlay() == OSDOverlay.CLOCK

clock_payload = engine.osd.get_payload()
assert "time" in clock_payload
assert isinstance(clock_payload["time"], str)
assert clock_payload["time"]                       # non-empty
assert ("AM" in clock_payload["time"]) or ("PM" in clock_payload["time"])

engine.osd.tick(engine.osd.fade_duration + 0.1)    # FADE_IN  -> VISIBLE
engine.osd.tick(engine.osd.visible_duration + 0.1) # VISIBLE  -> FADE_OUT
engine.osd.tick(engine.osd.fade_duration + 0.1)    # FADE_OUT -> HIDDEN
assert engine.osd.is_visible() is False

print("Clock overlay verified.")


# ------------------------------------------------------------------
# TV Guide
# ------------------------------------------------------------------

print("\n=== Testing TV Guide ===")

assert engine.guide is not None

engine.open_guide()
assert engine.guide.is_open() is True
assert engine.guide.get_row_count() == engine.channel_manager.count()

first_row = engine.guide.get_rows()[0]
first_channel = engine.channel_manager.get_channels()[0]
assert first_row["number"] == first_channel.get_number()
assert first_row["name"] == first_channel.get_name()

assert engine.guide.get_current_program(0) is not None
assert engine.guide.get_upcoming_program(0) is not None

time_text = engine.guide.get_time_text()
assert isinstance(time_text, str) and time_text
assert ("AM" in time_text) or ("PM" in time_text)

assert engine.guide.get_selected_row() == 0
engine.guide_down()
if engine.channel_manager.count() > 1:
    assert engine.guide.get_selected_row() == 1
engine.guide_up()
assert engine.guide.get_selected_row() == 0
engine.guide_up()                     # clamp at top
assert engine.guide.get_selected_row() == 0

engine.close_guide()
assert engine.guide.is_open() is False

print("TV Guide verified.")


# ------------------------------------------------------------------
# Settings Menu
# ------------------------------------------------------------------

print("\n=== Testing Settings Menu ===")

engine.config.captions_enabled = True
engine.config.broadcast_mode = "mid_program"
engine.config.save()
with open(engine.config.path, encoding="utf-8") as handle:
    on_disk = json.load(handle)
assert on_disk["captions_enabled"] is True
assert on_disk["broadcast_mode"] == "mid_program"
print("Settings persistence verified.")

assert engine.settings_menu is not None
assert engine.config is not None

remote.press("settings")
assert engine.settings_menu.is_open() is True
assert engine.osd.get_overlay() == OSDOverlay.SETTINGS

rows = engine.osd.get_payload()["rows"]
assert len(rows) == 6
assert rows[0]["selected"] is True          # cursor starts at the top

# --- bytes field: storage budget steps by 1 GiB and clamps at 0 ---
engine.config.storage_budget_bytes = 0
engine.settings_menu.selected_row = 0
engine.settings_right()
assert engine.config.storage_budget_bytes == 1024 * 1024 * 1024
engine.settings_left()
engine.settings_left()                      # clamp at 0, never negative
assert engine.config.storage_budget_bytes == 0

# --- choice field: broadcast_mode cycles Off / Between / Mid ---
engine.settings_menu.selected_row = 1
engine.config.broadcast_mode = "off"
engine.settings_right()
assert engine.config.broadcast_mode == "between_programs"
engine.settings_right()
assert engine.config.broadcast_mode == "mid_program"
engine.settings_right()
assert engine.config.broadcast_mode == "off"   # wraps around

# --- bool field: captions toggle ---
engine.settings_menu.selected_row = 2
before = engine.config.captions_enabled
engine.settings_right()
assert engine.config.captions_enabled != before

# --- navigation clamps at both ends ---
engine.settings_menu.selected_row = 0
engine.settings_up()
assert engine.settings_menu.get_selected_row() == 0

engine.toggle_settings()
assert engine.settings_menu.is_open() is False

print("Settings Menu verified.")
print("\nEngine tests passed.")
