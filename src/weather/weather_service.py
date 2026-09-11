"""  
VISTOR Weather Service  
  
Headless weather subsystem. Like the Guide and Settings menu, it models  
state rather than rendering pixels: it holds the latest CurrentConditions  
and forecast for a configured location, and can mint a WeatherSegment  
metadata object for weather-themed channels/segments. Gated entirely by  
Config.is_weather_enabled(); when disabled it is inert.  
"""  
  
from core.logger import Logger  
from weather.weather_provider import create_weather_provider  
from metadata.media.television.weather_segment import WeatherSegment  
  
  
class WeatherService:  
    """Headless weather data holder + WeatherSegment factory."""  
  
    def __init__(self, config, provider=None, location="Local"):  
        self.config = config  
        self.provider = provider or create_weather_provider(config)  
        self.location = location  
  
        self.current = None  
        self.forecast = []  
  
    def is_enabled(self):  
        """Return whether weather features are turned on in Config."""  
        return bool(self.config and self.config.is_weather_enabled())  
  
    def refresh(self):  
        """Pull the latest conditions/forecast. No-op when disabled."""  
  
        if not self.is_enabled():  
            self.current = None  
            self.forecast = []  
            return  
  
        self.current = self.provider.get_current(self.location)  
        self.forecast = self.provider.get_forecast(self.location)  
  
        Logger.info(f"Weather refreshed for '{self.location}'.")  
  
    def get_current(self):  
        return self.current  
  
    def get_forecast(self):  
        return self.forecast  
  
    def get_location(self):  
        return self.location  
  
    def build_segment(self, segment_id, runtime_minutes=2):  
        """Mint a generated WeatherSegment from the latest conditions.  
  
        Returns None when weather is disabled or no conditions are loaded,  
        so callers can skip weather programming gracefully.  
        """  
  
        if not self.is_enabled() or self.current is None:  
            return None  
  
        description = str(self.current)  
  
        return WeatherSegment(  
            id=segment_id,  
            title=f"Local Weather - {self.location}",  
            location=self.location,  
            runtime_minutes=runtime_minutes,  
            description=description,  
            generated=True,  
        )