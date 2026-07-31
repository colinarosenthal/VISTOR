"""  
VISTOR Acquisition Loop  
  
Ties the RollingCache window plan to the SourceResolver so a series keeps  
exactly a small window of upcoming episodes on disk: aired episodes become  
evictable, and missing in-window episodes are fetched from their sources.  
"""  
  
from core.logger import Logger  
  
  
class AcquisitionLoop:  
    """Keeps a series' rolling window populated on disk."""  
  
    def __init__(self, rolling_cache, resolver):  
        self.rolling_cache = rolling_cache  
        self.resolver = resolver  
  
    def run_for_series(self, episodes, aired_count, candidates=None):  
        """  
        Fetch missing in-window episodes and report the window state.  
  
        episodes    : Episodes in air order.  
        aired_count : how many leading episodes have already aired.  
        candidates  : optional replacement asset pool for the resolver.  
  
        Returns:  
            {"fetched": [asset_id, ...], "failed": [asset_id, ...],  
             "evictable": [episode_id, ...]}  
        """  
  
        plan = self.rolling_cache.plan_window(episodes, aired_count)  
  
        fetched = []  
        failed = []  
  
        for episode in plan["fetch"]:  
            for asset in episode.get_media_assets():  
                report = self.resolver.resolve(asset, candidates=candidates)  
                if report["resolved"] or report["replacement"]:  
                    fetched.append(asset.get_asset_id())  
                else:  
                    failed.append(asset.get_asset_id())  
  
        evictable = [ep.get_id() for ep in plan["evict"]]  
  
        Logger.info(  
            f"Acquisition loop: fetched={len(fetched)} "  
            f"failed={len(failed)} evictable={len(evictable)}."  
        )  
  
        return {"fetched": fetched, "failed": failed, "evictable": evictable}