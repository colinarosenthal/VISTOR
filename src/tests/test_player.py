"""
VISTOR Player Tests

Player + PlaybackQueue transport lifecycle and volume/mute behavior
(headless, no renderer backend required).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from metadata.services import MetadataLibrary
from metadata.services.metadata_population import MetadataPopulation
from player.playback_queue import PlaybackQueue
from player.player import Player, PlaybackState


# Build a small populated library to feed the queue.
population = MetadataPopulation()
built = population.build_library()

library = MetadataLibrary()
for movie in built.get_movies():
    library.add_media(movie)


print("=== Testing Player + PlaybackQueue ===")

playback_queue = PlaybackQueue()
for media_item in library.get_media():
    playback_queue.enqueue(media_item)

player = Player()
player.set_source(playback_queue)

assert player.load_next() is True
assert player.get_current_item() is not None
assert player.get_state() == PlaybackState.STOPPED

player.play()
assert player.is_playing() is True

duration = player.get_duration()
player.tick(duration)
assert player.is_finished() is True
assert player.get_position() == duration

if player.load_next():
    assert player.get_position() == 0
    assert player.get_state() == PlaybackState.STOPPED

print("Player + PlaybackQueue verified.")


print("\n=== Testing Player Volume + Mute ===")

vol_player = Player()
assert vol_player.get_volume() == 50
assert vol_player.is_muted() is False

vol_player.volume_up()
assert vol_player.get_volume() == 55
vol_player.volume_down()
assert vol_player.get_volume() == 50

vol_player.set_volume(150)
assert vol_player.get_volume() == 100    # clamped high
vol_player.set_volume(-10)
assert vol_player.get_volume() == 0      # clamped low
vol_player.set_volume(40)

vol_player.toggle_mute()
assert vol_player.is_muted() is True
vol_player.toggle_mute()
assert vol_player.is_muted() is False

print("Player volume + mute verified.")
print("\nPlayer tests passed.")
