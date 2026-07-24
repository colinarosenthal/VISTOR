"""
VISTOR Application

Coordinates startup, initialization, and shutdown.
"""

from core.config import Config
from core.logger import Logger
from core.paths import Paths


class Application:
    """Main VISTOR application."""

    def __init__(self):
        self.running = False

    def initialize(self):
        """Initialize the application."""

        Logger.info("Initializing logger...")
        self.logger = Logger()

        Logger.info("Loading configuration...")
        self.config = Config()
        self.config.load()

        Logger.info("Initializing paths...")
        self.paths = Paths()
        self.paths.verify()

        Logger.info("Initializing engine...")
        # Placeholder for future engine initialization.

    def start(self):
        """Start the application."""

        Logger.info("Starting VISTOR...")

        self.initialize()

        self.running = True

        Logger.info("VISTOR successfully initialized.")

    def shutdown(self):
        """Shutdown the application."""

        self.running = False

        Logger.info("Shutting down VISTOR...")