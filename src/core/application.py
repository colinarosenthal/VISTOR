"""
VISTOR Application

Coordinates startup, initialization, and shutdown.
"""

from core.config import Config
from core.logger import Logger
from core.paths import Paths
from engine import Engine


class Application:
    """Main VISTOR application."""

    def __init__(self):

        self.running = False

    def initialize(self):
        """Initialize application services."""

        Logger.info("Loading configuration...")

        self.config = Config()
        self.config.load()

        Logger.info("Initializing paths...")

        self.paths = Paths()
        self.paths.verify()

        Logger.info("Initializing engine...")

        self.engine = Engine()
        self.engine.initialize()

    def start(self):
        """Start VISTOR."""

        Logger.info("Starting VISTOR...")

        self.initialize()

        self.engine.start()

        self.running = True

        Logger.success(
            "VISTOR successfully initialized."
        )

    def shutdown(self):
        """Shutdown VISTOR."""

        Logger.info(
            "Shutting down VISTOR..."
        )

        self.engine.shutdown()

        self.running = False

        Logger.success(
            "VISTOR shutdown complete."
        )