"""
VISTOR Provider Registry

Maps a source's `provider` string to a concrete fetcher. Unknown providers
fall back to the HTTP fetcher (treats `reference` as a direct URL).
"""

from metadata.services.fetchers.internet_archive_fetcher import InternetArchiveFetcher
from metadata.services.fetchers.youtube_fetcher import YouTubeFetcher
from metadata.services.fetchers.http_fetcher import HttpFetcher


class ProviderRegistry:

    def __init__(self, media_root="Media"):
        ia = InternetArchiveFetcher(media_root=media_root)
        yt = YouTubeFetcher(media_root=media_root)
        http = HttpFetcher(media_root=media_root)

        self._fetchers = {
            "internet_archive": ia,
            "youtube": yt,
            "http": http,
            "direct_url": http,
        }
        self._default = http

    def get(self, provider):
        """Return the fetcher for `provider`, or the HTTP fallback."""

        return self._fetchers.get(provider, self._default)

    def register(self, provider, fetcher):
        """Add or override a provider fetcher."""

        self._fetchers[provider] = fetcher
