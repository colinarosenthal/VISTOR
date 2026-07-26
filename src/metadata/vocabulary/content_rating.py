"""  
VISTOR Content Rating  
  
Defines official content rating classifications.  
"""  
  
  
class ContentRating:  
    """  
    Represents an official media content rating.  
  
    Ratings are described rather than fixed, because different  
    countries and organizations use different classification  
    standards. Each rating preserves the system and country of  
    the authority that issued it rather than being converted into  
    a single universal value.  
    """  
  
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
        """Return the rating system."""  
  
        return self.system  
  
    def get_country(self):  
        """Return the issuing country."""  
  
        return self.country  
  
    def get_min_age(self):  
        """Return the minimum recommended age."""  
  
        return self.min_age  
  
    def get_description(self):  
        """Return the rating description."""  
  
        return self.description  
  
    # ------------------------------------------------------------------  
    # Modification  
    # ------------------------------------------------------------------  
  
    def set_description(self, description: str):  
        """Set the rating description."""  
  
        self.description = description  
  
    def set_min_age(self, min_age: int):  
        """Set the minimum recommended age."""  
  
        self.min_age = min_age  
  
    # ------------------------------------------------------------------  
    # Utility  
    # ------------------------------------------------------------------  
  
    def __str__(self):  
        return self.name