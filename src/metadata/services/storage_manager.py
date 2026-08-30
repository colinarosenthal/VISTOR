"""  
VISTOR Storage Manager  
  
Runtime enforcement of the on-disk storage budget. Collects every resident  
MediaAsset across the library and hands them to RollingCache.evict_to_budget,  
which deletes the lowest-retention unpinned files until on-disk usage fits  
within Config.storage_budget_bytes.  
  
Budget = 0 means "disabled": no eviction ever runs. This is the safe default  
until an external drive is configured as the media root (#1).  
"""  
  
from core.config import Config  
from core.logger import Logger  
  
from metadata.services.rolling_cache import RollingCache  
  
  
class StorageManager:  
    """Enforces the configured on-disk storage budget across the library."""  
  
    def __init__(self, library, config=None, cache=None):  
        self.library = library  
        self.config = config if config is not None else Config().load()  
        self.cache = cache if cache is not None else RollingCache()  
  
    def _resident_assets(self):  
        """Every downloaded, on-disk asset in the library."""  
  
        assets = []  
  
        for item in self.library.get_media():  
            for asset in item.get_media_assets():  
                if asset.is_available():  
                    assets.append(asset)  
  
        return assets  
  
    def enforce_budget(self):  
        """Evict lowest-retention files until on-disk usage fits the budget.  
  
        Returns the list of evicted asset_ids ([] when disabled or already  
        within budget).  
        """  
  
        budget = self.config.get_storage_budget_bytes()  
  
        if budget <= 0:  
            return []  
  
        assets = self._resident_assets()  
  
        evicted = self.cache.evict_to_budget(assets, budget)  
  
        if evicted:  
            Logger.info(  
                f"StorageManager evicted {len(evicted)} asset(s) "  
                f"to fit budget {budget} bytes."  
            )  
  
        return evicted