"""
VISTOR Clock
"""

from datetime import datetime


class Clock:
    """Provides the current time for the VISTOR runtime."""

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

        return any([
            self.is_new_years_day(),
            self.is_valentines_day(),
            self.is_st_patricks_day(),
            self.is_independence_day(),
            self.is_halloween(),
            self.is_thanksgiving(),
            self.is_christmas_eve(),
            self.is_christmas_day(),
            self.is_new_years_eve()
        ])

    def is_morning(self):
        """Return whether it is morning."""

        return 5 <= self.get_hour() < 12

    def is_afternoon(self):
        """Return whether it is afternoon."""

        return 12 <= self.get_hour() < 17

    def is_evening(self):
        """Return whether it is evening."""

        return 17 <= self.get_hour() < 21

    def is_night(self):
        """Return whether it is night."""

        return self.get_hour() >= 21 or self.get_hour() < 5

    def shutdown(self):
        """Shutdown the clock."""

        self.current_time = None
        self.initialized = False

    def is_initialized(self):
        """Return whether the clock has been initialized."""

        return self.initialized