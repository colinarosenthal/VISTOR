"""  
VISTOR Pool Selector  
  
Fills a broadcast break from a pool of media items -- commercials,  
network promos, or station IDs. Given one of a channel's pools, selects an  
ordered set of items for a single break, with hooks for time-of-day and  
seasonal weighting so the same pool feels different across the broadcast day.  
  
Offline-safe and dependency-free: an empty pool yields an empty selection,  
so broadcast modes with no content fall back to empty placeholder blocks  
exactly as they do today. Selection is the single place break-fill logic  
lives, keeping the Broadcast Modes and Player free of content decisions.  
"""  
  
import random  
  
from core.logger import Logger  
  
  
# Default number of items used to fill one break.  
_DEFAULT_BREAK_SIZE = 3  
  
  
class PoolSelector:  
    """Selects items from a pool to fill a single broadcast break."""  
  
    def __init__(self, pool=None, break_size=_DEFAULT_BREAK_SIZE, rng=None):  
        self.pool = list(pool or [])  
        self.break_size = break_size  
        # Injectable RNG keeps selection deterministic in tests.  
        self._rng = rng if rng is not None else random.Random()  
  
    def set_pool(self, pool):  
        """Replace the pool."""  
        self.pool = list(pool or [])  
  
    def select(self, count=None, hour=None, season=None):  
        """Return an ordered list of items for one break.  
  
        `hour` (0-23) and `season` bias which items are eligible; both  
        default to no filtering. Returns [] when the pool is empty, so a  
        channel with no content produces empty placeholder blocks.  
        """  
        if not self.pool:  
            return []  
  
        count = count or self.break_size  
  
        eligible = [c for c in self.pool if self._is_eligible(c, hour, season)]  
        if not eligible:  
            eligible = list(self.pool)  
  
        k = min(count, len(eligible))  
        selection = self._rng.sample(eligible, k)  
  
        Logger.info(  
            f"PoolSelector filled a break with {len(selection)} "  
            f"item(s) from a pool of {len(self.pool)}."  
        )  
        return selection  
  
    def _is_eligible(self, item, hour, season):  
        """Time-of-day / seasonal eligibility (best-effort, duck-typed).  
  
        Items may expose optional `airs_at_hour(hour)` and  
        `airs_in_season(season)` predicates; when absent, the item is  
        always eligible. This lets weighting be added to a media model  
        later without changing the selector or the broadcast modes.  
        """  
        if hour is not None and hasattr(item, "airs_at_hour"):  
            try:  
                if not item.airs_at_hour(hour):  
                    return False  
            except Exception:  # noqa: BLE001  
                pass  
  
        if season is not None and hasattr(item, "airs_in_season"):  
            try:  
                if not item.airs_in_season(season):  
                    return False  
            except Exception:  # noqa: BLE001  
                pass  
  
        return True