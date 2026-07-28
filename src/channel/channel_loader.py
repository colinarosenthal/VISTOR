"""  
VISTOR Channel Loader  
  
Builds and loads the full set of channels for the Channel Manager,  
analogous to how ScheduleLoader builds the schedule library. Each  
channel is constructed here so the Channel Manager can self-populate  
on initialize() without callers registering channels manually.  
"""  
  
from core.logger import Logger  
  
from channel.channel import Channel  
  
  
class ChannelLoader:  
    """Builds and loads channels for the Channel Manager."""  
  
    def __init__(self):  
        self.channels = []  
  
        self.loaded = False  
  
    def load(self):  
        """Load all channels."""  
  
        Logger.info("Loading channels...")  
  
        self._load_default_channels()  
  
        self.loaded = True  
  
        Logger.info("Channels loaded.")  
  
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
  
    def _load_default_channels(self):  
        """Create the initial channel line-up."""  
  
        # NOTE: match this Channel(...) call to your real constructor.  
        self.channels.append(Channel(2, "VISTOR General"))
        self.channels.append(Channel(4, "VISTOR Movies"))