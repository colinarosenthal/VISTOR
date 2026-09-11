"""  
VISTOR Weather Data  
  
Plain value objects the Weather subsystem hands to a future renderer and to  
WeatherSegment generation. No network, no rendering -- just structured data.  
"""  
  
  
class CurrentConditions:  
    """A snapshot of current weather for a location."""  
  
    def __init__(self, location="", temperature_f=None, condition="",  
                 humidity_pct=None, wind_mph=None):  
        self.location = location  
        self.temperature_f = temperature_f  
        self.condition = condition  
        self.humidity_pct = humidity_pct  
        self.wind_mph = wind_mph  
  
    def get_location(self):  
        return self.location  
  
    def get_temperature_f(self):  
        return self.temperature_f  
  
    def get_condition(self):  
        return self.condition  
  
    def get_humidity_pct(self):  
        return self.humidity_pct  
  
    def get_wind_mph(self):  
        return self.wind_mph  
  
    def __str__(self):  
        temp = f"{self.temperature_f}F" if self.temperature_f is not None else "--"  
        return f"{self.location}: {temp} {self.condition}".strip()  
  
  
class ForecastDay:  
    """A single day in a forecast."""  
  
    def __init__(self, label="", high_f=None, low_f=None, condition=""):  
        self.label = label  
        self.high_f = high_f  
        self.low_f = low_f  
        self.condition = condition  
  
    def get_label(self):  
        return self.label  
  
    def get_high_f(self):  
        return self.high_f  
  
    def get_low_f(self):  
        return self.low_f  
  
    def get_condition(self):  
        return self.condition  
  
    def __str__(self):  
        return f"{self.label}: {self.high_f}/{self.low_f} {self.condition}".strip()