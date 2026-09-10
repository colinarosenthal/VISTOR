"""
VISTOR On-Screen Display (OSD) Manager

Headless overlay state machine. The OSDManager does not render pixels; it
models which temporary overlay is currently on screen (channel banner,
program information, volume, mute, clock), how opaque it is (for fade
in/out), and when it should auto-hide -- exactly like a late-1990s/
early-2000s cable box.

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
    PROGRAM_INFO = "program_info"
    VOLUME = "volume"
    MUTE = "mute"
    CLOCK = "clock"
    SETTINGS = "settings"



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

    def _resolve_player(self, channel, player=None):
        """Resolve a channel's Player (explicit arg, getter, then attribute)."""

        source = player

        if source is None and hasattr(channel, "get_player"):
            source = channel.get_player()

        if source is None:
            source = getattr(channel, "player", None)

        return source

    def show_channel_banner(self, channel, player=None):
        """Show the channel banner for the given channel."""

        payload = {
            "number": channel.get_number(),
            "name": channel.get_name(),
        }

        # Best-effort now-playing title from the channel's player.
        source = self._resolve_player(channel, player)

        if source is not None:
            item = source.get_current_item()
            payload["program"] = item.get_title() if item is not None else None

        self.show(OSDOverlay.CHANNEL_BANNER, payload)

    def show_program_info(self, channel, player=None):
        """Show the expanded program-information panel for the given channel.

        Reads the now-playing MediaItem from the channel's Player and the
        current time-slot context from the channel's active ProgrammingBlock.
        Every field is read defensively: many library items have no content
        rating and no genres, so missing values collapse to None / [].
        """

        payload = {
            "number": channel.get_number(),
            "channel_name": channel.get_name(),
            "title": None,
            "description": None,
            "release_year": None,
            "runtime_minutes": None,
            "rating": None,
            "genres": [],
            "media_type": None,
            "block_name": None,
            "block_start": None,
            "block_end": None,
        }

        # --- Now-playing MediaItem (may be None if nothing is loaded) ---
        source = self._resolve_player(channel, player)

        if source is not None:
            item = source.get_current_item()

            if item is not None:
                payload["title"] = item.get_title()
                payload["description"] = item.get_description()
                payload["release_year"] = item.get_release_year()
                payload["runtime_minutes"] = item.get_runtime_minutes()

                rating = item.get_content_rating()
                if rating is not None:
                    payload["rating"] = rating.get_name()

                payload["genres"] = [g.get_name() for g in item.get_genres()]

                media_type = item.get_media_type()
                if media_type is not None:
                    # Enum -> readable value where possible.
                    payload["media_type"] = getattr(
                        media_type, "value", str(media_type)
                    )

        # --- Time-slot context from the active programming block ---
        block = None
        if hasattr(channel, "get_current_block"):
            block = channel.get_current_block()

        if block is not None:
            payload["block_name"] = block.get_name()
            payload["block_start"] = block.get_start_time()
            payload["block_end"] = block.get_end_time()

        self.show(OSDOverlay.PROGRAM_INFO, payload)

    def show_volume(self, level, muted=False):
        """Show the volume indicator (also used for unmute feedback)."""

        self.show(OSDOverlay.VOLUME, {"level": level, "muted": muted})

    def show_mute(self, muted):
        """Show the mute indicator."""

        self.show(OSDOverlay.MUTE, {"muted": muted})

    def show_clock(self, time_text):
        """Show the clock overlay with a preformatted time string."""

        self.show(OSDOverlay.CLOCK, {"time": time_text})

    def show_settings(self, rows):
        """Show the settings menu overlay with a snapshot of its rows."""

        self.show(OSDOverlay.SETTINGS, {"rows": rows})

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
    # Fade Animations
    # ------------------------------------------------------------------

    @staticmethod
    def _ease(fraction):
        """Smoothstep easing (ease-in/ease-out) for gentler fades.

        Maps a linear 0.0-1.0 progress to an S-curve so overlays don't pop
        in/out with a hard linear ramp, matching period-correct OSD feel.
        """

        fraction = max(0.0, min(1.0, fraction))

        return fraction * fraction * (3.0 - 2.0 * fraction)

    def is_fading(self):
        """Return whether the overlay is mid fade-in or fade-out."""

        return self.phase in (OSDPhase.FADE_IN, OSDPhase.FADE_OUT)

    # ------------------------------------------------------------------
    # Introspection (for the future renderer)
    # ------------------------------------------------------------------

    def is_visible(self):
        """Return whether any overlay is currently on screen."""

        return self.phase != OSDPhase.HIDDEN

    def get_overlay(self):
        """Return the current overlay type."""

        return self.overlay

    def get_phase(self):
        """Return the current visibility phase."""

        return self.phase

    def get_payload(self):
        """Return the current overlay's snapshot data."""

        return self.payload

    def get_opacity(self):
        """Return current opacity 0.0-1.0 for fade rendering (eased)."""

        if self.phase == OSDPhase.HIDDEN:
            return 0.0

        if self.phase == OSDPhase.VISIBLE:
            return 1.0

        if self.fade_duration <= 0:
            return 1.0

        fraction = min(1.0, self._elapsed / self.fade_duration)
        eased = self._ease(fraction)

        if self.phase == OSDPhase.FADE_IN:
            return eased

        # FADE_OUT
        return 1.0 - eased
