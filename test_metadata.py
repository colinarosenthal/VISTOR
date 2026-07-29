import sys  
import json
  
from pathlib import Path  
  
sys.path.append("src")  
  
  
# ------------------------------------------------------------------  
# Imports  
# ------------------------------------------------------------------  
  
from metadata.enums import *  
from metadata.vocabulary import *  
from metadata.library import *  
from metadata.media import *  
from metadata.relationships import *  
  
from metadata.services import (  
    MetadataLibrary,  
    MetadataSearch,  
    MetadataSerializer,  
    MetadataValidator,  
    MetadataLoader,  
)  
  
from metadata.services.metadata_population import MetadataPopulation  
  
from metadata.media.film.movie import Movie  
from metadata.media.television.episode import Episode  
from metadata.media.music.music_video import MusicVideo  
from metadata.media.advertising.commercial import Commercial 

from core.clock import Clock
  
  
print("\n=== Metadata Import Test ===")  
  
print("Metadata imports successful")  
  
  
# ------------------------------------------------------------------  
# Model Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing Metadata Models ===")  
  
  
print("Testing Person...")  
  
person = Person(  
    id="person_000001",  
    name="Test Person",  
)  
  
print(person)  
  
  
print("Testing Media Item...")  
  
program = MediaItem(  
    id="media_000001",  
    title="Test Program",  
)  
  
print(program)  
  
  
print("Testing Appearance Relationship...")  
  
appearance = Appearance(  
    id="appearance_000001",  
    person=person,  
    media_item=program,  
    role=RoleType.ACTOR,  
)  
  
print(appearance)  
  
  
# ------------------------------------------------------------------  
# Collection Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing Collections ===")  
  
  
collection = Collection(  
    title="Test Collection"  
)  
  
collection.add_item(program)  
  
print(collection)  
  
assert collection.get_item_count() == 1  
  
print(  
    "Collection items:",  
    collection.get_item_count()  
)  
  
  
# ------------------------------------------------------------------  
# Media Library Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing Media Library ===")  
  
  
media_library = MediaLibrary()  
  
media_library.add_movie(program)  
  
print(media_library)  
  
assert len(media_library.get_movies()) == 1  
  
print(  
    "Movies:",  
    len(media_library.get_movies())  
)  
  
  
# ------------------------------------------------------------------  
# Metadata Library Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing MetadataLibrary ===")  
  
  
metadata_library = MetadataLibrary()  
  
metadata_library.add_person(person)  
  
metadata_library.add_relationship(  
    appearance  
)  
  
print(metadata_library)  
  
assert len(metadata_library.get_people()) == 1  
  
assert len(metadata_library.get_relationships()) == 1  
  
print(  
    "People:",  
    len(metadata_library.get_people())  
)  
  
print(  
    "Relationships:",  
    len(metadata_library.get_relationships())  
)  
  
  
# ------------------------------------------------------------------  
# Metadata Search Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing MetadataSearch ===")  
  
  
search = MetadataSearch(  
    metadata_library  
)  
  
  
person_results = search.find_person(  
    "Test Person"  
)  
  
print(  
    "Person Search:",  
    person_results  
)  
  
  
assert len(person_results) == 1  
  
  
# ------------------------------------------------------------------  
# Metadata Serializer Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing MetadataSerializer ===")  
  
  
serializer = MetadataSerializer(  
    metadata_library  
)  
  
  
metadata_data = serializer.to_dictionary()  
  
  
print(metadata_data)  
  
  
assert "people" in metadata_data  
  
assert len(metadata_data["people"]) == 1  
  
  
# ------------------------------------------------------------------  
# Metadata Validator Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing MetadataValidator ===")  
  
  
validator = MetadataValidator()  
  
  
validation_result = validator.validate(  
    metadata_library  
)  
  
  
print(  
    "Validation Result:",  
    validation_result  
)  
  
  
assert validation_result is True  
  
  
# ------------------------------------------------------------------  
# Metadata Loader Tests  
# ------------------------------------------------------------------  
  
print("\n=== Testing MetadataLoader ===")  
  
  
loader = MetadataLoader()  
  
  
metadata_path = Path(  
    "Metadata/data"  
)
  
  
loaded_library = loader.load(  
    metadata_path  
)  
  
  
print(  
    loaded_library  
)  
  
  
assert loaded_library is not None  
  
  
print(  
    "Metadata loading pipeline complete"  
)  
  
  
# ------------------------------------------------------------------  
# Metadata Population  
# ------------------------------------------------------------------  
  
print("\n=== Testing Metadata Population ===")  
  
  
population = MetadataPopulation()  
  
genres = population.create_genres()  
  
print("Genres Created:", len(genres))  
  
for genre in genres:  
    print("-", genre)  
  
    print()  
  
print("Testing Music Genre Population...")  
  
music_genres = population.create_music_genres()  
  
print(  
    "Music Genres Created:",  
    len(music_genres)  
)  
  
for genre in music_genres:  
    print("-", genre)  
  
  
# ------------------------------------------------------------------  
# Library Assembly  
# ------------------------------------------------------------------  
  
print("\n=== Testing Library Assembly ===")  
  
  
library = population.build_library()  
  
media = library.get_media()  
  
movies = [m for m in media if isinstance(m, Movie)]  
episodes = [m for m in media if isinstance(m, Episode)]  
music_videos = [m for m in media if isinstance(m, MusicVideo)]  
commercials = [m for m in media if isinstance(m, Commercial)]  
  
print("Movies:", len(movies))  
print("Episodes:", len(episodes))  
print("Music videos:", len(music_videos))  
print("Commercials:", len(commercials))  
print("Total:", len(media))  
  
  
# Reference-sharing check  
advertisers = population.create_advertisers()  
products = population.create_products(advertisers)  
campaigns = population.create_campaigns(products)  
  
check_commercials = population.create_commercials(  
    advertisers,  
    products,  
    campaigns,  
)  
  
assert check_commercials[0].get_advertiser() is advertisers["coca_cola"]  
  
print("Reference sharing verified.")  
  
assert len(commercials) >= 1  
  
  
# ------------------------------------------------------------------  
# Serialization Round-Trip (media exercised)  
# ------------------------------------------------------------------  

from metadata.media.film.movie import Movie  
from metadata.media.television.episode import Episode  
from metadata.media.music.music_video import MusicVideo  
from metadata.media.advertising.commercial import Commercial

print("\n=== Testing Serialization Round-Trip ===")  
  
# Build a populated MetadataLibrary so the media buckets are actually written.  
round_trip_library = MetadataLibrary()  
  
# Carry the person over so people.json is still exercised too.  
round_trip_library.add_person(person)  
  
# build_library() returns a MediaLibrary; move its media into the  
# MetadataLibrary the serializer understands (get_media / add_media).  
built = population.build_library()  
  
for movie in built.get_movies():  
    round_trip_library.add_media(movie)  
  
for episode in built.get_episodes():  
    round_trip_library.add_media(episode)  
  
for video in built.get_music_videos():  
    round_trip_library.add_media(video)  
  
for commercial in built.get_commercials():  
    round_trip_library.add_media(commercial)

seen_seasons = {}  
seen_series = {}  
seen_franchises = {}  
  
for episode in built.get_episodes():  
    round_trip_library.add_media(episode)  
  
    season = episode.get_season()  
    if season and season.get_id() not in seen_seasons:  
        seen_seasons[season.get_id()] = season  
  
        series = season.get_series()  
        if series and series.get_id() not in seen_series:  
            seen_series[series.get_id()] = series  
  
            franchise = series.get_franchise()  
            if franchise and franchise.get_id() not in seen_franchises:  
                seen_franchises[franchise.get_id()] = franchise  
  
for franchise in seen_franchises.values():  
    round_trip_library.add_franchise(franchise)  
  
for series in seen_series.values():  
    round_trip_library.add_series(series)  
  
for season in seen_seasons.values():  
    round_trip_library.add_season(season)  
  
# Serialize to disk. Keep this path casing identical to the loader's.  
metadata_path = Path("Metadata/data")  
  
MetadataSerializer(round_trip_library).save_to_directory(metadata_path)  
  
print("Serialization round-trip complete")  
  
# Reload from disk.  
reloaded = MetadataLoader().load(metadata_path)  
  
loaded_media = reloaded.get_media()  
  
loaded_movies = [m for m in loaded_media if isinstance(m, Movie)]  
loaded_episodes = [m for m in loaded_media if isinstance(m, Episode)]  
loaded_music_videos = [m for m in loaded_media if isinstance(m, MusicVideo)]  
loaded_commercials = [m for m in loaded_media if isinstance(m, Commercial)]  
  
print("Loaded movies:", len(loaded_movies))  
print("Loaded episodes:", len(loaded_episodes))  
print("Loaded music videos:", len(loaded_music_videos))  
print("Loaded commercials:", len(loaded_commercials))  
print("Loaded total:", len(loaded_media))  
  
assert len(loaded_movies) >= 1  
assert len(loaded_music_videos) >= 1  
assert len(loaded_commercials) >= 1  
  
# Episodes need series/seasons serialized before they can reconstruct  
# (Episode.__init__ requires a Season). Enable once those buckets are written.  
assert len(loaded_episodes) >= 1  
  
# People bucket still round-trips.  
assert len(reloaded.get_people()) >= 1  
  
print("Serialization round-trip verified (media exercised).")  

# ----------------------------------------------------------------------  
# Media Verifier  
# ----------------------------------------------------------------------  
  
print("\n=== Testing MediaVerifier ===")  
  
from metadata.services.media_verifier import (  
    MediaVerifier,  
    normalize_filename,  
)  
from metadata.services.metadata_population import MetadataPopulation  
  
verifier_library = MetadataPopulation().build_library()  
  
verifier = MediaVerifier(verifier_library)  
report = verifier.verify()  
  
assert "total_media" in report  
assert "total_assets" in report  
assert isinstance(report["verified"], list)  
assert isinstance(report["missing"], list)  
  
print("Media items checked:", report["total_media"])  
print("Assets checked:", report["total_assets"])  
print("Verified:", len(report["verified"]))  
print("Missing:", len(report["missing"]))  
  
# Filename normalization checks  
assert normalize_filename("Friends S01E01 (Pilot).MKV") == "friends_s01e01_pilot.mkv"  
assert normalize_filename("  Weird##Name!!.MP4 ") == "weird_name.mp4"  
  
print("Filename normalization verified.")

# ----------------------------------------------------------------------  
# Media Scanner  
# ---------------------------------------------------------------------- 

from metadata.services.media_scanner import MediaScanner  
  
print("=== Testing MediaScanner ===")  
  
scan_report = MediaScanner().scan()  
  
print("Media files found:", scan_report["total_files"])  
  
# Scanning an empty/missing Media dir is valid; just assert shape.  
assert "files" in scan_report  
assert "total_files" in scan_report  
  
print("Media scan verified.")

# ----------------------------------------------------------------------  
# Media Associator
# ---------------------------------------------------------------------- 

print("\n=== Testing MediaAssociator ===")  
  
from metadata.services.media_associator import MediaAssociator  
  
# Reuse the populated library from the round-trip section.  
associator_library = built  
  
# Pick a real id from the library so the manifest matches something.  
first_media = associator_library.get_media()[0]  
sample_id = first_media.get_id()  
  
manifest_data = {  
    sample_id: "Movies/sample_placeholder.mkv"  
}  
  
manifest_path = Path("Metadata/data/asset_manifest.json")  
  
with open(manifest_path, "w", encoding="utf-8") as manifest_file:  
    json.dump(manifest_data, manifest_file, indent=4)  
  
associator = MediaAssociator(  
    associator_library,  
    Path("Media"),  
)  
  
assoc_report = associator.associate_from_manifest(manifest_path)  
  
print("Associated:", len(assoc_report["associated"]))  
print("Unmatched ids:", len(assoc_report["unmatched_ids"]))  
print("Missing files:", len(assoc_report["missing_files"]))  
  
assert len(assoc_report["associated"]) >= 1  
assert len(first_media.get_media_assets()) >= 1  
  
print("Media association verified.")

# ----------------------------------------------------------------------  
# Media Validator  
# ----------------------------------------------------------------------  
  
print("\n=== Testing MediaValidator ===")  
  
from metadata.services.media_validator import MediaValidator  
  
validator = MediaValidator(loaded_library)  
  
validation_report = validator.validate()  
  
print("Media checked:", validation_report["total_media"])  
print("Valid:", len(validation_report["valid"]))  
print("Without assets:", len(validation_report["media_without_assets"]))  
print("Missing asset files:", len(validation_report["missing_assets"]))  
  
# Resolve any dangling assets by dropping them.  
resolution_report = validator.resolve_missing_assets(strategy="drop")  
  
print("Dropped:", len(resolution_report["dropped"]))  
print("Flagged:", len(resolution_report["flagged"]))  
  
# After a "drop" pass, re-validation should report no missing asset files.  
post_report = validator.validate()  
  
assert len(post_report["missing_assets"]) == 0  
  
print("Media validation verified.")

print("=== Testing Player + PlaybackQueue ===")  
  
from player.playback_queue import PlaybackQueue  
from player.player import Player, PlaybackState  
  
# Build a queue and enqueue a few media items from the round-trip library.  
playback_queue = PlaybackQueue()  
  
for media_item in round_trip_library.get_media():  
    playback_queue.enqueue(media_item)  
  
# Wire the queue into the Player as its media source.  
player = Player()  
player.set_source(playback_queue)  
  
# Pull the first item from the queue and confirm it loaded.  
assert player.load_next() is True  
assert player.get_current_item() is not None  
assert player.get_state() == PlaybackState.STOPPED  
  
# Begin playback.  
player.play()  
assert player.is_playing() is True  
  
# Advance the transport past the item's duration so it finishes.  
duration = player.get_duration()  
  
player.tick(duration)  
  
assert player.is_finished() is True  
assert player.get_position() == duration  
  
# Loading the next item resets position and returns to STOPPED.  
if player.load_next():  
    assert player.get_position() == 0  
    assert player.get_state() == PlaybackState.STOPPED  
  
print("Player + PlaybackQueue verified.")

print("\n=== Testing Engine Broadcast Pipeline ===")  
  
from engine.engine import Engine  
  
engine = Engine()  
engine.initialize()  
  
# Attach media to the active channel's current programming block.  
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

from channel.channel_manager import ChannelManager  
from channel.channel import Channel  
  
print("\n=== Testing Channel Manager (time sync) ===")  
  
engine = Engine()  
engine.initialize()   # builds clock, scheduler, channel_manager (from loader), osd  
  
# The engine self-populates its ChannelManager from ChannelConfigs/channels.json  
# (channels 2 "VISTOR General" and 4 "VISTOR Movies").  
manager = engine.channel_manager  
assert manager.count() >= 2  
  
# Channels progress in real time on every engine tick.  
engine.update()  
engine.update()  
  
manager.channel_up()  
assert manager.get_active_channel().get_number() == 4  
manager.previous_channel()  
assert manager.get_active_channel().get_number() == 2  
  
print("Channel Manager verified.")

print("\n=== Testing Remote Controller ===")  
  
from remote.remote_controller import RemoteController  
  
# Reuse the engine/channel_manager already built in the earlier block.  
manager = engine.channel_manager  
  
remote = RemoteController(manager, engine)  
  
# Channel up / down cycle through the registered channels.  
remote.press("channel_up")  
remote.press("channel_down")  
  
# Numeric entry: type "4" then Enter to jump to channel number 4.  
remote.press("digit_4")  
remote.press("enter")  
assert manager.get_active_channel().get_number() == 4  
  
# Previous-channel button returns to the last-watched channel.  
remote.press("prev")  
  
# Unknown key should warn, not crash.  
remote.press("power") 

# Clock button flashes the 5-second summoned clock overlay.  
from osd.osd_manager import OSDOverlay  
remote.press("clock")  
assert engine.osd.get_overlay() == OSDOverlay.CLOCK  
assert engine.osd.is_visible() is True  
engine.osd.hide()   # reset so later overlay assertions start clean
  
print("Remote Controller verified.")

print("=== Testing OSD Manager ===")  
  
from osd.osd_manager import OSDManager, OSDOverlay, OSDPhase  
  
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
  
print("\n=== Testing Channel Banner + OSD Indicators ===")  
  
from osd.osd_manager import OSDManager, OSDOverlay  
  
# The engine (built above) owns a ChannelManager + OSDManager wired together.  
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
  
# --- Auto-hide: tick() advances one phase per call (FADE_IN -> VISIBLE -> FADE_OUT -> HIDDEN) ---  
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

print("\n=== Testing Program Information ===")  
  
from osd.osd_manager import OSDOverlay  
  
# Ensure the active channel has a now-playing item to describe.  
active = engine.channel_manager.get_active_channel()  
active_block = active.get_current_block()  
assert active_block is not None  
  
# Reuse a movie from the built library (guaranteed to have a title).  
info_movie = built.get_movies()[0]  
active_block.add_item(info_movie)  
  
# Tick the channel so its player loads/plays the item from the block.  
engine.update()  
engine.update()  
  
# --- Program Information fires ---  
engine.show_info()  
assert engine.osd.is_visible() is True  
assert engine.osd.get_overlay() == OSDOverlay.PROGRAM_INFO  
  
info = engine.osd.get_payload()  
assert info["number"] == active.get_number()  
assert info["channel_name"] == active.get_name()  
# Title is present when something is playing; tolerate None if the block is empty.  
if active.get_player().get_current_item() is not None:  
    assert info["title"] == active.get_player().get_current_item().get_title()  
# Defensive fields must always exist, even when unpopulated.  
assert "rating" in info  
assert isinstance(info["genres"], list)  
  
# --- Auto-hide (tick advances one phase per call) ---  
engine.osd.tick(engine.osd.fade_duration + 0.1)      # FADE_IN  -> VISIBLE  
engine.osd.tick(engine.osd.visible_duration + 0.1)   # VISIBLE  -> FADE_OUT  
engine.osd.tick(engine.osd.fade_duration + 0.1)      # FADE_OUT -> HIDDEN  
assert engine.osd.is_visible() is False  
  
print("Program Information verified.")

print("\n=== Testing Clock Overlay ===")  
  
from osd.osd_manager import OSDOverlay, OSDPhase  
  
engine.show_clock()  
assert engine.osd.is_visible() is True  
assert engine.osd.get_overlay() == OSDOverlay.CLOCK  
  
clock_payload = engine.osd.get_payload()  
assert "time" in clock_payload  
assert isinstance(clock_payload["time"], str)  
assert clock_payload["time"]                       # non-empty  
assert ("AM" in clock_payload["time"]) or ("PM" in clock_payload["time"])  
  
# Auto-hide (tick advances one phase per call).  
engine.osd.tick(engine.osd.fade_duration + 0.1)    # FADE_IN  -> VISIBLE  
engine.osd.tick(engine.osd.visible_duration + 0.1) # VISIBLE  -> FADE_OUT  
engine.osd.tick(engine.osd.fade_duration + 0.1)    # FADE_OUT -> HIDDEN  
assert engine.osd.is_visible() is False  
  
print("Clock overlay verified.")  
  
  
print("\n=== Testing Fade Animations ===")  
  
from osd.osd_manager import OSDManager  
  
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

print("\n=== Testing TV Guide ===")  
  
# The engine (built above) owns a Guide over its ChannelManager + Clock.  
assert engine.guide is not None  
  
# Opening the guide builds one row per channel.  
engine.open_guide()  
assert engine.guide.is_open() is True  
assert engine.guide.get_row_count() == engine.channel_manager.count()  
  
# Each row exposes the channel's number + name.  
first_row = engine.guide.get_rows()[0]  
first_channel = engine.channel_manager.get_channels()[0]  
assert first_row["number"] == first_channel.get_number()  
assert first_row["name"] == first_channel.get_name()  
  
# Current + upcoming program labels are always populated (placeholder if empty).  
assert engine.guide.get_current_program(0) is not None  
assert engine.guide.get_upcoming_program(0) is not None  
  
# Time display is a non-empty 12-hour string.  
time_text = engine.guide.get_time_text()  
assert isinstance(time_text, str) and time_text  
assert ("AM" in time_text) or ("PM" in time_text)  
  
# Navigation: cursor starts at 0, moves down, and clamps at the ends.  
assert engine.guide.get_selected_row() == 0  
engine.guide_down()  
if engine.channel_manager.count() > 1:  
    assert engine.guide.get_selected_row() == 1  
engine.guide_up()  
assert engine.guide.get_selected_row() == 0  
engine.guide_up()                     # clamp at top  
assert engine.guide.get_selected_row() == 0  
  
# Closing hides it.  
engine.close_guide()  
assert engine.guide.is_open() is False  
  
print("TV Guide verified.")

print("\n=== Testing Intelligent Content Management (asset persistence) ===")  
  
import tempfile  
from pathlib import Path as _Path  
  
from metadata.relationships.media_asset import MediaAsset  
from metadata.enums.download_status import DownloadStatus  
from metadata.services.metadata_serializer import MetadataSerializer  
from metadata.services.metadata_loader import MetadataLoader  
  
# Attach an asset carrying full ICM state to a real media item.  
sample = built.get_media()[0]  
  
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
  
from metadata.services.keyframe_fingerprint import KeyframeFingerprintService  
  
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
  
from datetime import datetime, timedelta  
  
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

print("\n=== Testing Multi-Archive Resolver ===")  
  
from metadata.services.source_resolver import SourceResolver, FetchResult  
from metadata.relationships.media_asset import MediaAsset  
from metadata.enums.download_status import DownloadStatus  
  
  
class _FakeFetcher:  
    """Canned fetcher: maps 'provider:reference' -> FetchResult."""  
  
    def __init__(self, responses):  
        self._responses = responses  
  
    def fetch(self, provider, reference):  
        key = f"{provider}:{reference}"  
        return self._responses.get(key, FetchResult.failure(404))  
  
  
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

# ------------------------------------------------------------------  
# Scoring (broadcast / retention / pinning)  
# ------------------------------------------------------------------  
  
print("\n=== Testing Scoring ===")  
  
from metadata.services.asset_scorer import AssetScorer  
  
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
  
# Pinning is a hard override: a pinned asset is never evictable even with  
# a zero retention score; an unpinned low-score asset is.  
pinned_asset = MediaAsset(asset_id="score_pinned", path="Media/pinned.mkv")  
pinned_asset.set_retention_score(0.0)  
pinned_asset.set_pinned(True)  
assert scorer.should_evict(pinned_asset) is False  
  
evictable = MediaAsset(asset_id="score_evictable", path="Media/evictable.mkv")  
evictable.set_retention_score(0.0)  
assert scorer.should_evict(evictable) is True  
  
# A high-retention unpinned asset is retained.  
keeper = MediaAsset(asset_id="score_keeper", path="Media/keeper.mkv")  
keeper.set_retention_score(9.0)  
assert scorer.should_evict(keeper) is False  
  
print("Scoring verified.")

# ------------------------------------------------------------------  
# Intelligent Content Management: Rolling Cache  
# ------------------------------------------------------------------  
  
print("\n=== Testing Rolling Cache ===")  
  
from metadata.services.rolling_cache import RollingCache  
  
# --- Rolling episode window --------------------------------------  
  
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
  
# --- Retention-driven eviction (with pinning) --------------------  
  
def _resident(asset_id, retention, size, pinned=False):  
    a = MediaAsset(asset_id=asset_id, path=f"Media/{asset_id}.mkv")  
    a.set_download_status(DownloadStatus.DOWNLOADED)  
    a.set_retention_score(retention)  
    a.file_size = size  
    a.set_pinned(pinned)  
    return a  
  
low   = _resident("rc_low",   retention=1.0, size=100)  
mid   = _resident("rc_mid",   retention=5.0, size=100)  
high  = _resident("rc_high",  retention=9.0, size=100)  
pinned = _resident("rc_pinned", retention=0.0, size=100, pinned=True)  
  
assets = [high, low, pinned, mid]  
  
# Total 400 bytes, budget 250 -> must free >=150 bytes (>=2 files).  
evicted = cache.evict_to_budget(assets, budget_bytes=250)  
  
# Lowest retention evicted first; pinned never evicted despite 0.0 score.  
assert "rc_low" in evicted  
assert "rc_mid" in evicted  
assert "rc_pinned" not in evicted  
assert low.get_download_status() == DownloadStatus.MISSING  
assert pinned.get_download_status() == DownloadStatus.DOWNLOADED  
  
# Deleted-content metadata retention: evicted asset still carries its  
# metadata (score/sources survive), so it can be re-fetched later.  
assert low.get_retention_score() == 1.0  
assert low.needs_download() is True  
  
# Under budget -> no eviction.  
assert cache.evict_to_budget([high], budget_bytes=1000) == []  
  
print("Rolling cache verified.")
  
# ------------------------------------------------------------------  
# Final Result  
# ------------------------------------------------------------------  

print("\n================================")  
print("Metadata System Test Complete")  
print("All tests passed successfully.")  
print("================================")