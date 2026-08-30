"""  
VISTOR Engine  
"""  
  
from core.logger import Logger  
from core.clock import Clock  
from core.config import Config
  
from scheduler.scheduler import Scheduler  
from scheduler.broadcast_controller import BroadcastController  
  
from player.player import Player    
from player.playback_queue import PlaybackQueue    
from player.renderer import create_renderer, NullRenderer 
  
from channel.channel_manager import ChannelManager  
  
from osd.osd_manager import OSDManager  

from metadata.services.storage_manager import StorageManager

from guide.guide import Guide  
  
from settings.settings_menu import SettingsMenu
  
  
class Engine:  
    """Coordinates the VISTOR runtime."""  
  
    def __init__(self):  
        self.running = False  
        self.library = None  
  
        self.clock = None  
        self.scheduler = None  
  
        self.queue = None  
        self.broadcast_controller = None  
        self.player = None  
  
        self.storage_manager = None
        self._storage_tick_accumulator = 0.0
  
        # Real audio/video output. One shared renderer is attached to only  
        # the currently-watched channel's Player; every other channel keeps  
        # its headless NullRenderer so it advances without decoding.  
        self.renderer = None  
        self._rendered_player = None  
  
        self.current_block = None  
  
        # Channel + OSD subsystems.  
        self.channel_manager = None  
        self.osd = None

        self.guide = None  
  
        self.config = None  
        self.settings_menu = None
  
    def initialize(self):  
        """Initialize the engine."""  
  
        Logger.info("Engine initialized.")  
  
        self.clock = Clock()  
        self.clock.initialize()  
  
        self.scheduler = Scheduler(self.clock)  
        self.scheduler.initialize()  
  
        # Legacy single pipeline (retained for existing tests / tooling).  
        self.queue = PlaybackQueue()  
        self.broadcast_controller = BroadcastController(self.queue)  
        self.player = Player(self.queue)  
  
        # Channels: each owns its own pipeline and shares the Clock so all  
        # lineups progress in real time regardless of what is being watched.  
        self.channel_manager = ChannelManager()  
        self.channel_manager.initialize(self.clock)  
  
        # On-Screen Display. Raise the channel banner whenever the active  
        # channel changes; the ChannelManager stays OSD-agnostic.  
        self.osd = OSDManager()  
        self.channel_manager.set_on_channel_change(self._on_channel_change)

        self.guide = Guide(self.channel_manager, self.clock)  
  
        # TV Settings Menu (adjustable from the remote). Wraps a persisted  
        # Config; changes are saved to disk when the menu closes.  
        self.config = Config().load()  
        self.settings_menu = SettingsMenu(self.config)  
  
        # Build the real renderer (falls back to NullRenderer when python-mpv  
        # / libmpv is unavailable) and surface only the active channel.  
        self.renderer = create_renderer()  
        self._attach_renderer_to_active()
        # Storage budget enforcement (no-op until a library is loaded and a  
        # nonzero storage_budget_bytes is configured).  
        if self.library is not None:  
            self.storage_manager = StorageManager(self.library)
  
    def start(self):  
        """Start the engine."""  
  
        Logger.info("Starting engine...")  
  
        self.running = True  
  
        while self.running:  
            self.update()  
            break  
  
    def update(self):  
        """Run one engine update."""

        if self.scheduler is None:  
            Logger.warning("Engine.update() called before initialize(); skipping.")  
            return  
  
        # Capture real elapsed time from the Clock before advancing it.  
        previous_time = self.clock.get_time()  
        self.clock.update()  
        current_time = self.clock.get_time()  
  
        if previous_time is not None:  
            elapsed_seconds = (current_time - previous_time).total_seconds()  
        else:  
            elapsed_seconds = 0.0  
  
        self.scheduler.update()  
  
        # Refill the queue whenever the active programming block changes.  
        block = self.scheduler.get_current_block()  
  
        if block is not self.current_block:  
            self.current_block = block  
            self._on_block_change(block)  
  
        # Drive the legacy pipeline.  
        self.player.tick(elapsed_seconds)  
  
        # Advance every channel so all lineups stay time-synced.  
        if self.channel_manager is not None:  
            self.channel_manager.update(elapsed_seconds)  
  
        # Advance the OSD so banners/indicators fade and auto-hide.  
        # Advance the OSD so banners/indicators fade and auto-hide.    
        if self.osd is not None:    
            self.osd.tick(elapsed_seconds)    
  
            # Paint the current overlay onto the active renderer's surface.  
            if self.renderer is not None:  
                self.renderer.render_osd(self.osd)
  
        Logger.info("Engine update.")
        # Enforce the storage budget on a throttle (no-op when disabled).  
        if self.storage_manager is not None:  
            self._storage_tick_accumulator += elapsed_seconds  
            if self._storage_tick_accumulator >= 3600:  # hourly  
                self._storage_tick_accumulator = 0.0  
                self.storage_manager.enforce_budget()

        if self.guide is not None and self.guide.is_open():  
            self.guide.refresh_time()
  
    def _on_block_change(self, block):  
        """Hand the new block to the Broadcast Controller to rebuild the queue."""  
  
        # The Broadcast Controller decides what goes in the queue (programs +  
        # any interruptions). The Engine only coordinates; it does not enqueue.  
        self.broadcast_controller.update(block)  
  
        # Begin playback of the first queued item on the next tick.  
        self.player.load_next()  
  
    # ------------------------------------------------------------------  
    # Channel Control (remote-facing)  
    # ------------------------------------------------------------------  
  
    def channel_up(self):  
        """Switch to the next channel (raises the channel banner)."""  
  
        return self.channel_manager.channel_up()  
  
    def channel_down(self):  
        """Switch to the previous channel (raises the channel banner)."""  
  
        return self.channel_manager.channel_down()  
  
    def set_channel_by_number(self, number):  
        """Switch to a channel by its on-screen number (numeric entry)."""  
  
        return self.channel_manager.set_channel_by_number(number)  
  
    def previous_channel(self):  
        """Jump back to the last-watched channel."""  
  
        return self.channel_manager.previous_channel()  
  
    # ------------------------------------------------------------------  
    # Audio Control (remote-facing)
    # ------------------------------------------------------------------  
  
    def _active_player(self):  
        """Return the active channel's Player, or None."""  
  
        if self.channel_manager is None:  
            return None  
  
        channel = self.channel_manager.get_active_channel()  
  
        return channel.get_player() if channel is not None else None 

    def _attach_renderer_to_active(self):  
        """Give the shared renderer to the watched channel's Player only.  
  
        The previously-surfaced Player is reset to a headless NullRenderer  
        (so it keeps advancing without decoding); the active channel's Player  
        receives the real renderer and resurfaces its in-progress item.  
        """  
  
        if self.renderer is None:  
            return  
  
        active = self._active_player()  
  
        if self._rendered_player is active:  
            return  
  
        if self._rendered_player is not None:  
            self._rendered_player.set_renderer(NullRenderer())  
  
        if active is not None:  
            active.set_renderer(self.renderer)  
  
        self._rendered_player = active 
  
    def volume_up(self, step=5):  
        """Raise volume on the active channel and show the volume indicator."""  
  
        player = self._active_player()  
  
        if player is None:  
            return  
  
        player.volume_up(step)  
        self.osd.show_volume(player.get_volume(), player.is_muted())  
  
    def volume_down(self, step=5):  
        """Lower volume on the active channel and show the volume indicator."""  
  
        player = self._active_player()  
  
        if player is None:  
            return  
  
        player.volume_down(step)  
        self.osd.show_volume(player.get_volume(), player.is_muted())  
  
    def toggle_mute(self):  
        """Toggle mute on the active channel and show the mute indicator."""  
  
        player = self._active_player()  
  
        if player is None:  
            return  
  
        player.toggle_mute()  
        self.osd.show_mute(player.is_muted())

    def show_info(self):  
        """Show the program-information panel for the active channel."""  
  
        if self.channel_manager is None or self.osd is None:  
            return  
  
        channel = self.channel_manager.get_active_channel()  
  
        if channel is None:  
            return  
  
        self.osd.show_program_info(channel, channel.get_player())

    def show_clock(self):  
        """Show the clock overlay with the current wall-clock time."""  
  
        if self.osd is None or self.clock is None:  
            return  
  
        self.osd.show_clock(self._format_clock_text())  
  
    def _format_clock_text(self):  
        """Format the current time as a 12-hour cable-box clock string."""  
  
        hour = self.clock.get_hour()  
        minute = self.clock.get_minute()  
  
        suffix = "AM" if hour < 12 else "PM"  
  
        hour_12 = hour % 12  
        if hour_12 == 0:  
            hour_12 = 12  
  
        return f"{hour_12}:{minute:02d} {suffix}"

    # ------------------------------------------------------------------  
    # Guide Control
    # ------------------------------------------------------------------  

    def open_guide(self):  
        """Open the TV guide (rebuilds rows from the current lineup)."""  
  
        if self.guide is None:  
            return  
  
        self.guide.open()  
  
    def close_guide(self):  
        """Close the TV guide."""  
  
        if self.guide is None:  
            return  
  
        self.guide.close()  
  
    def toggle_guide(self):  
        """Toggle the TV guide open/closed."""  
  
        if self.guide is None:  
            return  
  
        self.guide.toggle()  
  
    def guide_up(self):  
        """Move the guide selection up one channel row."""  
  
        if self.guide is None:  
            return  
  
        self.guide.move_up()  
  
    def guide_down(self):  
        """Move the guide selection down one channel row."""  
  
        if self.guide is None:  
            return  
  
        self.guide.move_down()

    # ------------------------------------------------------------------  
    # Settings Control  
    # ------------------------------------------------------------------  
  
    def toggle_settings(self):  
        """Toggle the TV settings menu and raise/lower its OSD overlay."""  
  
        if self.settings_menu is None:  
            return  
  
        opened = self.settings_menu.toggle()  
  
        if self.osd is not None:  
            if opened:  
                self.osd.show_settings(self.settings_menu.get_rows())  
            else:  
                self.osd.hide()  
  
    def _refresh_settings_overlay(self):  
        """Re-paint the settings overlay after a navigation/adjust action."""  
  
        if self.settings_menu is None or not self.settings_menu.is_open():  
            return  
  
        if self.osd is not None:  
            self.osd.show_settings(self.settings_menu.get_rows())  
  
    def settings_up(self):  
        """Move the settings selection up one row."""  
  
        if self.settings_menu is not None:  
            self.settings_menu.move_up()  
            self._refresh_settings_overlay()  
  
    def settings_down(self):  
        """Move the settings selection down one row."""  
  
        if self.settings_menu is not None:  
            self.settings_menu.move_down()  
            self._refresh_settings_overlay()  
  
    def settings_left(self):  
        """Decrease / toggle / cycle the selected setting backward."""  
  
        if self.settings_menu is not None:  
            self.settings_menu.adjust_left()  
            self._refresh_settings_overlay()  
  
    def settings_right(self):  
        """Increase / toggle / cycle the selected setting forward."""  
  
        if self.settings_menu is not None:  
            self.settings_menu.adjust_right()  
            self._refresh_settings_overlay()
  
    # ------------------------------------------------------------------  
    # OSD callbacks  
    # ------------------------------------------------------------------  
  
    def _on_channel_change(self, channel):    
        """Raise the channel banner for the newly-active channel."""    
    
        if self.osd is not None and channel is not None:    
            self.osd.show_channel_banner(channel, channel.get_player())    
  
        # Re-point the real renderer at the newly-watched channel's Player.  
        self._attach_renderer_to_active()
  
    def stop(self):  
        """Stop the engine."""  
  
        Logger.info("Stopping engine...")  
  
        self.running = False  
  
    def shutdown(self):  
        """Shutdown the engine."""  
  
        Logger.info("Shutting down engine...")  
  
        self.running = False  
  
        if self.channel_manager is not None:  
            self.channel_manager.shutdown()  
  
        if self.scheduler is not None:  
            self.scheduler.shutdown()  
  
        if self.clock is not None:  
            self.clock.shutdown()