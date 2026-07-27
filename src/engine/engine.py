"""  
VISTOR Engine  
"""  
  
from core.logger import Logger  
from core.clock import Clock  
  
from scheduler.scheduler import Scheduler  
from scheduler.broadcast_controller import BroadcastController  
  
from player.player import Player  
from player.playback_queue import PlaybackQueue  
  
  
class Engine:  
    """Coordinates the VISTOR runtime."""  
  
    def __init__(self):  
        self.running = False  
        self.library = None  
  
        self.clock = None  
        self.scheduler = None  
  
        self.queue = None  
        self.broadcast_controller = None  
        self.player = None  
  
        self.current_block = None  
  
    def initialize(self):  
        """Initialize the engine."""  
  
        Logger.info("Engine initialized.")  
  
        self.clock = Clock()  
        self.clock.initialize()  
  
        self.scheduler = Scheduler(self.clock)  
        self.scheduler.initialize()  
  
        # Playback pipeline. The queue's ordering strategy is injectable,  
        # so a future UI broadcast-structure setting can swap ordering  
        # without touching the Engine or Player. The Broadcast Controller  
        # owns block -> queue population; the Engine never enqueues directly.  
        self.queue = PlaybackQueue()  
        self.broadcast_controller = BroadcastController(self.queue)  
        self.player = Player(self.queue)  
  
    def start(self):  
        """Start the engine."""  
  
        Logger.info("Starting engine...")  
  
        self.running = True  
  
        while self.running:  
            self.update()  
            break  
  
    def update(self):  
        """Run one engine update."""  
  
        # Capture real elapsed time from the Clock before advancing it.  
        previous_time = self.clock.get_time()  
        self.clock.update()  
        current_time = self.clock.get_time()  
  
        if previous_time is not None:  
            elapsed_seconds = (current_time - previous_time).total_seconds()  
        else:  
            elapsed_seconds = 0.0  
  
        self.scheduler.update()  
  
        # Refill the queue whenever the active programming block changes.  
        block = self.scheduler.get_current_block()  
  
        if block is not self.current_block:  
            self.current_block = block  
            self._on_block_change(block)  
  
        # Drive playback with real elapsed time.  
        self.player.tick(elapsed_seconds)  
  
        Logger.info("Engine update.")  
  
    def _on_block_change(self, block):  
        """Hand the new block to the Broadcast Controller to rebuild the queue."""  
  
        # The Broadcast Controller decides what goes in the queue (programs +  
        # any interruptions). The Engine only coordinates; it does not enqueue.  
        self.broadcast_controller.update(block)
  
        # Begin playback of the first queued item on the next tick.  
        self.player.load_next()  
  
    def stop(self):  
        """Stop the engine."""  
  
        Logger.info("Stopping engine...")  
  
        self.running = False  
  
    def shutdown(self):  
        """Shutdown the engine."""  
  
        Logger.info("Shutting down engine...")  
  
        self.running = False  
  
        if self.scheduler is not None:  
            self.scheduler.shutdown()  
  
        if self.clock is not None:  
            self.clock.shutdown()