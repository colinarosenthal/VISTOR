"""
VISTOR Configuration
"""


class Config:
    """Manages VISTOR configuration."""

    def __init__(self):

        # General
        self.debug = False
        self.version = "0.2.0"

        # Directories
        self.media_directory = "Media"
        self.assets_directory = "Assets"
        self.metadata_directory = "Metadata"

        # Features
        self.weather_enabled = True
        self.osd_enabled = True

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load(self):
        """
        Load configuration.

        Placeholder for future:
        - JSON loading
        - YAML loading
        - TOML loading
        - Environment variables
        """

        pass

    # ------------------------------------------------------------------
    # General
    # ------------------------------------------------------------------

    def is_debug_enabled(self):
        return self.debug

    def get_version(self):
        return self.version

    # ------------------------------------------------------------------
    # Directories
    # ------------------------------------------------------------------

    def get_media_directory(self):
        return self.media_directory

    def get_assets_directory(self):
        return self.assets_directory

    def get_metadata_directory(self):
        return self.metadata_directory

    # ------------------------------------------------------------------
    # Features
    # ------------------------------------------------------------------

    def is_weather_enabled(self):
        return self.weather_enabled

    def is_osd_enabled(self):
        return self.osd_enabled