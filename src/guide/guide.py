"""  
VISTOR TV Guide  
  
Headless electronic program guide. The Guide does not render pixels; it  
models what an on-screen guide would show -- one row per channel, each with  
the channel's now-airing program (current) and the next scheduled program  
(upcoming), a wall-clock time-display string, and a selection cursor for  
navigation. A future renderer reads these accessors to paint the grid.  
  
The Guide is built from the Scheduler's ProgrammingBlocks across every  
channel in the ChannelManager. It reads the ChannelManager and Clock; it is  
never depended on by Channel or Player, keeping the dependency one-way.  
"""  
  
from core.logger import Logger  
  
  
class Guide:  
    """Headless electronic program guide over all channels."""  
  
    # ------------------------------------------------------------------  
    # Construction  
    # ------------------------------------------------------------------  
  
    def __init__(self, channel_manager, clock):  
        self.channel_manager = channel_manager  
        self.clock = clock  
  
        self.is_visible = False  
        self.selected_row = 0  
  
        # Snapshot state (recomputed on build/refresh) for the renderer.  
        self.rows = []  
        self.time_text = ""  
  
    # ------------------------------------------------------------------  
    # Open / close (Navigation entry points)  
    # ------------------------------------------------------------------  
  
    def open(self):  
        """Open the guide, rebuilding its rows from the current lineup."""  
  
        self.build()  
        self.is_visible = True  
  
        Logger.info("Guide opened.")  
  
    def close(self):  
        """Close the guide."""  
  
        self.is_visible = False  
  
        Logger.info("Guide closed.")  
  
    def toggle(self):  
        """Toggle the guide open/closed and return the new state."""  
  
        if self.is_visible:  
            self.close()  
        else:  
            self.open()  
  
        return self.is_visible  
  
    def is_open(self):  
        """Return whether the guide is currently on screen."""  
  
        return self.is_visible  
  
    # ------------------------------------------------------------------  
    # Build / refresh  
    # ------------------------------------------------------------------  
  
    def build(self):  
        """(Re)compute the guide rows and time display from the lineup."""  
  
        self.rows = []  
  
        for channel in self.channel_manager.get_channels():  
            current = channel.get_current_block()  
            upcoming = self._upcoming_block(channel, current)  
  
            self.rows.append({  
                "number": channel.get_number(),  
                "name": channel.get_name(),  
                "current": self._block_label(current),  
                "current_slot": self._block_slot(current),  
                "upcoming": self._block_label(upcoming),  
                "upcoming_slot": self._block_slot(upcoming),  
            })  
  
        self.refresh_time()  
  
        # Keep the cursor in range if the channel set shrank.  
        if self.selected_row >= len(self.rows):  
            self.selected_row = max(0, len(self.rows) - 1)  
  
    def refresh(self):  
        """Rebuild rows and time (used while the guide stays open)."""  
  
        self.build()  
  
    def refresh_time(self):  
        """Refresh only the time-display string (cheap, per-frame safe)."""  
  
        self.time_text = self._format_time()  
  
    # ------------------------------------------------------------------  
    # Navigation  
    # ------------------------------------------------------------------  
  
    def move_up(self):  
        """Move the selection cursor up one channel row (clamped)."""  
  
        if self.selected_row > 0:  
            self.selected_row -= 1  
  
        return self.selected_row  
  
    def move_down(self):  
        """Move the selection cursor down one channel row (clamped)."""  
  
        if self.selected_row < len(self.rows) - 1:  
            self.selected_row += 1  
  
        return self.selected_row  
  
    # ------------------------------------------------------------------  
    # Introspection (for the future renderer)  
    # ------------------------------------------------------------------  
  
    def get_rows(self):  
        """Return all guide rows (one per channel)."""  
  
        return self.rows  
  
    def get_row_count(self):  
        """Return the number of guide rows."""  
  
        return len(self.rows)  
  
    def get_selected_row(self):  
        """Return the selected row index."""  
  
        return self.selected_row  
  
    def get_selection(self):  
        """Return the selected row's data, or None if empty."""  
  
        if 0 <= self.selected_row < len(self.rows):  
            return self.rows[self.selected_row]  
  
        return None  
  
    def get_current_program(self, row_index):  
        """Return the current-program label for a given row (guard range)."""  
  
        if 0 <= row_index < len(self.rows):  
            return self.rows[row_index]["current"]  
  
        return None  
  
    def get_upcoming_program(self, row_index):  
        """Return the upcoming-program label for a given row (guard range)."""  
  
        if 0 <= row_index < len(self.rows):  
            return self.rows[row_index]["upcoming"]  
  
        return None  
  
    def get_time_text(self):  
        """Return the guide's wall-clock time-display string."""  
  
        return self.time_text  
  
    # ------------------------------------------------------------------  
    # Internal helpers  
    # ------------------------------------------------------------------  
  
    def _upcoming_block(self, channel, current):  
        """Return the next ProgrammingBlock after `current` in the schedule."""  
  
        schedule = channel.get_current_schedule()  
  
        if schedule is None:  
            return None  
  
        blocks = schedule.get_blocks()  
  
        if not blocks:  
            return None  
  
        # If we can't locate the current block, fall back to the first.  
        if current is None or current not in blocks:  
            return blocks[0]  
  
        index = blocks.index(current)  
  
        if index + 1 < len(blocks):  
            return blocks[index + 1]  
  
        return None  
  
    def _block_label(self, block):  
        """Return a display name for a block, or a placeholder."""  
  
        if block is None:  
            return "No Program"  
  
        return block.get_name()  
  
    def _block_slot(self, block):  
        """Return a 'H:MM AM - H:MM PM' time-slot string, or ''."""  
  
        if block is None:  
            return ""  
  
        start = self._format_hm(*block.get_start_time())  
        end = self._format_hm(*block.get_end_time())  
  
        return f"{start} - {end}"  
  
    def _format_time(self):  
        """Return the current wall-clock time as a 12-hour string."""  
  
        if self.clock is None:  
            return ""  
  
        return self._format_hm(self.clock.get_hour(), self.clock.get_minute())  
  
    def _format_hm(self, hour, minute):  
        """Format an (hour, minute) pair as a 12-hour cable-box string."""  
  
        suffix = "AM" if hour < 12 else "PM"  
  
        display_hour = hour % 12  
  
        if display_hour == 0:  
            display_hour = 12  
  
        return f"{display_hour}:{minute:02d} {suffix}"