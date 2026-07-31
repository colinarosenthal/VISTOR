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
        self.version = "0.6.0"  
  
        # Directories  
        self.media_directory = "Media"  
        self.assets_directory = "Assets"  
        self.metadata_directory = "Metadata"  
  
        # Features  
        self.weather_enabled = True  
        self.osd_enabled = True  
  
        # Recommended Media (see Docs/Ideas.md -> Recommended Media).  
        # recommended_media gates the whole feature; recommendation_mode is  
        # "suggest_only" (human-confirmed, the safe default) or "auto_commit"  
        # (reserved for a later slice - not yet wired to auto-download).  
        self.recommended_media = False  
        self.recommendation_mode = "suggest_only"  
  
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
            "recommended_media": self.recommended_media,  
            "recommendation_mode": self.recommendation_mode,  
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
  
    def is_recommended_media_enabled(self):  
        return self.recommended_media  
  
    def get_recommendation_mode(self):  
        return self.recommendation_mode