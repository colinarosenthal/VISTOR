"""  
VISTOR Commercial Selector  
  
Fills commercial blocks from a pool of Commercial items. Given a channel's  
commercial pool, selects an ordered set of commercials for a single break,  
with hooks for time-of-day and seasonal weighting so the same pool feels  
different across the broadcast day.  
  
Offline-safe and dependency-free: an empty pool yields an empty selection,  
so broadcast modes with no commercials fall back to empty placeholder blocks  
exactly as they do today. Selection is the single place ad-fill logic lives,  
keeping the Broadcast Modes and Player free of content decisions.  
"""  
  
import random  
  
from core.logger import Logger  
  
  
# Default number of commercials used to fill one break.  
_DEFAULT_BREAK_SIZE = 3  
  
  
class CommercialSelector:  
    """Selects commercials from a pool for a single commercial block."""  
  
    def __init__(self, pool=None, break_size=_DEFAULT_BREAK_SIZE, rng=None):  
        self.pool = list(pool or [])  
        self.break_size = break_size  
        # Injectable RNG keeps selection deterministic in tests.  
        self._rng = rng if rng is not None else random.Random()  
  
    def set_pool(self, pool):  
        """Replace the commercial pool."""  
        self.pool = list(pool or [])  
  
    def select(self, count=None, hour=None, season=None):  
        """Return an ordered list of Commercials for one break.  
  
        `hour` (0-23) and `season` bias which commercials are eligible; both  
        default to no filtering. Returns [] when the pool is empty, so a  
        channel with no commercials produces empty placeholder blocks.  
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
            f"CommercialSelector filled a break with {len(selection)} "  
            f"commercial(s) from a pool of {len(self.pool)}."  
        )  
        return selection  
  
    def _is_eligible(self, commercial, hour, season):  
        """Time-of-day / seasonal eligibility (best-effort, duck-typed).  
  
        Commercials may expose optional `airs_at_hour(hour)` and  
        `airs_in_season(season)` predicates; when absent, the commercial is  
        always eligible. This lets weighting be added to the Commercial model  
        later without changing the selector or the broadcast modes.  
        """  
        if hour is not None and hasattr(commercial, "airs_at_hour"):  
            try:  
                if not commercial.airs_at_hour(hour):  
                    return False  
            except Exception:  # noqa: BLE001  
                pass  
  
        if season is not None and hasattr(commercial, "airs_in_season"):  
            try:  
                if not commercial.airs_in_season(season):  
                    return False  
            except Exception:  # noqa: BLE001  
                pass  
  
        return True