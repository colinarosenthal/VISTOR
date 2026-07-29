"""  
VISTOR Authoritative Source  
  
Abstract contract for an external metadata catalog. Backends return a  
normalized dict (or None) so MetadataEnricher never depends on a specific  
provider's JSON shape.  
  
Normalized result shape (all keys optional except title):  
    {  
        "title": str,  
        "release_year": int,  
        "runtime_minutes": int,  
        "description": str,  
        "media_type": str,          # a MediaType-compatible name, e.g. "Movie"  
        "genres": [str, ...],       # VISTOR controlled Genre names ONLY  
    }  
"""  
  
  
class AuthoritativeSource:  
    """Base class for a pluggable authoritative metadata lookup."""  
  
    def lookup(self, title, year=None, media_type=None):  
        """Return a normalized metadata dict, or None if no confident match."""  
  
        raise NotImplementedError