"""
VISTOR Rolling Cache Service

Headless disk-retention manager for Intelligent Content Management.

Implements three behaviors from the design:

1. Rolling Episode Window
   Keep only a small window of upcoming episodes on disk. As an episode
   airs, its file becomes evictable and the next episode enters the
   window (to be fetched by the resolver).

2. Retention-Driven Eviction
   When disk usage exceeds a budget, evict the lowest-value files first,
   ranked by retention_score (ties broken by larger file_size). Pinned
   assets are NEVER evicted regardless of score.

3. Deleted-Content Metadata Retention
   Eviction only removes the FILE (download_status -> MISSING). The
   MediaAsset and its owning MediaItem stay in the library, so the
   fingerprint/sources survive and the file can be re-fetched later.
"""

from metadata.enums.download_status import DownloadStatus

from core.logger import Logger


class RollingCache:
    """Manages which media files stay on disk."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self, window_size: int = 3):
        # How many upcoming episodes to keep resident per series.
        self.window_size = window_size

    # ------------------------------------------------------------------
    # Rolling Episode Window
    # ------------------------------------------------------------------

    def plan_window(self, episodes, aired_count: int):
        """
        Given an ordered list of episodes and how many have already
        aired, return a plan describing the rolling window.

        episodes    : list of Episode, ordered by air order.
        aired_count : number of leading episodes that have already aired.

        Returns a dict:
            {
                "keep":     [Episode, ...],   # inside the window, resident
                "fetch":    [Episode, ...],   # inside the window, missing
                "evict":    [Episode, ...],   # already aired, droppable
            }
        """

        window = episodes[aired_count:aired_count + self.window_size]
        aired = episodes[:aired_count]

        keep = []
        fetch = []

        for episode in window:
            if self._episode_available(episode):
                keep.append(episode)
            else:
                fetch.append(episode)

        # Everything already aired is a candidate for eviction (unless a
        # pinned asset guards it — handled by evict()).
        evict = [ep for ep in aired if self._episode_available(ep)]

        Logger.info(
            f"Rolling window: keep={len(keep)} "
            f"fetch={len(fetch)} evict={len(evict)}."
        )

        return {"keep": keep, "fetch": fetch, "evict": evict}

    # ------------------------------------------------------------------
    # Retention-Driven Eviction
    # ------------------------------------------------------------------

    def evict_to_budget(self, assets, budget_bytes: int):
        """
        Evict resident, unpinned assets (lowest retention first) until
        the total on-disk size is within budget_bytes.

        Deleted-Content Metadata Retention: eviction sets each removed
        asset's download_status to MISSING but never removes it from the
        library. Fingerprint and sources survive for later re-fetch.

        Returns a list of the asset_ids that were evicted.
        """

        resident = [a for a in assets if a.is_available()]

        current = sum(a.get_file_size() for a in resident)

        if current <= budget_bytes:
            Logger.info(
                f"On-disk usage {current} within budget {budget_bytes}; "
                f"no eviction."
            )
            return []

        # Evictable = resident AND not pinned. Rank lowest-value first:
        # lower retention_score first, then larger file_size (more
        # expensive to keep) first.
        evictable = [a for a in resident if not a.is_pinned()]

        evictable.sort(
            key=lambda a: (a.get_retention_score(), -a.get_file_size())
        )

        evicted = []

        for asset in evictable:

            if current <= budget_bytes:
                break

            # Delete the physical file so space is actually reclaimed.
            # Metadata (fingerprint/sources) is retained on the asset, so
            # the file can be re-fetched later (Deleted-Content Metadata
            # Retention).
            path = asset.get_path()
            try:
                if path.exists():
                    path.unlink()
            except OSError as error:
                Logger.error(
                    f"Could not delete '{asset.get_asset_id()}' "
                    f"at {path}: {error}; skipping."
                )
                continue

            asset.set_download_status(DownloadStatus.MISSING)

            current -= asset.get_file_size()

            evicted.append(asset.get_asset_id())

            Logger.warning(
                f"Evicted '{asset.get_asset_id()}' "
                f"(retention={asset.get_retention_score()}, "
                f"size={asset.get_file_size()}); metadata retained."
            )

        if current > budget_bytes:
            Logger.warning(
                f"Still over budget ({current} > {budget_bytes}) after "
                f"evicting all unpinned assets; pinned assets protected."
            )

        return evicted

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _episode_available(self, episode):
        """Return whether any of an episode's assets is on disk."""

        return any(
            asset.is_available()
            for asset in episode.get_media_assets()
        )
