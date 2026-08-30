"""  
VISTOR Settings Menu  
  
Headless, navigable on-screen settings menu. Like the Guide, this does not  
render pixels; it models the rows a settings overlay would show, a selection  
cursor, and value adjustment. It reads and writes a Config instance and  
persists changes to disk when closed, so settings are adjustable from the TV.  
"""  
  
from core.logger import Logger  
  
  
class SettingsMenu:  
    """Headless settings menu over a Config instance."""  
  
    # Storage-budget adjustment step: 1 GiB per left/right press.  
    BUDGET_STEP_BYTES = 1024 * 1024 * 1024  
  
    # Ordered options for the broadcast-mode choice field. The label is what  
    # the viewer sees; the value is what Config.broadcast_mode stores.  
    BROADCAST_MODES = [  
        ("off", "Off (No Commercials)"),  
        ("between_programs", "Between Programs"),  
        ("mid_program", "Mid-Program"),  
    ]  
  
    def __init__(self, config):  
        self.config = config  
  
        self.is_visible = False  
        self.selected_row = 0  
  
        # Ordered list of adjustable settings. Each entry is a dict with a  
        # display label, the Config attribute it edits, and its kind. This  
        # covers every user-facing Config setting.  
        self._fields = [  
            {"label": "Storage Budget", "key": "storage_budget_bytes", "kind": "bytes"},  
            {"label": "Commercials", "key": "broadcast_mode", "kind": "choice",  
             "options": self.BROADCAST_MODES},  
            {"label": "Captions", "key": "captions_enabled", "kind": "bool"},  
            {"label": "OSD Enabled", "key": "osd_enabled", "kind": "bool"},  
            {"label": "Weather Enabled", "key": "weather_enabled", "kind": "bool"},  
            {"label": "Recommended Media", "key": "recommended_media", "kind": "bool"},  
        ]  
  
    # ------------------------------------------------------------------  
    # Open / close  
    # ------------------------------------------------------------------  
  
    def open(self):  
        """Open the settings menu."""  
  
        self.is_visible = True  
        Logger.info("Settings menu opened.")  
  
    def close(self):  
        """Close the settings menu and persist any changes."""  
  
        self.is_visible = False  
  
        try:  
            self.config.save()  
        except Exception as error:  # noqa: BLE001 - never crash on save  
            Logger.error(f"Could not save settings: {error}.")  
  
        Logger.info("Settings menu closed (settings saved).")  
  
    def toggle(self):  
        """Toggle the settings menu open/closed and return the new state."""  
  
        if self.is_visible:  
            self.close()  
        else:  
            self.open()  
  
        return self.is_visible  
  
    def is_open(self):  
        """Return whether the settings menu is currently on screen."""  
  
        return self.is_visible  
  
    # ------------------------------------------------------------------  
    # Navigation  
    # ------------------------------------------------------------------  
  
    def move_up(self):  
        """Move the selection cursor up one row (clamped)."""  
  
        if self.selected_row > 0:  
            self.selected_row -= 1  
  
        return self.selected_row  
  
    def move_down(self):  
        """Move the selection cursor down one row (clamped)."""  
  
        if self.selected_row < len(self._fields) - 1:  
            self.selected_row += 1  
  
        return self.selected_row  
  
    def adjust_left(self):  
        """Decrease / toggle / cycle-back the selected setting."""  
  
        self._adjust(-1)  
  
    def adjust_right(self):  
        """Increase / toggle / cycle-forward the selected setting."""  
  
        self._adjust(1)  
  
    def _adjust(self, direction):  
        """Apply an adjustment in `direction` (+1 / -1) to the selected field."""  
  
        field = self._fields[self.selected_row]  
        key = field["key"]  
        current = getattr(self.config, key)  
  
        if field["kind"] == "bool":  
            setattr(self.config, key, not current)  
  
        elif field["kind"] == "bytes":  
            new_value = current + direction * self.BUDGET_STEP_BYTES  
            setattr(self.config, key, max(0, new_value))  
  
        elif field["kind"] == "choice":  
            values = [value for value, _label in field["options"]]  
            try:  
                index = values.index(current)  
            except ValueError:  
                index = 0  
            index = (index + direction) % len(values)  
            setattr(self.config, key, values[index])  
  
        Logger.info(f"Setting '{key}' -> {getattr(self.config, key)}.")  
  
    # ------------------------------------------------------------------  
    # Introspection (for the renderer + OSD payload)  
    # ------------------------------------------------------------------  
  
    def get_rows(self):  
        """Return the display rows: [{'label', 'value', 'selected'}, ...]."""  
  
        rows = []  
  
        for index, field in enumerate(self._fields):  
            rows.append({  
                "label": field["label"],  
                "value": self._format_value(field),  
                "selected": index == self.selected_row,  
            })  
  
        return rows  
  
    def get_selected_row(self):  
        """Return the selected row index."""  
  
        return self.selected_row  
  
    def _format_value(self, field):  
        """Format a field's current value for display."""  
  
        value = getattr(self.config, field["key"])  
  
        if field["kind"] == "bool":  
            return "On" if value else "Off"  
  
        if field["kind"] == "bytes":  
            if value <= 0:  
                return "Unlimited"  
            return f"{value / self.BUDGET_STEP_BYTES:.0f} GB"  
  
        if field["kind"] == "choice":  
            for option_value, option_label in field["options"]:  
                if option_value == value:  
                    return option_label  
            return str(value)  
  
        return str(value)