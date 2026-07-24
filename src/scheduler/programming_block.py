"""
VISTOR Programming Block
"""


class ProgrammingBlock:
    """Represents a single broadcast programming block."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self, name, start_hour, start_minute, end_hour, end_minute):
        self.name = name

        self.start_hour = start_hour
        self.start_minute = start_minute

        self.end_hour = end_hour
        self.end_minute = end_minute

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def is_active_at(self, clock):
        """Return whether the programming block is active at the current time."""

        current_minutes = (
            clock.get_hour() * 60 +
            clock.get_minute()
        )

        start_minutes = (
            self.start_hour * 60 +
            self.start_minute
        )

        end_minutes = (
            self.end_hour * 60 +
            self.end_minute
        )

        # TODO:
        # Support programming blocks that span midnight.

        return start_minutes <= current_minutes < end_minutes

    def get_name(self):
        """Return the programming block name."""

        return self.name

    def get_start_time(self):
        """Return the programming block start time."""

        return (
            self.start_hour,
            self.start_minute
        )

    def get_end_time(self):
        """Return the programming block end time."""

        return (
            self.end_hour,
            self.end_minute
        )