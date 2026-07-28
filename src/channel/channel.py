"""  
VISTOR Channel  
  
A Channel represents a single always-on broadcast lineup. Each channel  
owns its own broadcast pipeline (Scheduler -> Broadcast Controller ->  
Playback Queue -> Player) so that every channel progresses independently  
of whether the viewer is currently watching it.  
"""  
  
from core.logger import Logger  
  
from scheduler.scheduler import Scheduler  
from scheduler.broadcast_controller import BroadcastController  
from player.playback_queue import PlaybackQueue  
from player.player import Player  
  
  
class Channel:  
    """Represents a single television channel with its own broadcast pipeline."""  
  
    # ------------------------------------------------------------------  
    # Construction  
    # ------------------------------------------------------------------  
  
    def __init__(  
        self,  
        number,  
        name,  
        logo="",  
        primary_genre=None,  
        target_audience="",  
        network_branding="",  
    ):  
        # --- Identity (Design Bible Section 10) ---  
        self.number = number  
        self.name = name  
        self.logo = logo  
        self.primary_genre = primary_genre  
        self.target_audience = target_audience  
        self.network_branding = network_branding  
  
        # --- Content pools (populated from metadata in a later step) ---  
        self.programming_sources = []  
        self.commercial_pool = []  
        self.promotional_material = []  
        self.station_ids = []  
  
        # --- Broadcast pipeline (built in initialize) ---  
        # This channel owns its own Scheduler -> Broadcast Controller ->  
        # Playback Queue -> Player so it can keep airing independently.  
        self.scheduler = None  
        self.queue = None  
        self.broadcast_controller = None  
        self.player = None  
  
        self.current_block = None  
  
        self.initialized = False  
  
    # ------------------------------------------------------------------  
    # Lifecycle  
    # ------------------------------------------------------------------  
  
    def initialize(self, clock):  
        """  
        Initialize the channel's own broadcast pipeline against a shared clock.  
  
        The Clock is shared across all channels so each channel's schedule  
        advances with the same wall-clock time. This is what lets a channel  
        keep "airing" while the viewer is elsewhere.  
        """  
  
        # Schedule (time -> programming block)  
        self.scheduler = Scheduler(clock)  
        self.scheduler.initialize()  
  
        # Playback pipeline. The queue's ordering strategy is injectable, so a  
        # future UI broadcast-structure setting can swap ordering without  
        # touching the Channel or Player. The Broadcast Controller owns  
        # block -> queue population; the Channel only coordinates.  
        self.queue = PlaybackQueue()  
        self.broadcast_controller = BroadcastController(self.queue)  
        self.player = Player(self.queue)  
  
        self.initialized = True  
  
        Logger.info(f"Channel {self.number} '{self.name}' initialized.")  
  
    def update(self, elapsed_seconds):  
        """  
        Advance this channel's schedule and playback by elapsed time.  
  
        Called every engine tick regardless of whether the viewer is  
        currently watching this channel, so every channel stays time-synced  
        and never stops.  
        """  
  
        if not self.initialized:  
            return  
  
        self.scheduler.update()  
  
        # Refill the queue whenever the active programming block changes.  
        block = self.scheduler.get_current_block()  
  
        if block is not self.current_block:  
            self.current_block = block  
            self._on_block_change(block)  
  
        # Continue to the next queued item when the current one finishes.  
        if self.player.is_finished():  
            if self.player.load_next():  
                self.player.play()  
  
        # Drive playback with real elapsed time.  
        self.player.tick(elapsed_seconds)  
  
    def _on_block_change(self, block):  
        """Hand the new block to the Broadcast Controller to rebuild the queue."""  
  
        if block is None:  
            return  
  
        # The Broadcast Controller decides what goes in the queue (programs +  
        # any interruptions). The Channel only coordinates; it does not enqueue.  
        self.broadcast_controller.update(block)  
  
        # Begin playback of the first queued item.  
        if self.player.load_next():  
            self.player.play()  
  
    def shutdown(self):  
        """Shutdown the channel's pipeline."""  
  
        if self.player is not None:  
            self.player.stop()  
  
        if self.scheduler is not None:  
            self.scheduler.shutdown()  
  
        self.initialized = False  
  
    def is_initialized(self):  
        """Return whether the channel has been initialized."""  
  
        return self.initialized  
  
    # ------------------------------------------------------------------  
    # Broadcast Pipeline  
    # ------------------------------------------------------------------  
  
    def get_scheduler(self):  
        """Return this channel's scheduler."""  
  
        return self.scheduler  
  
    def get_queue(self):  
        """Return this channel's playback queue."""  
  
        return self.queue  
  
    def get_broadcast_controller(self):  
        """Return this channel's broadcast controller."""  
  
        return self.broadcast_controller  
  
    def get_player(self):  
        """Return this channel's player."""  
  
        return self.player  
  
    def get_current_block(self):  
        """Return the programming block airing on this channel right now."""  
  
        if self.scheduler is None:  
            return None  
  
        return self.scheduler.get_current_block()  
  
    def get_current_schedule(self):  
        """Return this channel's currently active schedule."""  
  
        if self.scheduler is None:  
            return None  
  
        return self.scheduler.get_current_schedule()  
  
    # ------------------------------------------------------------------  
    # Identity (Design Bible Section 10)  
    # ------------------------------------------------------------------  
  
    def get_number(self):  
        """Return the channel number."""  
  
        return self.number  
  
    def get_name(self):  
        """Return the channel name."""  
  
        return self.name  
  
    def get_logo(self):  
        """Return the channel logo."""  
  
        return self.logo  
  
    def set_logo(self, logo):  
        """Set the channel logo."""  
  
        self.logo = logo  
  
    def get_primary_genre(self):  
        """Return the channel's primary genre."""  
  
        return self.primary_genre  
  
    def set_primary_genre(self, genre):  
        """Set the channel's primary genre."""  
  
        self.primary_genre = genre  
  
    def get_target_audience(self):  
        """Return the channel's target audience."""  
  
        return self.target_audience  
  
    def set_target_audience(self, target_audience):  
        """Set the channel's target audience."""  
  
        self.target_audience = target_audience  
  
    def get_network_branding(self):  
        """Return the channel's network branding."""  
  
        return self.network_branding  
  
    def set_network_branding(self, network_branding):  
        """Set the channel's network branding."""  
  
        self.network_branding = network_branding  
  
    # ------------------------------------------------------------------  
    # Programming Sources  
    # ------------------------------------------------------------------  
  
    def add_programming_source(self, source):  
        """Add a programming source to this channel."""  
  
        self.programming_sources.append(source)  
  
    def get_programming_sources(self):  
        """Return this channel's programming sources."""  
  
        return self.programming_sources  
  
    # ------------------------------------------------------------------  
    # Commercial Pool  
    # ------------------------------------------------------------------  
  
    def add_commercial(self, commercial):  
        """Add a commercial to this channel's commercial pool."""  
  
        self.commercial_pool.append(commercial)  
  
    def get_commercial_pool(self):  
        """Return this channel's commercial pool."""  
  
        return self.commercial_pool  
  
    # ------------------------------------------------------------------  
    # Promotional Material  
    # ------------------------------------------------------------------  
  
    def add_promo(self, promo):  
        """Add promotional material to this channel."""  
  
        self.promotional_material.append(promo)  
  
    def get_promotional_material(self):  
        """Return this channel's promotional material."""  
  
        return self.promotional_material  
  
    # ------------------------------------------------------------------  
    # Station Identification  
    # ------------------------------------------------------------------  
  
    def add_station_id(self, station_id):  
        """Add a station identification asset to this channel."""  
  
        self.station_ids.append(station_id)  
  
    def get_station_ids(self):  
        """Return this channel's station identification assets."""  
  
        return self.station_ids