"""  
VISTOR On-Screen Display (OSD) Manager  
  
Headless overlay state machine. The OSDManager does not render pixels; it  
models which temporary overlay is currently on screen (channel banner,  
volume, mute, clock), how opaque it is (for fade in/out), and when it  
should auto-hide -- exactly like a late-1990s/early-2000s cable box.  
  
A single timed-visibility model is shared by every overlay type, so the  
channel banner and the volume indicator behave identically: show, hold,  
fade out. It is driven by real elapsed seconds from the runtime Clock.  
"""  
  
from enum import Enum  
  
from core.logger import Logger  
  
  
class OSDOverlay(Enum):  
    """The kind of overlay currently displayed."""  
  
    NONE = "none"  
    CHANNEL_BANNER = "channel_banner"  
    VOLUME = "volume"  
    MUTE = "mute"  
    CLOCK = "clock"  
  
  
class OSDPhase(Enum):  
    """Visibility phase within the timed-visibility model."""  
  
    HIDDEN = "hidden"  
    FADE_IN = "fade_in"  
    VISIBLE = "visible"  
    FADE_OUT = "fade_out"  
  
  
class OSDManager:  
    """Owns which overlay is shown and drives its fade/auto-hide timing."""  
  
    # Period-correct cable-box timings (seconds).  
    FADE_DURATION = 0.4  
    VISIBLE_DURATION = 5.0  
  
    def __init__(self, visible_duration=None, fade_duration=None):  
        self.visible_duration = (  
            self.VISIBLE_DURATION if visible_duration is None else visible_duration  
        )  
        self.fade_duration = (  
            self.FADE_DURATION if fade_duration is None else fade_duration  
        )  
  
        self.overlay = OSDOverlay.NONE  
        self.phase = OSDPhase.HIDDEN  
  
        # Payload is the snapshot the renderer will draw (title, number, etc.).  
        self.payload = {}  
  
        # Time spent in the current phase.  
        self._elapsed = 0.0  
  
    # ------------------------------------------------------------------  
    # Showing overlays  
    # ------------------------------------------------------------------  
  
    def show(self, overlay, payload=None):  
        """Show an overlay, (re)starting the timed-visibility cycle."""  
  
        self.overlay = overlay  
        self.payload = payload or {}  
  
        # Restart the cycle: fade in from wherever we are now.  
        self.phase = OSDPhase.FADE_IN  
        self._elapsed = 0.0  
  
    def show_channel_banner(self, channel, player=None):  
        """Show the channel banner for the given channel."""  
  
        payload = {  
            "number": channel.get_number(),  
            "name": channel.get_name(),  
        }  
  
        # Best-effort now-playing title from the channel's player.  
        source = player  
        if source is None and hasattr(channel, "get_player"):  
            source = channel.get_player()  
        if source is None:  
            source = getattr(channel, "player", None)  
  
        if source is not None:  
            item = source.get_current_item()  
            payload["program"] = item.get_title() if item is not None else None  
  
        self.show(OSDOverlay.CHANNEL_BANNER, payload)  
  
    def show_volume(self, level, muted=False):  
        """Show the volume indicator (also used for unmute feedback)."""  
  
        self.show(OSDOverlay.VOLUME, {"level": level, "muted": muted})  
  
    def show_mute(self, muted):  
        """Show the mute indicator."""  
  
        self.show(OSDOverlay.MUTE, {"muted": muted})  
  
    def show_clock(self, time_text):  
        """Show the clock overlay."""  
  
        self.show(OSDOverlay.CLOCK, {"time": time_text})  
  
    def hide(self):  
        """Immediately hide any overlay (skips the fade)."""  
  
        self.overlay = OSDOverlay.NONE  
        self.phase = OSDPhase.HIDDEN  
        self.payload = {}  
        self._elapsed = 0.0  
  
    # ------------------------------------------------------------------  
    # Runtime  
    # ------------------------------------------------------------------  
  
    def tick(self, seconds):  
        """Advance the visibility cycle by real elapsed seconds."""  
  
        if self.phase == OSDPhase.HIDDEN:  
            return  
  
        self._elapsed += seconds  
  
        if self.phase == OSDPhase.FADE_IN:  
            if self._elapsed >= self.fade_duration:  
                self.phase = OSDPhase.VISIBLE  
                self._elapsed = 0.0  
  
        elif self.phase == OSDPhase.VISIBLE:  
            if self._elapsed >= self.visible_duration:  
                self.phase = OSDPhase.FADE_OUT  
                self._elapsed = 0.0  
  
        elif self.phase == OSDPhase.FADE_OUT:  
            if self._elapsed >= self.fade_duration:  
                self.hide()  
  
    # ------------------------------------------------------------------  
    # Introspection (for the future renderer)  
    # ------------------------------------------------------------------  
  
    def is_visible(self):  
        """Return whether any overlay is currently on screen."""  
  
        return self.phase != OSDPhase.HIDDEN  
  
    def get_overlay(self):  
        """Return the current overlay type."""  
  
        return self.overlay  
  
    def get_payload(self):  
        """Return the current overlay's snapshot data."""  
  
        return self.payload  
  
    def get_opacity(self):  
        """Return current opacity 0.0-1.0 for fade rendering."""  
  
        if self.phase == OSDPhase.HIDDEN:  
            return 0.0  
  
        if self.phase == OSDPhase.VISIBLE:  
            return 1.0  
  
        if self.fade_duration <= 0:  
            return 1.0  
  
        fraction = min(1.0, self._elapsed / self.fade_duration)  
  
        if self.phase == OSDPhase.FADE_IN:  
            return fraction  
  
        # FADE_OUT  
        return 1.0 - fraction