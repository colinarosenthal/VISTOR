"""  
VISTOR Broadcast Controller  
  
Sits between the Scheduler and the Playback Queue in the broadcast  
pipeline. Given the programming block the Scheduler selected, the  
Broadcast Controller decides the airing sequence and fills the Playback  
Queue. It is the single place interruption behavior (commercial breaks,  
station IDs, future event types) is decided, so the Player never makes  
scheduling decisions.  
  
Sequencing is delegated to an injectable broadcast mode so the future  
user-interface setting for broadcast structure can change how the queue  
is filled without touching the Queue or the Player.  
"""  
  
from core.logger import Logger  
  
  
class BroadcastController:  
    """Fills the Playback Queue from the Scheduler's current block."""  
  
    def __init__(self, queue, mode=None):  
        self.queue = queue  
        self.mode = mode  
        self.current_block = None  
  
    def set_mode(self, mode):  
        """Inject a broadcast mode (ordering / interruption strategy)."""  
  
        self.mode = mode  
  
    def update(self, block):  
        """React to the Scheduler's current block.  
  
        Rebuilds the queue only when the active block actually changes,  
        so a steady-state block does not wipe playback every tick.  
        """  
  
        if block is self.current_block:  
            return  
  
        self.current_block = block  
  
        self.queue.clear()  
  
        if block is None:  
            Logger.warning("No active programming block; queue left empty.")  
            return  
  
        items = block.get_items()  
  
        if not items:  
            Logger.warning(  
                f"Programming block '{block.get_name()}' has no media items."  
            )  
            return  
  
        sequence = self._build_sequence(items)  
  
        if not sequence:  
            Logger.warning(  
                f"Broadcast mode produced no items for block "  
                f"'{block.get_name()}'; queue left empty."  
            )  
            return  
  
        for item in sequence:  
            self.queue.enqueue(item)  
  
        Logger.info(  
            f"Broadcast Controller filled queue for block "  
            f"'{block.get_name()}' ({len(sequence)} item(s) from "  
            f"{len(items)} program(s))."  
        )  
  
    def _build_sequence(self, items):  
        """Produce the airing order for a block's items.  
  
        Default (Broadcast Mode: Off) airs programs in order with no  
        interruptions. When a mode is injected, delegate to it so  
        commercial blocks / future events can be interleaved without  
        changing this class.  
        """  
  
        if self.mode is not None:  
            return list(self.mode.build_sequence(items))  
  
        return list(items)