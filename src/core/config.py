"""
VISTOR Configuration
"""

import json
import os


class Config:
    """Manages VISTOR configuration."""

    def __init__(self, path="Metadata/data/config.json"):

        # General
        self.debug = False
        self.version = "0.8.1"

        # Directories
        self.media_directory = "Media"
        self.assets_directory = "Assets"
        self.metadata_directory = "Metadata"

        # Features
        self.weather_enabled = True
        self.osd_enabled = True
        self.captions_enabled = False

        # Broadcast Mode (see Design Bible 3.4 -> Broadcast Modes). Controls
        # where commercial blocks air relative to programs:
        #   "off"              -> no commercials at all
        #   "between_programs" -> commercials only after a program ends
        #   "mid_program"      -> commercials at authentic mid-program breaks
        self.broadcast_mode = "between_programs"

        # Recommended Media (see Docs/Ideas.md -> Recommended Media).
        # recommended_media gates the whole feature; recommendation_mode is
        # one of:
        #   "suggest_only" -> return suggestions only; download nothing (default)
        #   "assisted"     -> auto-find a candidate source URL; human confirms
        #   "automatic"    -> auto URL-discovery + ingest, capped per week
        self.recommended_media = False
        self.recommendation_mode = "suggest_only"
        # Discovery loop bounds (see Docs/Ideas.md -> Possible Settings).
        self.seed_source = "whole_library"      # whole_library | per_channel | specific
        self.max_auto_additions_per_week = 0    # hard cap for automatic mode

        # Storage budget (Intelligent Content Management). Max bytes VISTOR
        # may keep on disk under the media root before retention-driven
        # eviction runs. 0 = disabled (no eviction), the safe default until
        # an external drive is in place (#1).
        self.storage_budget_bytes = 0

        # Where load()/save() persist overrides.
        self.path = path

    # ------------------------------------------------------------------
    # Loading / Saving
    # ------------------------------------------------------------------

    def load(self):
        """Load overrides from `self.path` if present, else keep defaults.

        Returns self so callers can do `Config().load()`.
        """

        if not self.path or not os.path.exists(self.path):
            return self

        try:
            with open(self.path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except Exception:  # noqa: BLE001 - a bad config file must not crash boot
            return self

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        return self

    def save(self):
        """Persist the current settings to `self.path` as JSON."""

        data = {
            "debug": self.debug,
            "version": self.version,
            "media_directory": self.media_directory,
            "assets_directory": self.assets_directory,
            "metadata_directory": self.metadata_directory,
            "weather_enabled": self.weather_enabled,
            "osd_enabled": self.osd_enabled,
            "captions_enabled": self.captions_enabled,
            "broadcast_mode": self.broadcast_mode,
            "recommended_media": self.recommended_media,
            "recommendation_mode": self.recommendation_mode,
            "seed_source": self.seed_source,
            "max_auto_additions_per_week": self.max_auto_additions_per_week,
            "storage_budget_bytes": self.storage_budget_bytes,
        }

        directory = os.path.dirname(self.path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self.path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=4)

        return self

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

    def set_media_directory(self, path):
        """Set the media root and persist it (TV Settings Menu #1)."""
        self.media_directory = path
        self.save()

    def get_assets_directory(self):
        return self.assets_directory

    def get_metadata_directory(self):
        return self.metadata_directory

    # ------------------------------------------------------------------
    # Storage Budget
    # ------------------------------------------------------------------

    def get_storage_budget_bytes(self):
        """Return the on-disk storage budget in bytes (0 = disabled)."""

        return self.storage_budget_bytes

    def is_storage_budget_enabled(self):
        """Return whether a nonzero storage budget is configured."""

        return self.storage_budget_bytes > 0

    # ------------------------------------------------------------------
    # Features
    # ------------------------------------------------------------------

    def is_weather_enabled(self):
        return self.weather_enabled

    def is_osd_enabled(self):
        return self.osd_enabled

    def is_recommended_media_enabled(self):
        return self.recommended_media

    def get_recommendation_mode(self):
        return self.recommendation_mode

    def is_captions_enabled(self):
        return self.captions_enabled

    def get_broadcast_mode(self):
        return self.broadcast_mode
