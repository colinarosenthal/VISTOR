"""  
VISTOR Channel Loader  
  
Builds and loads the full set of channels for the Channel Manager from  
an external configuration file (ChannelConfigs/channels.json), so  
channels can be added or edited without code changes.    
"""  
  
from pathlib import Path  

import json  
  
from core.logger import Logger  
  
from channel.channel import Channel  
  
  
class ChannelLoader:  
    """Builds and loads channels for the Channel Manager."""  

    DEFAULT_CONFIG_PATH = "ChannelConfigs/channels.json" 

    def __init__(self, config_path=None):  
        self.config_path = Path(config_path or self.DEFAULT_CONFIG_PATH)  
  
        self.channels = []  
  
        self.loaded = False  
  
    def load(self):  
        """Load all channels from the configuration file."""  
  
        Logger.info("Loading channels...")  
  
        for record in self._read_config(self.config_path):  
  
            channel = self._build_channel(record)  
  
            if channel is not None:  
                self.channels.append(channel)  
  
        self.loaded = True  
  
        Logger.info(f"Channels loaded ({len(self.channels)}).")  
  
    def unload(self):  
        """Unload all channels."""  
  
        self.channels.clear()  
  
        self.loaded = False  
  
    def is_loaded(self):  
        """Return whether channels have been loaded."""  
  
        return self.loaded  
  
    def get_channels(self):  
        """Return the complete channel set."""  
  
        return self.channels  
  
    # ------------------------------------------------------------------  
    # Internal Loading  
    # ------------------------------------------------------------------  
  
    def _build_channel(self, record):  
        """Construct a Channel from one JSON record, defaulting absent fields."""  
  
        if "number" not in record or "name" not in record:  
            Logger.warning(  
                "Channel config entry missing required 'number'/'name'; "  
                "skipping."  
            )  
            return None  
  
        return Channel(  
            number=record["number"],  
            name=record["name"],  
            logo=record.get("logo", ""),  
            primary_genre=record.get("primary_genre", ""),  
            target_audience=record.get("target_audience", ""),  
            programming_sources=record.get("programming_sources", []),  
            commercial_pools=record.get("commercial_pools", []),  
            promotional_material=record.get("promotional_material", []),  
            broadcast_schedule=record.get("broadcast_schedule", "default"),  
            station_id_graphics=record.get("station_id_graphics", []),  
            network_branding=record.get("network_branding", ""),  
        )  
  
    def _read_config(self, path):  
        """Read and parse the channel config, tolerating missing/bad files."""  
  
        path = Path(path)  
  
        if not path.exists():  
            Logger.warning(f"Channel config not found: {path}")  
            return []  
  
        try:  
            with open(path, "r", encoding="utf-8") as file:  
                data = json.load(file)  
        except (json.JSONDecodeError, OSError) as error:  
            Logger.error(f"Failed to read channel config {path}: {error}")  
            return []  
  
        if not isinstance(data, list):  
            Logger.error(  
                f"Channel config {path} must be a JSON array of channel "  
                f"objects."  
            )  
            return []  
  
        return data