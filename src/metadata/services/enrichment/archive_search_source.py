"""
VISTOR Archive Search Source

Source URL Discovery backend for the autonomous catalogue expansion loop.
Given a suggested title (from RecommendationSource), searches the Internet
Archive's advanced-search API for a matching item and returns a playable
`/details/` URL that LinkResolver / RecordBuilder can consume.

Best-effort and offline-safe: with no network (or on any failure / no
match) find_source_url() returns None, so the DiscoveryLoop's assisted and
automatic modes stay inert exactly as before.
"""

from core.logger import Logger

_ADVANCED_SEARCH = "https://archive.org/advancedsearch.php"
_DETAILS_BASE = "https://archive.org/details"


class ArchiveSearchSource:
    """Finds a candidate Internet Archive URL for a suggested title."""

    def __init__(self, timeout=10):
        self.timeout = timeout

    def find_source_url(self, title, year=None, media_type="Movie"):
        """Return an archive.org /details/ URL for `title`, or None.

        Queries the Internet Archive advanced-search API for the most
        relevant item whose mediatype matches the requested media type.
        Returns None offline / on any failure / when nothing matches.
        """

        if not title:
            return None

        import requests  # lazy: keeps the offline smoke test network-free

        query = self._build_query(title, year, media_type)

        try:
            resp = requests.get(
                _ADVANCED_SEARCH,
                params={
                    "q": query,
                    "fl[]": "identifier",
                    "rows": 1,
                    "page": 1,
                    "output": "json",
                },
                timeout=self.timeout,
            )
            resp.raise_for_status()
            docs = (
                (resp.json() or {})
                .get("response", {})
                .get("docs", [])
            )
        except Exception as exc:  # noqa: BLE001 - discovery is best-effort
            Logger.warning(f"Archive search for '{title}' failed: {exc!r}.")
            return None

        if not docs:
            Logger.info(f"Archive search for '{title}': no match.")
            return None

        identifier = docs[0].get("identifier")

        if not identifier:
            return None

        url = f"{_DETAILS_BASE}/{identifier}"
        Logger.info(f"Archive search for '{title}' -> {url}.")
        return url

    def _build_query(self, title, year, media_type):
        """Compose an advanced-search query string for the title."""

        mediatype = (
            "audio"
            if media_type in ("MusicVideo", "Song", "Music")
            else "movies"
        )

        clauses = [f'title:("{title}")', f"mediatype:({mediatype})"]

        if year:
            clauses.append(f"year:({year})")

        return " AND ".join(clauses)
