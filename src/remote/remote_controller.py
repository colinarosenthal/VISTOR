"""
VISTOR Remote Controller

Headless input dispatcher for the viewer's remote control.

The RemoteController does not talk to any real keyboard/input backend.
It maps abstract key names (e.g. "channel_up", "digit_4", "prev") to
actions on the ChannelManager, so the control logic is fully testable
without a GUI. A real input backend (keyboard/pynput/on-screen remote)
can later feed key names into press() without changing this class.
"""

from core.logger import Logger


class RemoteController:
    """Maps remote key presses to ChannelManager actions."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self, channel_manager, engine=None):
        self.channel_manager = channel_manager

        # Optional reference to the Engine, needed for actions that live on
        # the runtime rather than the ChannelManager (e.g. the summoned
        # clock overlay, which is raised via Engine.show_clock()). Kept
        # optional so channel-only usage/tests still work.
        self.engine = engine

        # Buffer for multi-digit numeric channel entry (e.g. "1", "2" -> 12).
        self._digit_buffer = ""

        # Key name -> handler method. Extend this to add new remote keys
        # without changing press().
        self._bindings = {
            "channel_up": self._on_channel_up,
            "channel_down": self._on_channel_down,
            "prev": self._on_previous_channel,
            "clock": self._on_clock,
            "guide": self._on_guide,
            "settings": self._on_settings,
        }

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------

    def press(self, key):
        """Handle a single remote key press by name."""

        # Numeric entry: keys named "digit_0" .. "digit_9".
        if key.startswith("digit_"):
            self._on_digit(key[len("digit_"):])
            return

        # "enter" commits any buffered numeric channel entry.
        if key == "enter":
            self._commit_digits()
            return

        handler = self._bindings.get(key)

        if handler is None:
            Logger.warning(f"Remote key '{key}' is not bound.")
            return

        handler()

    # ------------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------------

    def _on_channel_up(self):
        """Channel up button."""

        self.channel_manager.channel_up()

    def _on_channel_down(self):
        """Channel down button."""

        self.channel_manager.channel_down()

    def _on_previous_channel(self):
        """Previous (last-watched) channel button."""

        self.channel_manager.previous_channel()

    def _on_clock(self):
        """Clock button: flash the 5-second summoned clock overlay."""

        if self.engine is None:
            Logger.warning("Clock button pressed but no engine is bound.")
            return

        self.engine.show_clock()

    def _on_guide(self):
        """Guide button: toggle the electronic program guide."""

        if self.engine is None:
            Logger.warning("Guide button pressed but no engine is bound.")
            return

        self.engine.toggle_guide()

    def _on_settings(self):
        """Settings button: toggle the TV settings menu."""

        if self.engine is None:
            Logger.warning("Settings button pressed but no engine is bound.")
            return

        self.engine.toggle_settings()

    def _on_digit(self, digit):
        """Accumulate a digit for numeric channel entry."""

        if not digit.isdigit():
            Logger.warning(f"Ignoring non-digit remote input '{digit}'.")
            return

        self._digit_buffer += digit

    def _commit_digits(self):
        """Switch to the channel number typed into the digit buffer."""

        if not self._digit_buffer:
            return

        number = int(self._digit_buffer)

        self._digit_buffer = ""

        self.channel_manager.set_channel_by_number(number)
