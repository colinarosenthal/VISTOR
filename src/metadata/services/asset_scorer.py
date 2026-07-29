"""  
VISTOR Asset Scorer Service  
  
Computes the two deliberately-separate scores for a MediaAsset:  
  
  * Broadcast Score  — how likely the asset is to AIR. Driven only by  
    airplay signals (repurposability across channels, non-seasonal vs  
    seasonal, overall appeal). Never mixed with storage cost.  
  
  * Retention Score  — whether the file should STAY ON DISK. A combined  
    score derived from the broadcast score, the "at-risk" fragility of  
    the asset's sources (few / young / unreliable sources raise it), and  
    the storage footprint (larger files are more expensive to keep, so  
    they lower it).  
  
Pinning is a hard override handled by should_evict(): a pinned asset is  
never evicted regardless of score.  
  
This service is headless and deterministic so it can be unit-tested with  
no media files, network, or GUI.  
"""  
  
from core.logger import Logger  
  
  
class AssetScorer:  
    """Computes broadcast and retention scores for media assets."""  
  
    # ------------------------------------------------------------------  
    # Tunable weights / reference points  
    # ------------------------------------------------------------------  
  
    # A source that has been posted this many days is treated as fully  
    # "settled" (lowest takedown risk). Younger postings are more at-risk.  
    SETTLED_AGE_DAYS = 365 * 3  
  
    # File size (bytes) treated as the reference "large" footprint. Files  
    # at or above this size get the maximum storage penalty.  
    LARGE_FILE_BYTES = 4 * 1024 * 1024 * 1024  # 4 GiB  
  
    # Retention blend weights (must sum to 1.0).  
    BROADCAST_WEIGHT = 0.5  
    FRAGILITY_WEIGHT = 0.3  
    STORAGE_WEIGHT = 0.2  
  
    # ------------------------------------------------------------------  
    # Broadcast Score  
    # ------------------------------------------------------------------  
  
    def compute_broadcast_score(  
        self,  
        asset,  
        channel_count: int = 0,  
        is_seasonal: bool = False,  
        appeal: float = 0.0,  
    ):  
        """  
        Compute and store the broadcast (airplay-likelihood) score in  
        the range 0.0 - 10.0.  
  
        channel_count : how many channels can use this asset (more =  
                        more repurposable = higher).  
        is_seasonal   : seasonal content sits in a lower bracket than  
                        evergreen content.  
        appeal        : 0.0 - 10.0 overall appeal (rating / popularity).  
        """  
  
        # Repurposability: saturates so a huge channel count can't dwarf  
        # everything else. 0 channels -> 0, 4+ channels -> ~1.0.  
        repurposability = min(channel_count, 4) / 4.0  
  
        seasonal_bracket = 0.4 if is_seasonal else 1.0  
  
        appeal_norm = max(0.0, min(appeal, 10.0)) / 10.0  
  
        # Blend, then scale to 0-10.  
        raw = (  
            0.4 * repurposability +  
            0.3 * seasonal_bracket +  
            0.3 * appeal_norm  
        )  
  
        score = round(raw * 10.0, 4)  
  
        asset.set_broadcast_score(score)  
  
        Logger.info(  
            f"Broadcast score for '{asset.get_asset_id()}' -> {score}."  
        )  
  
        return score  
  
    # ------------------------------------------------------------------  
    # Retention Score  
    # ------------------------------------------------------------------  
  
    def compute_retention_score(self, asset):  
        """  
        Compute and store the retention (keep-on-disk) score in the range  
        0.0 - 10.0, combining broadcast score, source fragility, and  
        storage footprint. Reads broadcast_score off the asset, so call  
        compute_broadcast_score() first if you want them consistent.  
        """  
  
        broadcast_norm = max(0.0, min(asset.get_broadcast_score(), 10.0)) / 10.0  
  
        fragility = self._source_fragility(asset)  
  
        storage_penalty = self._storage_penalty(asset)  
  
        # Higher fragility raises retention; higher storage cost lowers it.  
        raw = (  
            self.BROADCAST_WEIGHT * broadcast_norm +  
            self.FRAGILITY_WEIGHT * fragility +  
            self.STORAGE_WEIGHT * (1.0 - storage_penalty)  
        )  
  
        score = round(raw * 10.0, 4)  
  
        asset.set_retention_score(score)  
  
        Logger.info(  
            f"Retention score for '{asset.get_asset_id()}' -> {score}."  
        )  
  
        return score  
  
    # ------------------------------------------------------------------  
    # Fragility / storage helpers  
    # ------------------------------------------------------------------  
  
    def _source_fragility(self, asset):  
        """  
        Return 0.0 (rock-solid) - 1.0 (extremely at-risk).  
  
        Fewer sources = more fragile. A younger newest-source posting is  
        more at-risk than one that has survived for years (a link up for  
        3+ years is unlikely to disappear soon).  
        """  
  
        sources = asset.get_sources()  
  
        if not sources:  
            # No known source at all is the most at-risk state.  
            return 1.0  
  
        # Scarcity: 1 source -> 1.0, 4+ sources -> ~0.0.  
        scarcity = 1.0 - (min(len(sources), 4) - 1) / 3.0  
  
        # Age risk: use the settled (oldest) posting as the safety anchor.  
        age_days = self._newest_settled_age(asset)  
        age_risk = 1.0 - min(age_days, self.SETTLED_AGE_DAYS) / self.SETTLED_AGE_DAYS  
  
        # Blend scarcity and age risk equally.  
        return round((scarcity + age_risk) / 2.0, 4)  
  
    def _newest_settled_age(self, asset):  
        """  
        Return the age (in days) of the most-settled source, i.e. the  
        source that has been up the longest, since that is the strongest  
        argument the media is durable. Falls back to 0 if unknown.  
        """  
  
        getter = getattr(asset, "get_source_age_days", None)  
  
        if callable(getter):  
            try:  
                return max(0, int(getter()))  
            except (TypeError, ValueError):  
                return 0  
  
        return 0  
  
    def _storage_penalty(self, asset):  
        """Return 0.0 (tiny) - 1.0 (very large) based on file size."""  
  
        size = asset.get_file_size() or 0  
  
        return round(min(size, self.LARGE_FILE_BYTES) / self.LARGE_FILE_BYTES, 4)  
  
    # ------------------------------------------------------------------  
    # Eviction decision (pinning override)  
    # ------------------------------------------------------------------  
  
    def should_evict(self, asset, threshold: float = 3.0):  
        """  
        Return whether this asset is a candidate for on-disk eviction.  
  
        A pinned asset is NEVER evicted regardless of score. Otherwise an  
        asset is evictable when its retention score falls below the given  
        threshold.  
        """  
  
        if asset.is_pinned():  
            return False  
  
        return asset.get_retention_score() < threshold