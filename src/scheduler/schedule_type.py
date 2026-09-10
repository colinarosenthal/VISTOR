"""
VISTOR Schedule Types
"""


from enum import Enum


class ScheduleType(Enum):
    """Available schedule types."""

    WEEKDAY = "weekday"
    WEEKEND = "weekend"

    NEW_YEARS_DAY = "new_years_day"
    VALENTINES_DAY = "valentines_day"
    ST_PATRICKS_DAY = "st_patricks_day"
    INDEPENDENCE_DAY = "independence_day"
    HALLOWEEN = "halloween"
    THANKSGIVING = "thanksgiving"
    CHRISTMAS_EVE = "christmas_eve"
    CHRISTMAS_DAY = "christmas_day"
    NEW_YEARS_EVE = "new_years_eve"
