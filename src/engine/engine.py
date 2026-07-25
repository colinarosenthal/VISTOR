"""
VISTOR Engine
"""

from core.logger import Logger
from core.clock import Clock
from scheduler.scheduler import Scheduler


class Engine:
    """Coordinates the VISTOR runtime."""

    def __init__(self):
        self.running = False

    def initialize(self):
        """Initialize the engine."""

        Logger.info("Engine initialized.")

        self.clock = Clock()
        self.clock.initialize()

        self.scheduler = Scheduler(self.clock)
        self.scheduler.initialize()

    def start(self):
        """Start the engine."""

        Logger.info("Starting engine...")

        self.running = True

        while self.running:
            self.update()
            break

    def update(self):
        """Run one engine update."""

        self.clock.update()
        self.scheduler.update()

        Logger.info("Engine update.")

    def stop(self):
        """Stop the engine."""

        Logger.info("Stopping engine...")

        self.running = False

    def shutdown(self):
        """Shutdown the engine."""

        Logger.info("Shutting down engine...")

        self.running = False