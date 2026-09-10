"""
VISTOR Logging
"""

from datetime import datetime


class Logger:
    """Central logging service for VISTOR."""

    @staticmethod
    def _log(level: str, message: str):
        """Print formatted log message."""

        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"[{timestamp}] [{level}] {message}")

    @staticmethod
    def debug(message: str):
        """Log debugging information."""

        Logger._log("DEBUG", message)

    @staticmethod
    def info(message: str):
        """Log informational messages."""

        Logger._log("INFO", message)

    @staticmethod
    def success(message: str):
        """Log successful operations."""

        Logger._log("SUCCESS", message)

    @staticmethod
    def warning(message: str):
        """Log warnings."""

        Logger._log("WARNING", message)

    @staticmethod
    def error(message: str):
        """Log errors."""

        Logger._log("ERROR", message)

    @staticmethod
    def critical(message: str):
        """Log critical failures."""

        Logger._log("CRITICAL", message)
