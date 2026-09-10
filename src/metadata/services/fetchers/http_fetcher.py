"""
VISTOR HTTP Fetcher

reference format: a direct URL to the media file.
Catch-all so ANY website with a direct link is downloadable.
"""

from metadata.services.fetchers.base_fetcher import BaseFetcher


class HttpFetcher(BaseFetcher):

    def _download(self, reference, temp_path):
        import requests  # optional dep, imported lazily

        with requests.get(reference, stream=True, timeout=30) as resp:
            if resp.status_code != 200:
                return resp.status_code

            with open(temp_path, "wb") as handle:
                for chunk in resp.iter_content(chunk_size=1 << 16):
                    if chunk:
                        handle.write(chunk)

        return 200
