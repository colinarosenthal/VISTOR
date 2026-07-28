"""  
VISTOR Engine  
"""  
  
from core.logger import Logger  
from core.clock import Clock  
  
from channel.channel_manager import ChannelManager  
  
  
class Engine:  
    """Coordinates the VISTOR runtime."""  
  
    def __init__(self):  
        self.running = False  
        self.library = None  
  
        # One shared Clock drives every channel so all channels stay  
        # time-synced and keep airing whether or not they are being watched.  
        self.clock = None  
  
        # The ChannelManager owns the set of channels and tracks the active  
        # (and previous) channel. Each channel owns its own broadcast pipeline.  
        self.channel_manager = None  
  
    def initialize(self):  
        """Initialize the engine."""  
  
        Logger.info("Engine initialized.")  
  
        self.clock = Clock()  
        self.clock.initialize()  
  
        # Every channel is initialized against the shared Clock. Channels are  
        # registered before initialize() (by a ChannelLoader in a later step)  
        # or via channel_manager.add_channel(...).  
        self.channel_manager = ChannelManager()  
        self.channel_manager.initialize(self.clock)  
  
    def start(self):  
        """Start the engine."""  
  
        Logger.info("Starting engine...")  
  
        self.running = True  
  
        while self.running:  
            self.update()  
            break  
  
    def update(self):  
        """Run one engine update."""  
  
        # Capture real elapsed time from the shared Clock before advancing it.  
        previous_time = self.clock.get_time()  
        self.clock.update()  
        current_time = self.clock.get_time()  
  
        if previous_time is not None:  
            elapsed_seconds = (current_time - previous_time).total_seconds()  
        else:  
            elapsed_seconds = 0.0  
  
        # Tick EVERY channel with the same elapsed time so unattended channels  
        # progress exactly as much as the one being watched. This is what makes  
        # "channels never stop" and "resume playback after channel changes"  
        # work: switching channels just changes which channel's player output  
        # the viewer sees; no channel is ever paused or restarted.  
        self.channel_manager.update(elapsed_seconds)  
  
        Logger.info("Engine update.")  
  
    # ------------------------------------------------------------------  
    # Active Channel (what the viewer currently sees)  
    # ------------------------------------------------------------------  
  
    def get_active_channel(self):  
        """Return the channel the viewer is currently watching."""  
  
        if self.channel_manager is None:  
            return None  
  
        return self.channel_manager.get_active_channel()  
  
    def get_active_player(self):  
        """Return the player of the currently watched channel."""  
  
        channel = self.get_active_channel()  
  
        if channel is None:  
            return None  
  
        return channel.get_player()  
  
    def stop(self):  
        """Stop the engine."""  
  
        Logger.info("Stopping engine...")  
  
        self.running = False  
  
    def shutdown(self):  
        """Shutdown the engine."""  
  
        Logger.info("Shutting down engine...")  
  
        self.running = False  
  
        if self.channel_manager is not None:  
            self.channel_manager.shutdown()  
  
        if self.clock is not None:  
            self.clock.shutdown()