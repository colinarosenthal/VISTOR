"""
VISTOR Configuration
"""


class Config:
    """Manages VISTOR configuration."""

    def __init__(self):
        # General
        self.debug = False
        self.version = "0.1.0"

        # Directories
        self.media_directory = "Media"
        self.assets_directory = "Assets"

        # Features
        self.weather_enabled = True
        self.osd_enabled = True

    def load(self):
        """Load configuration."""

        # Placeholder for future configuration loading.
        pass