"""
VISTOR Schedule Loader
"""

from core.logger import Logger

from scheduler.schedule import Schedule
from scheduler.programming_block import ProgrammingBlock
from scheduler.schedule_type import ScheduleType


class ScheduleLoader:
    """Builds and loads schedules for the scheduler."""

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def __init__(self):
        self.schedule_library = {}

        self.loaded = False

    def load(self):
        """Load all schedules."""

        Logger.info("Loading schedules...")

        self._load_weekday_schedule()
        self._load_weekend_schedule()
        self._load_holiday_schedules()

        self.loaded = True

        Logger.info("Schedules loaded.")

    def unload(self):
        """Unload all schedules."""

        self.schedule_library.clear()

        self.loaded = False

    def is_loaded(self):
        """Return whether schedules have been loaded."""

        return self.loaded

    # ------------------------------------------------------------------
    # Schedule Access
    # ------------------------------------------------------------------

    def get_schedule_library(self):
        """Return the complete schedule library."""

        return self.schedule_library

    def get_schedule(self, schedule_type):
        """Return a schedule by type."""

        return self.schedule_library.get(schedule_type)

    # ------------------------------------------------------------------
    # Internal Loading
    # ------------------------------------------------------------------

    def _load_weekday_schedule(self):
        """Create the weekday schedule."""

        schedule = Schedule("Weekday")

        schedule.add_block(
            ProgrammingBlock(
                "Default Programming",
                0,
                0,
                23,
                59
            )
        )

        schedule.load()

        self.schedule_library[ScheduleType.WEEKDAY] = schedule

    def _load_weekend_schedule(self):
        """Create the weekend schedule."""

        schedule = Schedule("Weekend")

        schedule.add_block(
            ProgrammingBlock(
                "Weekend Programming",
                0,
                0,
                23,
                59
            )
        )

        schedule.load()

        self.schedule_library[ScheduleType.WEEKEND] = schedule

    def _load_holiday_schedules(self):
        """Create placeholder holiday schedules."""

        holidays = [
            ScheduleType.NEW_YEARS_DAY,
            ScheduleType.VALENTINES_DAY,
            ScheduleType.ST_PATRICKS_DAY,
            ScheduleType.INDEPENDENCE_DAY,
            ScheduleType.HALLOWEEN,
            ScheduleType.THANKSGIVING,
            ScheduleType.CHRISTMAS_EVE,
            ScheduleType.CHRISTMAS_DAY,
            ScheduleType.NEW_YEARS_EVE,
        ]

        for holiday in holidays:
            schedule = Schedule(holiday.name.title().replace("_", " "))

            schedule.add_block(
                ProgrammingBlock(
                    "Holiday Programming",
                    0,
                    0,
                    23,
                    59
                )
            )

            schedule.load()

            self.schedule_library[holiday] = schedule