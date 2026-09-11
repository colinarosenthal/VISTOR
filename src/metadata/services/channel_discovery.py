"""
VISTOR Channel Discovery

Selects catalog MediaItems that match a Channel's specification so free
disk space can be filled with channel-appropriate content. Operates only
over the known metadata catalog (see Docs/Ideas.md "Catalogue Expansion"
for the deferred uncatalogued-search feature).

Richer matching: genre + target audience + tag overlap, with the channel's
programming_sources acting as a hard allow-list when non-empty.
"""

from core.logger import Logger


class ChannelDiscovery:
    """Ranks catalog items by fit to a channel's specification."""

    def discover(self, channel, media_items, limit=None):
        """
        Return channel-appropriate media items ranked by match score.

        A programming_sources allow-list (if the channel defines one) is a
        hard filter: an item whose id is not permitted is excluded even if
        it otherwise matches.
        """

        allow_list = set(channel.get_programming_sources() or [])

        scored = []

        for item in media_items:
            if allow_list and item.get_id() not in allow_list:
                continue

            score = self._match_score(channel, item)

            if score > 0:
                scored.append((score, item))

        scored.sort(key=lambda pair: pair[0], reverse=True)

        results = [item for _, item in scored]

        if limit is not None:
            results = results[:limit]

        Logger.info(
            f"Channel '{channel.name}' discovery: "
            f"{len(results)} candidate(s) from {len(media_items)} item(s)."
        )

        return results

    # ------------------------------------------------------------------
    # Match scoring
    # ------------------------------------------------------------------

    def _match_score(self, channel, item):
        """Weighted fit: genre (primary), audience, tag overlap."""

        score = 0.0

        genre = (channel.get_primary_genre() or "").strip().lower()
        if genre:
            item_genres = {g.get_name().lower() for g in item.get_genres()}
            if genre in item_genres:
                score += 3.0

        audience = (channel.get_target_audience() or "").strip().lower().replace(" ", "_")
        if audience and item.get_audience() is not None:
            item_aud = getattr(item.get_audience(), "name", "").lower()
            if audience == item_aud:
                score += 2.0

        # Tag overlap as a softer signal (channel tags via network_branding
        # keywords are out of scope; use item tags against the genre word).
        for tag in item.get_tags():
            if genre and genre in tag.get_name().lower():
                score += 0.5

        return score
