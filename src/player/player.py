"""  
VISTOR Player  
  
Headless playback state machine.  
  
The Player does not decode or render video. It models the transport  
state of a single media item (stopped, playing, paused, finished) and  
advances playback position when ticked by the runtime loop.  
"""  
  
from __future__ import annotations  
  
from enum import Enum 

from typing import Optional, Protocol  
  
from core.logger import Logger

from player.renderer import NullRenderer
  
  
class PlaybackState(Enum):  
    """Transport states for the Player."""  
  
    STOPPED = "stopped"  
    PLAYING = "playing"  
    PAUSED = "paused"  
    FINISHED = "finished"  
  
  
class MediaSource(Protocol):  
    """  
    Anything the Player can pull the next media item from.  
  
    A PlaybackQueue is the default implementation, but any object that  
    returns the next media item (or None when exhausted) is accepted.  
    This keeps the broadcast structure configurable outside the Player.  
    """  
  
    def has_next(self):  
        """Return whether another item is available."""  
        ...  
  
    def get_next(self):  
        """Return the next media item, or None if the source is empty."""  
        ...
  
  
class Player:  
    """Headless transport for a single media item at a time."""  
  
    # ------------------------------------------------------------------  
    # Construction  
    # ------------------------------------------------------------------  
  
    def __init__(self, source: Optional[MediaSource] = None, renderer=None):  
        self.source = source  
  
        # Real output layer. Defaults to headless so tests / unwatched  
        # channels never touch a display; swap in an MpvRenderer for the  
        # channel the viewer is actually watching.  
        self.renderer = renderer or NullRenderer()  
  
        self.current_item = None  
  
        self.state = PlaybackState.STOPPED  
  
        self.position_seconds = 0  
  
        self.duration_seconds = 0  
  
        # Audio state (mirrored to the renderer).  
        self.volume = 50  
  
        self.muted = False
  
    # ------------------------------------------------------------------  
    # Source  
    # ------------------------------------------------------------------  
  
    def set_source(self, source: MediaSource):  
        """Set the media source the Player pulls from."""  
  
        self.source = source  

    def set_renderer(self, renderer):  
        """Swap the output renderer, mirroring audio + playback state.  
  
        Pushes current volume/mute onto the new backend, then resurfaces the  
        in-progress item so a channel switch shows the live program  
        immediately instead of a black screen.  
        """  
  
        self.renderer = renderer  
  
        renderer.set_volume(self.volume)  
        renderer.set_mute(self.muted)  
  
        if self.current_item is not None:  
            path = self._resolve_source_path(self.current_item)  
  
            if path is not None:  
                renderer.load(path)  
  
                # Resume mid-program: jump the new backend to the position the  
                # headless transport has tracked (channels never stop), so a  
                # channel switch shows the running program at the right offset.  
                if self.position_seconds > 0:  
                    renderer.seek(self.position_seconds)  
  
                if self.state == PlaybackState.PLAYING:  
                    renderer.play()
  
    # ------------------------------------------------------------------  
    # Loading  
    # ------------------------------------------------------------------  
  
    def load_item(self, item) -> bool:  
        """  
        Load a specific media item and prepare it for playback.  
  
        Returns True if the item was loaded, False otherwise.  
        """  
  
        if item is None:  
            Logger.warning("Player received no item to load.")  
  
            self._reset()  
  
            return False  
  
        self.current_item = item  
  
        self.position_seconds = 0  
  
        self.duration_seconds = self._resolve_duration(item)

        path = self._resolve_source_path(item)  
        if path is not None:  
            self.renderer.load(path)
  
        self.state = PlaybackState.STOPPED  
  
        Logger.info(  
            f"Loaded '{item.get_title()}' "  
            f"({self.duration_seconds}s) into the player."  
        )  
  
        return True  
  
    def load_next(self) -> bool:  
        """  
        Pull the next item from the configured source and load it.  
  
        Returns True if an item was loaded, False if the source is  
        empty or unset.  
        """  
  
        if self.source is None:  
            Logger.warning("Player has no media source set.")  
  
            return False  
  
        if not self.source.has_next():  
            return False  
  
        return self.load_item(self.source.get_next())
  
    # ------------------------------------------------------------------  
    # Transport  
    # ------------------------------------------------------------------  
  
    def play(self):  
        """Begin or resume playback of the current item."""  
  
        if self.current_item is None:  
            Logger.warning("Play requested with no item loaded.")  
  
            return  
  
        self.state = PlaybackState.PLAYING  
  
        self.renderer.play()  
  
        Logger.info(f"Playing '{self.current_item.get_title()}'.")
  
    def pause(self):  
        """Pause playback, preserving position."""  
  
        if self.state != PlaybackState.PLAYING:  
            return  
  
        self.state = PlaybackState.PAUSED  
  
        self.renderer.pause()  
  
        Logger.info(f"Paused '{self.current_item.get_title()}'.")
  
    def stop(self):  
        """Stop playback and clear the current item."""  
  
        if self.current_item is not None:  
            Logger.info(f"Stopped '{self.current_item.get_title()}'.")  
  
        self.renderer.stop()  
  
        self._reset()
  
    # ------------------------------------------------------------------  
    # Runtime  
    # ------------------------------------------------------------------  
  
    def tick(self, seconds: int = 1):  
        """  
        Advance playback by the given number of seconds.  
  
        When the current item reaches its duration it is marked  
        finished; the runtime loop is responsible for calling  
        load_next() to continue the broadcast.  
        """  
  
        if self.state != PlaybackState.PLAYING:  
            return  
  
        self.position_seconds += seconds  
  
        if self.position_seconds >= self.duration_seconds:  
            self.position_seconds = self.duration_seconds  
  
            self.state = PlaybackState.FINISHED  
  
            Logger.info(  
                f"Finished '{self.current_item.get_title()}'."  
            )  
  
    # ------------------------------------------------------------------  
    # State  
    # ------------------------------------------------------------------  
  
    def get_state(self):  
        """Return the current playback state."""  
  
        return self.state  
  
    def get_current_item(self):  
        """Return the currently loaded media item."""  
  
        return self.current_item  
  
    def get_position(self):  
        """Return the current playback position in seconds."""  
  
        return self.position_seconds  
  
    def get_duration(self):  
        """Return the duration of the current item in seconds."""  
  
        return self.duration_seconds  
  
    def is_playing(self):  
        """Return whether the player is actively playing."""  
  
        return self.state == PlaybackState.PLAYING  
  
    def is_finished(self):  
        """Return whether the current item has finished."""  
  
        return self.state == PlaybackState.FINISHED  
  
    # ------------------------------------------------------------------  
    # Internal  
    # ------------------------------------------------------------------  
  
    def _reset(self):  
        """Clear all playback state."""  
  
        self.current_item = None  
  
        self.state = PlaybackState.STOPPED  
  
        self.position_seconds = 0  
  
        self.duration_seconds = 0  
  
    def _resolve_duration(self, item) -> int:  
        """  
        Determine playback duration in seconds for an item.  
  
        Prefers a verified media asset's runtime; falls back to the  
        item's declared runtime in minutes.  
        """  
  
        assets = item.get_media_assets()  
  
        for asset in assets:  
            runtime = asset.get_runtime_seconds()  
  
            if runtime > 0:  
                return runtime  
  
        return item.get_runtime_minutes() * 60

    def _resolve_source_path(self, item):  
        """Return the on-disk path of the first present media asset, or None."""  
  
        for asset in item.get_media_assets():  
            if asset.exists():  
                return str(asset.get_path())  
  
        Logger.warning(  
            f"No downloaded asset on disk for '{item.get_title()}'; "  
            f"renderer has nothing to open."  
        )  
        return None

    # ------------------------------------------------------------------  
    # Audio  
    # ------------------------------------------------------------------  
  
    def set_volume(self, level):  
        """Set the volume, clamped to the 0-100 range."""  
  
        self.volume = max(0, min(100, int(level)))  
  
        self.renderer.set_volume(self.volume)  
  
        Logger.info(f"Volume set to {self.volume}.")
  
    def volume_up(self, step=5):  
        """Increase the volume by step (clamped)."""  
  
        self.set_volume(self.volume + step)  
  
    def volume_down(self, step=5):  
        """Decrease the volume by step (clamped)."""  
  
        self.set_volume(self.volume - step)  
  
    def set_mute(self, flag):  
        """Set the mute state explicitly."""  
  
        self.muted = bool(flag)  
  
        self.renderer.set_mute(self.muted)  
  
        Logger.info("Muted." if self.muted else "Unmuted.")
  
    def toggle_mute(self):  
        """Toggle the mute state."""  
  
        self.set_mute(not self.muted)  
  
    def get_volume(self):  
        """Return the current volume (0-100)."""  
  
        return self.volume  
  
    def is_muted(self):  
        """Return whether the player is muted."""  
  
        return self.muted