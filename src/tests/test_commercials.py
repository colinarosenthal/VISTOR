"""  
VISTOR Commercial System Tests  
  
CommercialSelector pool selection + broadcast-mode ad-fill. Offline-safe.  
Run standalone: python src/tests/test_commercials.py  
"""  
  
import random  
import sys  
from pathlib import Path  
  
sys.path.append(str(Path(__file__).resolve().parent.parent))  
  
from scheduler.commercial_selector import CommercialSelector  
from scheduler.broadcast_modes import BetweenProgramsMode  
from scheduler.broadcast_event import BroadcastEvent  
  
print("\n=== Testing Commercial Selector ===")  
  
# Empty pool -> empty selection (placeholder-block parity).  
assert CommercialSelector([]).select() == []  
  
# Non-empty pool -> a bounded, ordered selection.  
pool = [f"ad{i}" for i in range(10)]  
sel = CommercialSelector(pool, break_size=3, rng=random.Random(1))  
picked = sel.select()  
assert len(picked) == 3  
assert all(p in pool for p in picked)  
  
# Selection never exceeds the pool size.  
small = CommercialSelector(["only"], break_size=5)  
assert len(small.select()) == 1  
  
print("Commercial selection verified.")  
  
  
print("\n=== Testing Broadcast Mode Ad-Fill ===")  
  
  
class _P:  
    def __str__(self):  
        return "prog"  
  
  
# With a selector, breaks carry commercials.  
mode = BetweenProgramsMode(CommercialSelector(pool, break_size=2))  
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
  
print("\nCommercial system tests passed.")

print("\n=== Testing Time/Season Weighting ===")  
  
from metadata.media.advertising.commercial import Commercial  
  
day = Commercial(id="c-day", title="Daytime Ad")  
day.set_airing_hours([9, 10, 11])  
night = Commercial(id="c-night", title="Late Night Ad")  
night.set_airing_hours([23])  
  
sel = CommercialSelector([day, night], break_size=5)  
picked = [c.get_id() for c in sel.select(hour=10)]  
assert picked == ["c-day"], picked  
  
xmas = Commercial(id="c-xmas", title="Holiday Ad")  
xmas.set_airing_seasons(["christmas_day"])  
generic = Commercial(id="c-any", title="Generic Ad")  
sel2 = CommercialSelector([xmas, generic], break_size=5)  
season_ids = {c.get_id() for c in sel2.select(season="christmas_day")}  
assert season_ids == {"c-xmas", "c-any"}, season_ids  
offseason = {c.get_id() for c in sel2.select(season="halloween")}  
assert offseason == {"c-any"}, offseason  
  
print("Time/season weighting verified.")