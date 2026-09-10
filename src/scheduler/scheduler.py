"""
VISTOR Scheduler
"""

from core.logger import Logger
from scheduler.schedule_loader import ScheduleLoader

class Scheduler:
    """Manages the active broadcast schedule."""

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def __init__(self, clock):
        self.clock = clock

        self.initialized = False

        self.schedule_library = {}

        self.current_schedule = None
        self.current_block = None

    def initialize(self):
        """Initialize the scheduler."""

        Logger.info("Scheduler initialized.")

        loader = ScheduleLoader()

        loader.load()

        self.schedule_library = loader.get_schedule_library()

        self.initialized = True

    def update(self):
        """Update the active schedule and programming block."""

        schedule_type = self.clock.get_schedule_type()

        self.current_schedule = self.schedule_library.get(schedule_type)

        if self.current_schedule is None:
            self.current_block = None
            return

        self.current_block = self.current_schedule.get_current_block(self.clock)

    def shutdown(self):
        """Shutdown the scheduler."""

        self.schedule_library.clear()

        self.current_schedule = None
        self.current_block = None

        self.initialized = False

    def is_initialized(self):
        """Return whether the scheduler has been initialized."""

        return self.initialized

    # ------------------------------------------------------------------
    # Schedule Library
    # ------------------------------------------------------------------

    def add_schedule(self, schedule_type, schedule):
        """Add a schedule to the schedule library."""

        self.schedule_library[schedule_type] = schedule

    def get_schedule(self, schedule_type):
        """Return a schedule from the schedule library."""

        return self.schedule_library.get(schedule_type)

    # ------------------------------------------------------------------
    # Current State
    # ------------------------------------------------------------------

    def get_current_schedule(self):
        """Return the active schedule."""

        return self.current_schedule

    def get_current_block(self):
        """Return the active programming block."""

        return self.current_block
