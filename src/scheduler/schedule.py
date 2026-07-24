"""
VISTOR Schedule
"""

from core.logger import Logger


class Schedule:
    """Represents a broadcast schedule."""

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def __init__(self, name):
        self.name = name

        self.blocks = []

        self.loaded = False

    def load(self):
        """Load the schedule."""

        # Placeholder for future schedule loading.

        self.loaded = True

        Logger.info(f"{self.name} schedule loaded.")

    def unload(self):
        """Unload the schedule."""

        self.clear_blocks()

        self.loaded = False

    def is_loaded(self):
        """Return whether the schedule has been loaded."""

        return self.loaded

    # ------------------------------------------------------------------
    # Programming Blocks
    # ------------------------------------------------------------------

    def add_block(self, block):
        """Add a programming block."""

        self.blocks.append(block)

    def remove_block(self, block):
        """Remove a programming block."""

        if block in self.blocks:
            self.blocks.remove(block)

    def clear_blocks(self):
        """Remove all programming blocks."""

        self.blocks.clear()

    def get_blocks(self):
        """Return all programming blocks."""

        return self.blocks

    def get_current_block(self, clock):
        """Return the currently active programming block."""

        for block in self.blocks:
            if block.is_active_at(clock):
                return block

        return None