"""  
VISTOR Content Rating  
  
Defines official content rating classifications used throughout VISTOR.  
  
A content rating is a controlled vocabulary value describing an official  
classification (e.g. "PG-13", "BBFC 15"). Because different countries and  
versions of the same media may carry different ratings, a rating value is  
assigned to media per-region rather than being a permanent property of the  
media itself.  
"""  
  
  
class ContentRating:  
    """Represents an official media content rating classification."""  
  
    # ------------------------------------------------------------------  
    # Construction  
    # ------------------------------------------------------------------  
  
    def __init__(  
        self,  
        name: str,  
        system: str = "",  
        country: str = "",  
        min_age: int = 0,  
        description: str = "",  
    ):  
        self.name = name  
  
        self.system = system  
  
        self.country = country  
  
        self.min_age = min_age  
  
        self.description = description  
  
    # ------------------------------------------------------------------  
    # Basic Information  
    # ------------------------------------------------------------------  
  
    def get_name(self):  
        """Return the rating name."""  
  
        return self.name  
  
    def get_system(self):  
        """Return the rating system (e.g. MPAA, BBFC)."""  
  
        return self.system  
  
    def get_country(self):  
        """Return the country or region that issues this rating."""  
  
        return self.country  
  
    def get_min_age(self):  
        """Return the approximate minimum recommended age."""  
  
        return self.min_age  
  
    def get_description(self):  
        """Return the rating description."""  
  
        return self.description  
  
    # ------------------------------------------------------------------  
    # Utility  
    # ------------------------------------------------------------------  
  
    def __str__(self):  
        return self.name