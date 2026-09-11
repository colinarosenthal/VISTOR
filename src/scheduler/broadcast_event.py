"""
VISTOR Broadcast Event

A Broadcast Event is a non-program interruption the Broadcast Controller
can interleave with programs (commercial blocks, station IDs, network
promos, and future event types such as breaking news / EAS / weather).
Modeling interruptions as first-class items lets the Broadcast Modes
insert them into the Playback Queue without the Player making any
scheduling decisions.
"""

from enum import Enum


class BroadcastEventType(Enum):
    """The kind of interruption a BroadcastEvent represents."""

    COMMERCIAL_BLOCK = "commercial_block"
    STATION_ID = "station_id"
    NETWORK_PROMO = "network_promo"

    # Reserved for future event types (Design Bible -> Future Expansion).
    BREAKING_NEWS = "breaking_news"
    EMERGENCY_ALERT = "emergency_alert"
    WEATHER = "weather"


class BroadcastEvent:
    """A schedulable interruption placed between or inside programs.

    Kept intentionally lightweight: it is a marker the Broadcast
    Controller enqueues like any other item. Real commercial / station-ID
    media can be attached later via `items` without changing the modes or
    the Player.
    """

    def __init__(self, event_type, duration_seconds=0, items=None, label=""):
        self.event_type = event_type
        self.duration_seconds = duration_seconds
        self.items = list(items) if items else []
        self.label = label or event_type.value

    def is_event(self):
        """Marker so the Player / Queue can tell events from programs."""
        return True

    def get_event_type(self):
        return self.event_type

    def get_duration_seconds(self):
        return self.duration_seconds

    def get_items(self):
        return self.items

    def get_label(self):
        return self.label

    def __str__(self):
        return f"[BroadcastEvent {self.label}]"


def make_commercial_block(duration_seconds=0, items=None):
    """Convenience constructor for the most common event type."""
    return BroadcastEvent(
        BroadcastEventType.COMMERCIAL_BLOCK,
        duration_seconds=duration_seconds,
        items=items,
        label="Commercial Block",
    )

def make_station_id(duration_seconds=0, items=None):  
    """Convenience constructor for a station-identification event."""  
    return BroadcastEvent(  
        BroadcastEventType.STATION_ID,  
        duration_seconds=duration_seconds,  
        items=items,  
        label="Station ID",  
    )  
  
  
def make_network_promo(duration_seconds=0, items=None):  
    """Convenience constructor for a network-promo event."""  
    return BroadcastEvent(  
        BroadcastEventType.NETWORK_PROMO,  
        duration_seconds=duration_seconds,  
        items=items,  
        label="Network Promo",  
    )