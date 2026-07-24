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