"""  
VISTOR Scheduled Item  
  
A ScheduledItem is a schedule-authoring reference to a piece of programming  
by its stable metadata id (MediaItem.get_id()). Schedules are authored  
metadata-only: they declare *what* airs and *when* without depending on a  
downloaded file or a loaded MetadataLibrary. The media id is resolved to a  
concrete MediaItem / MediaAsset later in the pipeline (content-population  
stage / Phase 8).  
"""  
  
  
class ScheduledItem:  
    """A metadata-id reference to programming placed in a ProgrammingBlock."""  
  
    def __init__(self, media_id, resolved=None):  
        self.media_id = media_id  
        self.resolved = resolved  
  
    def get_media_id(self):  
        return self.media_id  
  
    def get_resolved(self):  
        """Return the resolved MediaItem once content population links it."""  
        return self.resolved  
  
    def set_resolved(self, item):  
        self.resolved = item  
  
    def is_resolved(self):  
        return self.resolved is not None  
  
    def __str__(self):  
        return f"[ScheduledItem {self.media_id}]"