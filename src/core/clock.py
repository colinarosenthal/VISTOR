"""
VISTOR Clock
"""

from datetime import datetime

from core.schedule_type import ScheduleType


class Clock:
    """Provides current time information for VISTOR."""

    def __init__(self):

        self.current_time = None
        self.initialized = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def initialize(self):

        self.update()

        self.initialized = True

    def update(self):

        self.current_time = datetime.now()

    def shutdown(self):

        self.current_time = None
        self.initialized = False

    def is_initialized(self):

        return self.initialized

    # ------------------------------------------------------------------
    # Time Access
    # ------------------------------------------------------------------

    def get_time(self):

        return self.current_time

    def get_datetime_string(self):

        return self.current_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def get_year(self):

        return self.current_time.year

    def get_month(self):

        return self.current_time.month

    def get_day(self):

        return self.current_time.day

    def get_weekday(self):

        return self.current_time.strftime("%A")

    def get_hour(self):

        return self.current_time.hour

    def get_minute(self):

        return self.current_time.minute

    def get_second(self):

        return self.current_time.second

    # ------------------------------------------------------------------
    # Calendar
    # ------------------------------------------------------------------

    def is_weekday(self):

        return self.current_time.weekday() < 5

    def is_weekend(self):

        return self.current_time.weekday() >= 5

    def is_halloween(self):

        return (
            self.get_month() == 10
            and self.get_day() == 31
        )

    def is_christmas_day(self):

        return (
            self.get_month() == 12
            and self.get_day() == 25
        )

    def is_holiday(self):

        return self.get_schedule_type() not in (
            ScheduleType.WEEKDAY,
            ScheduleType.WEEKEND,
        )

    def get_schedule_type(self):

        if self.is_halloween():

            return ScheduleType.HALLOWEEN

        if self.is_christmas_day():

            return ScheduleType.CHRISTMAS_DAY

        if self.is_weekend():

            return ScheduleType.WEEKEND

        return ScheduleType.WEEKDAY