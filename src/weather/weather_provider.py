"""  
VISTOR Weather Provider  
  
Pluggable weather-data backend, following the same offline-safe fallback  
pattern as the renderer (create_renderer -> NullRenderer). The default  
NullWeatherProvider requires no network so the test suite stays offline;  
a real API-backed provider can be dropped in later without touching the  
WeatherService or the metadata WeatherSegment.  
"""  
  
from core.logger import Logger  
from weather.weather_data import CurrentConditions, ForecastDay  
  
  
class WeatherProvider:  
    """Base weather provider. Subclasses override fetch_* methods."""  
  
    def get_current(self, location):  
        """Return CurrentConditions for `location`, or None if unavailable."""  
        raise NotImplementedError  
  
    def get_forecast(self, location, days=5):  
        """Return a list of ForecastDay, or [] if unavailable."""  
        raise NotImplementedError  
  
  
class NullWeatherProvider(WeatherProvider):  
    """Offline provider. Returns placeholder data; performs no network I/O."""  
  
    def get_current(self, location):  
        return CurrentConditions(  
            location=location,  
            temperature_f=None,  
            condition="Unavailable",  
        )  
  
    def get_forecast(self, location, days=5):  
        return []  
  
  
def create_weather_provider(config=None):  
    """Return the best available provider, falling back to NullWeatherProvider.  
  
    Mirrors create_renderer(): a real network-backed provider can be added  
    here later (guarded by lazy import + try/except) so this function never  
    raises and the offline default always works.  
    """  
  
    Logger.info("Weather: using NullWeatherProvider (offline default).")  
    return NullWeatherProvider()