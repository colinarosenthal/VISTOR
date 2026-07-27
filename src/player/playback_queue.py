"""  
VISTOR Playback Queue  
  
Holds the ordered sequence of media items the Player will consume.  
  
The PlaybackQueue implements the MediaSource contract expected by the  
Player: it hands out one media item at a time and never makes scheduling  
decisions. The order in which items are handed out is delegated to an  
injectable ordering strategy, so the eventual user-interface setting for  
broadcast structure can swap ordering behavior without changing the queue  
or the Player.  
"""  
  
from abc import ABC, abstractmethod  
  
from core.logger import Logger  
  
  
# ----------------------------------------------------------------------  
# Ordering Strategies  
# ----------------------------------------------------------------------  
  
class QueueOrderingStrategy(ABC):  
    """  
    Defines how enqueued media items are ordered before playback.  
  
    Concrete strategies receive the raw list of enqueued items and return  
    a new list in the desired play order. Strategies must not mutate the  
    input list and must not drop or duplicate items.  
    """  
  
    @abstractmethod  
    def order(self, items):  
        """Return a new list of items in play order."""  
  
        raise NotImplementedError  
  
  
class SequentialOrdering(QueueOrderingStrategy):  
    """Default FIFO ordering. Items play in the order they were enqueued."""  
  
    def order(self, items):  
        """Return items unchanged, preserving insertion order."""  
  
        return list(items)  
  
  
# ----------------------------------------------------------------------  
# Playback Queue  
# ----------------------------------------------------------------------  
  
class PlaybackQueue:  
    """  
    An ordered, consumable sequence of media items for the Player.  
  
    Implements the MediaSource contract (has_next / get_next / peek).  
    Ordering is applied lazily whenever the queue is (re)built, using the  
    injected QueueOrderingStrategy. Injecting a different strategy later  
    changes play order without changing this class or the Player.  
    """  
  
    # ------------------------------------------------------------------  
    # Construction  
    # ------------------------------------------------------------------  
  
    def __init__(self, ordering_strategy=None):  
        # Raw, insertion-ordered items as enqueued by the caller.  
        self._items = []  
  
        # Ordered view produced by the strategy; the cursor walks this.  
        self._ordered = []  
  
        self._cursor = 0  
  
        # Whether _ordered is stale relative to _items.  
        self._dirty = False  
  
        self._ordering_strategy = ordering_strategy or SequentialOrdering()  
  
    # ------------------------------------------------------------------  
    # Queue Building  
    # ------------------------------------------------------------------  
  
    def enqueue(self, media_item):  
        """Add a single media item to the queue."""  
  
        self._items.append(media_item)  
  
        self._dirty = True  
  
    def extend(self, media_items):  
        """Add multiple media items to the queue."""  
  
        for media_item in media_items:  
            self._items.append(media_item)  
  
        self._dirty = True  
  
    def clear(self):  
        """Remove all items and reset the cursor."""  
  
        self._items.clear()  
        self._ordered.clear()  
        self._cursor = 0  
        self._dirty = False  
  
    def set_ordering_strategy(self, ordering_strategy):  
        """  
        Replace the ordering strategy.  
  
        This is the hook for the future UI broadcast-structure setting.  
        The queue is marked dirty so the new order applies on next read.  
        """  
  
        self._ordering_strategy = ordering_strategy or SequentialOrdering()  
  
        self._dirty = True  
  
    # ------------------------------------------------------------------  
    # Internal  
    # ------------------------------------------------------------------  
  
    def _rebuild(self):  
        """Apply the ordering strategy and reset the cursor."""  
  
        self._ordered = self._ordering_strategy.order(self._items)  
  
        self._cursor = 0  
  
        self._dirty = False  
  
    def _ensure_ordered(self):  
        """Rebuild the ordered view if it is stale."""  
  
        if self._dirty:  
            self._rebuild()  
  
    # ------------------------------------------------------------------  
    # MediaSource Contract  
    # ------------------------------------------------------------------  
  
    def has_next(self):  
        """Return whether another item is available to play."""  
  
        self._ensure_ordered()  
  
        return self._cursor < len(self._ordered)  
  
    def get_next(self):  
        """  
        Return the next media item and advance the cursor.  
  
        Returns None when the queue is exhausted.  
        """  
  
        self._ensure_ordered()  
  
        if self._cursor >= len(self._ordered):  
            Logger.info("Playback queue exhausted.")  
  
            return None  
  
        media_item = self._ordered[self._cursor]  
  
        self._cursor += 1  
  
        return media_item  
  
    def peek(self):  
        """Return the next media item without advancing the cursor."""  
  
        self._ensure_ordered()  
  
        if self._cursor >= len(self._ordered):  
            return None  
  
        return self._ordered[self._cursor]  
  
    def reset(self):  
        """Rewind to the start of the current order without rebuilding."""  
  
        self._cursor = 0  
  
    # ------------------------------------------------------------------  
    # Introspection  
    # ------------------------------------------------------------------  
  
    def size(self):  
        """Return the total number of enqueued items."""  
  
        return len(self._items)  
  
    def remaining(self):  
        """Return the number of items not yet played."""  
  
        self._ensure_ordered()  
  
        return max(0, len(self._ordered) - self._cursor)