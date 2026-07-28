"""  
VISTOR Channel Manager  
  
Owns the full set of channels and the notion of which one is active.  
Every channel is ticked on every update so all channels progress in  
real time, regardless of which one the viewer is watching. Changing channels 
only re-points which channel's Player output is surfaced; it never restarts playback.  
"""  
  
from core.logger import Logger  
  
from channel.channel import Channel  
  
  
class ChannelManager:  
    """Manages all channels and the active/previous channel selection."""  
  
    # ------------------------------------------------------------------  
    # Construction  
    # ------------------------------------------------------------------  
  
    def __init__(self):  
        self.clock = None  
  
        self.channels = []  
        self.active_index = 0  
        self.previous_index = 0  
  
        self.initialized = False  
  
    # ------------------------------------------------------------------  
    # Lifecycle  
    # ------------------------------------------------------------------  
  
    def initialize(self, clock):  
        """Initialize every channel against the shared clock."""  
  
        Logger.info("Channel Manager initialized.")  
  
        self.clock = clock  
  
        # Self-populate the channel set (option B).  
        from channel.channel_loader import ChannelLoader  
    
        loader = ChannelLoader()  
        loader.load()  
        self.channels = loader.get_channels()  
    
        for channel in self.channels:  
            channel.initialize(clock)  
    
        self.initialized = True  
  
    def update(self, elapsed_seconds):  
        """Tick every channel so all lineups progress in real time."""  
  
        for channel in self.channels:  
            channel.update(elapsed_seconds)  
  
    def shutdown(self):  
        """Shutdown every channel."""  
  
        for channel in self.channels:  
            channel.shutdown()  
  
        self.channels.clear()  
  
        self.active_index = 0  
        self.previous_index = 0  
  
        self.initialized = False  
  
    def is_initialized(self):  
        """Return whether the manager has been initialized."""  
  
        return self.initialized  
  
    # ------------------------------------------------------------------  
    # Registration  
    # ------------------------------------------------------------------  
  
    def add_channel(self, channel: Channel):  
        """Register a channel. If the manager is already initialized,  
        initialize the new channel immediately so it stays time-synced."""  
  
        self.channels.append(channel)  
  
        if self.initialized and self.clock is not None:  
            channel.initialize(self.clock)  
  
    # ------------------------------------------------------------------  
    # Selection  
    # ------------------------------------------------------------------  
  
    def get_active_channel(self):  
        """Return the currently active channel, or None if there are none."""  
  
        if not self.channels:  
            return None  
  
        return self.channels[self.active_index]  
  
    def set_channel(self, index):  
        """Switch to the channel at the given index (no playback restart)."""  
  
        if not self.channels:  
            Logger.warning("No channels registered.")  
            return None  
  
        if index < 0 or index >= len(self.channels):  
            Logger.warning(f"Channel index {index} out of range.")  
            return self.get_active_channel()  
  
        self.previous_index = self.active_index  
        self.active_index = index  
  
        channel = self.get_active_channel()  
  
        Logger.info(  
            f"Switched to channel {channel.get_number()} "  
            f"'{channel.get_name()}'."  
        )  
  
        return channel

    def set_channel_by_number(self, number):  
        """Switch to the channel with the given on-screen number (Numeric Channel Entry)."""  
    
        for index, channel in enumerate(self.channels):  
            if channel.get_number() == number:  
                return self.set_channel(index)  
    
        Logger.warning(f"No channel with number {number}.")  
        return None
  
    def channel_up(self):  
        """Move to the next channel, wrapping around."""  
  
        if not self.channels:  
            return None  
  
        return self.set_channel((self.active_index + 1) % len(self.channels))  
  
    def channel_down(self):  
        """Move to the previous channel, wrapping around."""  
  
        if not self.channels:  
            return None  
  
        return self.set_channel((self.active_index - 1) % len(self.channels))  
  
    def previous_channel(self):  
        """Jump back to the last-watched channel (Previous Channel Support)."""  
  
        return self.set_channel(self.previous_index)  
  
    # ------------------------------------------------------------------  
    # Introspection  
    # ------------------------------------------------------------------  
  
    def get_channels(self):  
        """Return all registered channels."""  
  
        return self.channels  
  
    def count(self):  
        """Return the number of registered channels."""  
  
        return len(self.channels)