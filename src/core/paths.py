"""
VISTOR Path Management
"""

from pathlib import Path


class Paths:
    """Provides access to important VISTOR directories."""

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.assets = self.project_root / "Assets"
        self.media = self.project_root / "Media"
        self.logs = self.project_root / "Logs"
        self.config = self.project_root / "Config"
        self.metadata = self.project_root / "Metadata"
        self.schedules = self.project_root / "Schedules"

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    def verify(self):
        """Verify required directories exist."""

        required = [
            self.assets,
            self.media,
            self.logs,
            self.config,
            self.metadata,
            self.schedules,
        ]

        for directory in required:

            if not directory.exists():

                raise FileNotFoundError(
                    f"Missing required directory: {directory}"
                )

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_project_root(self):
        return self.project_root

    def get_assets_directory(self):
        return self.assets

    def get_media_directory(self):
        return self.media

    def get_logs_directory(self):
        return self.logs

    def get_config_directory(self):
        return self.config

    def get_metadata_directory(self):
        return self.metadata

    def get_schedules_directory(self):
        return self.schedules