"""
VISTOR Path Management
"""

from pathlib import Path

from core.config import Config


class Paths:
    """Provides access to important VISTOR directories."""

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        # Media root is configurable (Design Bible 3.6 / 4.3): an absolute
        # media_directory (e.g. an external USB SSD or Raspberry Pi path) is
        # used as-is; a relative value is anchored under the project root.
        media_dir = Config().load().get_media_directory()
        media_path = Path(media_dir)
        if media_path.is_absolute():
            self.media = media_path
        else:
            self.media = self.project_root / media_dir

        self.assets = self.project_root / "Assets"
        self.logs = self.project_root / "Logs"
        self.config = self.project_root / "Config"
        self.metadata = self.project_root / "Metadata"
        self.schedules = self.project_root / "Schedules"

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    def verify(self):
        """Verify required directories exist, creating local ones and
        warning (not crashing) if a configured external media drive is
        absent."""

        from core.logger import Logger

        local = [
            self.assets,
            self.logs,
            self.config,
            self.metadata,
            self.schedules,
        ]

        for directory in local:
            directory.mkdir(parents=True, exist_ok=True)

        if not self.media.exists():
            if self.media.is_absolute():
                Logger.warning(
                    f"Configured media root not present (drive not "
                    f"mounted?): {self.media}"
                )
            else:
                self.media.mkdir(parents=True, exist_ok=True)

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
