"""
VISTOR Runtime Engine
"""

from core.logger import Logger


class Engine:
    """Controls the VISTOR runtime."""

    def __init__(self):
        self.running = False
        self.initialized = False
        self.update_count = 0

    def initialize(self):
        """Initialize the engine."""

        Logger.info("Engine initialized.")

        self.initialized = True

    def start(self):
        """Start the engine."""

        if not self.initialized:
            raise RuntimeError("Engine has not been initialized.")

        Logger.info("Starting engine...")

        self.running = True

        while self.running:
            self.update()
            break

    def update(self):
        """Run one engine update."""

        self.update_count += 1

        Logger.info(f"Engine update #{self.update_count}.")

    def stop(self):
        """Stop the engine."""

        Logger.info("Stopping engine...")

        self.running = False

    def shutdown(self):
        """Shutdown the engine."""

        Logger.info("Shutting down engine...")

        self.running = False
        self.initialized = False

    def is_running(self):
        """Return whether the engine is running."""

        return self.running

    def is_initialized(self):
        """Return whether the engine has been initialized."""

        return self.initialized