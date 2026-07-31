"""  
VISTOR Composite Enrichment Source  
  
Routes lookups by media_type: sports types go to TheSportsDB, everything  
else stays on TMDB. Optional methods used elsewhere (search_candidates,  
lookup_by_id, lookup_tv_chain, recommend) transparently delegate to TMDB.  
"""  
  
from metadata.services.enrichment.tmdb_source import TMDBSource  
from metadata.services.enrichment.sports_source import SportsSource, SPORTS_TYPES  
  
  
class CompositeSource:  
    def __init__(self, tmdb=None, sports=None):  
        self.tmdb = tmdb or TMDBSource()  
        self.sports = sports or SportsSource()  
  
    def lookup(self, title, year=None, media_type=None):  
        if media_type in SPORTS_TYPES:  
            return self.sports.lookup(title, year=year, media_type=media_type)  
        return self.tmdb.lookup(title, year=year, media_type=media_type)  
  
    # Delegate candidate picker / chain / recommend calls to TMDB unchanged.  
    def __getattr__(self, name):  
        return getattr(self.tmdb, name)