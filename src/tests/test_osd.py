"""
VISTOR OSD Tests

OSD Manager phase lifecycle and fade animations (standalone).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from osd.osd_manager import OSDManager, OSDOverlay, OSDPhase


print("=== Testing OSD Manager ===")

osd = OSDManager(visible_duration=5.0, fade_duration=0.4)

osd.show_volume(level=60, muted=False)
assert osd.get_overlay() == OSDOverlay.VOLUME
assert osd.phase == OSDPhase.FADE_IN

osd.tick(0.4)                       # finish fade in
assert osd.phase == OSDPhase.VISIBLE
assert osd.get_opacity() == 1.0

osd.tick(5.0)                       # hold elapses -> fade out
assert osd.phase == OSDPhase.FADE_OUT

osd.tick(0.4)                       # fade out completes -> hidden
assert not osd.is_visible()
assert osd.get_overlay() == OSDOverlay.NONE

print("OSD Manager verified.")


print("\n=== Testing Fade Animations ===")

fade = OSDManager(visible_duration=5.0, fade_duration=1.0)

# Fresh overlay begins fading in from 0.
fade.show_clock("12:00 PM")
assert fade.get_phase() == OSDPhase.FADE_IN
assert fade.is_fading() is True
assert fade.get_opacity() == 0.0                   # eased(0) == 0

# Partway through the fade-in, opacity is strictly between 0 and 1.
fade.tick(0.5)                                      # halfway through 1.0s fade
mid_in = fade.get_opacity()
assert 0.0 < mid_in < 1.0

# Completing the fade-in reaches full opacity and the VISIBLE phase.
fade.tick(0.6)                                      # crosses fade_duration
assert fade.get_phase() == OSDPhase.VISIBLE
assert fade.get_opacity() == 1.0
assert fade.is_fading() is False

# Hold elapses, then a partial fade-out sits strictly between 1 and 0.
fade.tick(5.1)                                      # VISIBLE -> FADE_OUT
assert fade.get_phase() == OSDPhase.FADE_OUT
fade.tick(0.5)                                      # halfway through fade-out
mid_out = fade.get_opacity()
assert 0.0 < mid_out < 1.0

# Smoothstep is symmetric: fade-out midpoint mirrors fade-in midpoint.
assert abs(mid_out - (1.0 - mid_in)) < 1e-9

# Finishing the fade-out hides the overlay.
fade.tick(0.6)
assert fade.is_visible() is False

print("Fade animations verified.")
print("\nOSD tests passed.")
