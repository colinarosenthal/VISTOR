"""  
VISTOR Commercial System Tests  
  
PoolSelector pool selection + broadcast-mode break-fill for commercials,  
network promos, and station IDs. Offline-safe.  
Run standalone: python src/tests/test_commercials.py  
"""  
  
import random  
import sys  
from pathlib import Path  
  
sys.path.append(str(Path(__file__).resolve().parent.parent))  
  
from scheduler.pool_selector import PoolSelector  
from scheduler.broadcast_modes import BetweenProgramsMode  
from scheduler.broadcast_event import (  
    BroadcastEvent,  
    BroadcastEventType,  
    make_commercial_block,  
    make_network_promo,  
    make_station_id,  
)  
  
print("\n=== Testing Pool Selector ===")  
  
# Empty pool -> empty selection (placeholder-block parity).  
assert PoolSelector([]).select() == []  
  
# Non-empty pool -> a bounded, ordered selection.  
pool = [f"ad{i}" for i in range(10)]  
sel = PoolSelector(pool, break_size=3, rng=random.Random(1))  
picked = sel.select()  
assert len(picked) == 3  
assert all(p in pool for p in picked)  
  
# Selection never exceeds the pool size.  
small = PoolSelector(["only"], break_size=5)  
assert len(small.select()) == 1  
  
print("Pool selection verified.")  
  
  
print("\n=== Testing Broadcast Mode Ad-Fill ===")  
  
  
class _P:  
    def __str__(self):  
        return "prog"  
  
  
# With a selector, breaks carry commercials.  
mode = BetweenProgramsMode(PoolSelector(pool, break_size=2))  
seq = mode.build_sequence([_P()])  
blocks = [i for i in seq if isinstance(i, BroadcastEvent)]  
assert blocks and blocks[0].get_items()  
print("Broadcast mode fills breaks from the pool.")  
  
# Without a selector, breaks stay empty (unchanged legacy behavior).  
mode_none = BetweenProgramsMode()  
seq_none = mode_none.build_sequence([_P()])  
blocks_none = [i for i in seq_none if isinstance(i, BroadcastEvent)]  
assert blocks_none and not blocks_none[0].get_items()  
print("Broadcast mode without a selector leaves breaks empty.")  
  
  
print("\n=== Testing Time/Season Weighting ===")  
  
from metadata.media.advertising.commercial import Commercial  
  
day = Commercial(id="c-day", title="Daytime Ad")  
day.set_airing_hours([9, 10, 11])  
night = Commercial(id="c-night", title="Late Night Ad")  
night.set_airing_hours([23])  
  
sel = PoolSelector([day, night], break_size=5)  
picked = [c.get_id() for c in sel.select(hour=10)]  
assert picked == ["c-day"], picked  
  
xmas = Commercial(id="c-xmas", title="Holiday Ad")  
xmas.set_airing_seasons(["christmas_day"])  
generic = Commercial(id="c-any", title="Generic Ad")  
sel2 = PoolSelector([xmas, generic], break_size=5)  
season_ids = {c.get_id() for c in sel2.select(season="christmas_day")}  
assert season_ids == {"c-xmas", "c-any"}, season_ids  
offseason = {c.get_id() for c in sel2.select(season="halloween")}  
assert offseason == {"c-any"}, offseason  
  
print("Time/season weighting verified.")  
  
  
print("\n=== Testing Generalized Pool Fill (Promos + Station IDs) ===")  
  
# PoolSelector is content-agnostic: the same logic fills promo and  
# station-ID breaks from their own pools.  
promo_pool = [f"promo{i}" for i in range(4)]  
promo_sel = PoolSelector(promo_pool, break_size=2, rng=random.Random(2))  
assert len(promo_sel.select()) == 2  
  
id_pool = [f"id{i}" for i in range(3)]  
id_sel = PoolSelector(id_pool, break_size=5)  
assert len(id_sel.select()) == 3  # never exceeds pool size  
  
# The three event constructors tag the correct BroadcastEventType and  
# carry their items.  
commercial_block = make_commercial_block(items=["ad0"])  
assert commercial_block.get_event_type() == BroadcastEventType.COMMERCIAL_BLOCK  
  
promo_block = make_network_promo(items=promo_sel.select())  
assert promo_block.get_event_type() == BroadcastEventType.NETWORK_PROMO  
assert promo_block.get_items()  
  
id_block = make_station_id(items=id_sel.select())  
assert id_block.get_event_type() == BroadcastEventType.STATION_ID  
assert id_block.get_items()  
  
print("Generalized pool fill verified.")  
  
print("\nCommercial system tests passed.")