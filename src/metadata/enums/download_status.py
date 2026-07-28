"""  
VISTOR Download Status  
  
Runtime availability state of a physical MediaAsset. This is deliberately  
separate from metadata: a media item always exists in the library, but its  
asset's file may or may not currently be present on disk.  
"""  
  
from enum import Enum, auto  
  
  
class DownloadStatus(Enum):  
    """Availability state of a single media asset's file."""  
  
    # No local file and none requested yet.  
    NOT_DOWNLOADED = auto()  
  
    # Selected for acquisition; not yet fetched.  
    QUEUED = auto()  
  
    # Fetch in progress.  
    DOWNLOADING = auto()  
  
    # File is present locally.  
    DOWNLOADED = auto()  
  
    # File was present but has since gone missing from disk.  
    MISSING = auto()  
  
    # A fetch was attempted and failed (e.g. source 404/403).  
    FAILED = auto()