"""
VISTOR Logging
"""

from datetime import datetime


class Logger:
    """Simple console logger for VISTOR."""

    @staticmethod
    def info(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [INFO] {message}")

    @staticmethod
    def warning(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [WARNING] {message}")

    @staticmethod
    def error(message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [ERROR] {message}")