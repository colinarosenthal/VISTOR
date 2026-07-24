"""
VISTOR Clock
"""

from datetime import datetime
from scheduler.schedule_type import ScheduleType


class Clock:
    """Provides the current time for the VISTOR runtime."""

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def __init__(self):
        self.current_time = None
        self.initialized = False

    def initialize(self):
        """Initialize the clock."""

        self.update()

        self.initialized = True

    def update(self):
        """Update the current time."""

        self.current_time = datetime.now()

    def shutdown(self):
        """Shutdown the clock."""

        self.current_time = None
        self.initialized = False

    def is_initialized(self):
        """Return whether the clock has been initialized."""

        return self.initialized

    # ------------------------------------------------------------------
    # Time Accessors
    # ------------------------------------------------------------------

    def get_time(self):
        """Return the current datetime."""

        return self.current_time

    def get_date(self):
        """Return the current date."""

        return self.current_time.date()

    def get_datetime_string(self):
        """Return the current datetime as a formatted string."""

        return self.current_time.strftime("%Y-%m-%d %H:%M:%S")

    def get_year(self):
        """Return the current year."""

        return self.current_time.year

    def get_month(self):
        """Return the current month."""

        return self.current_time.month

    def get_day(self):
        """Return the current day."""

        return self.current_time.day

    def get_weekday(self):
        """Return the current weekday."""

        return self.current_time.strftime("%A")

    def get_hour(self):
        """Return the current hour."""

        return self.current_time.hour

    def get_minute(self):
        """Return the current minute."""

        return self.current_time.minute

    def get_second(self):
        """Return the current second."""

        return self.current_time.second

    # ------------------------------------------------------------------
    # Calendar
    # ------------------------------------------------------------------

    def is_weekday(self):
        """Return whether today is Monday through Friday."""

        return self.current_time.weekday() < 5

    def is_weekend(self):
        """Return whether today is Saturday or Sunday."""

        return self.current_time.weekday() >= 5

    def is_new_years_day(self):
        """Return whether today is New Year's Day."""

        return self.get_month() == 1 and self.get_day() == 1

    def is_valentines_day(self):
        """Return whether today is Valentine's Day."""

        return self.get_month() == 2 and self.get_day() == 14

    def is_st_patricks_day(self):
        """Return whether today is St. Patrick's Day."""

        return self.get_month() == 3 and self.get_day() == 17

    def is_independence_day(self):
        """Return whether today is Independence Day."""

        return self.get_month() == 7 and self.get_day() == 4

    def is_halloween(self):
        """Return whether today is Halloween."""

        return self.get_month() == 10 and self.get_day() == 31

    def is_thanksgiving(self):
        """Return whether today is Thanksgiving."""

        return (
            self.get_month() == 11
            and self.get_weekday() == "Thursday"
            and 22 <= self.get_day() <= 28
        )

    def is_christmas_eve(self):
        """Return whether today is Christmas Eve."""

        return self.get_month() == 12 and self.get_day() == 24

    def is_christmas_day(self):
        """Return whether today is Christmas Day."""

        return self.get_month() == 12 and self.get_day() == 25

    def is_new_years_eve(self):
        """Return whether today is New Year's Eve."""

        return self.get_month() == 12 and self.get_day() == 31

    def is_holiday(self):
        """Return whether today is a supported holiday."""

        return self.get_schedule_type() not in (
            ScheduleType.WEEKDAY,
            ScheduleType.WEEKEND
        )

    def get_schedule_type(self):
        """Return today's schedule type."""

        if self.is_new_years_day():
            return ScheduleType.NEW_YEARS_DAY

        if self.is_valentines_day():
            return ScheduleType.VALENTINES_DAY

        if self.is_st_patricks_day():
            return ScheduleType.ST_PATRICKS_DAY

        if self.is_independence_day():
            return ScheduleType.INDEPENDENCE_DAY

        if self.is_halloween():
            return ScheduleType.HALLOWEEN

        if self.is_thanksgiving():
            return ScheduleType.THANKSGIVING

        if self.is_christmas_eve():
            return ScheduleType.CHRISTMAS_EVE

        if self.is_christmas_day():
            return ScheduleType.CHRISTMAS_DAY

        if self.is_new_years_eve():
            return ScheduleType.NEW_YEARS_EVE

        if self.is_weekend():
            return ScheduleType.WEEKEND

        return ScheduleType.WEEKDAY