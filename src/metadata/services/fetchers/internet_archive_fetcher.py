"""  
VISTOR Internet Archive Fetcher  
  
reference format: "<identifier>/<filename>"  
    e.g. "entiretyofeva/endofevaalldub.mkv"  
  
Builds https://archive.org/download/<identifier>/<filename> and streams  
it to disk. Most-reliable provider, so it is ranked first.  
"""  
  
from metadata.services.fetchers.base_fetcher import BaseFetcher  
  
  
class InternetArchiveFetcher(BaseFetcher):  
  
    BASE = "https://archive.org/download"  
  
    def _download(self, reference, temp_path):  
        import requests  # optional dep, imported lazily  
  
        url = f"{self.BASE}/{reference.lstrip('/')}"  
  
        with requests.get(url, stream=True, timeout=30) as resp:  
            if resp.status_code != 200:  
                return resp.status_code  
  
            with open(temp_path, "wb") as handle:  
                for chunk in resp.iter_content(chunk_size=1 << 16):  
                    if chunk:  
                        handle.write(chunk)  
  
        return 200