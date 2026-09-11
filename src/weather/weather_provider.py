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
  
  
class LiveWeatherProvider(WeatherProvider):  
    """Network-backed provider using wttr.in (keyless, no API key/account).  
  
    Offline-safe: `requests` is imported lazily and every failure (no  
    network, bad status, parse error) degrades to None / [] so the  
    WeatherService falls back gracefully. Mirrors the renderer/fetcher  
    lazy-import + guarded-failure pattern.  
    """  
  
    BASE_URL = "https://wttr.in/{location}?format=j1"  
    TIMEOUT_SECONDS = 6  
  
    def _fetch(self, location):  
        """Fetch the raw wttr.in JSON payload, or None on any failure."""  
  
        try:  
            import requests  
        except ImportError:  
            return None  
  
        try:  
            response = requests.get(  
                self.BASE_URL.format(location=location or "Local"),  
                timeout=self.TIMEOUT_SECONDS,  
                headers={"User-Agent": "VISTOR/1.0"},  
            )  
            response.raise_for_status()  
            return response.json()  
        except Exception:  # noqa: BLE001  
            return None  
  
    def get_current(self, location):  
        data = self._fetch(location)  
  
        if not data:  
            return None  
  
        try:  
            current = data["current_condition"][0]  
            return CurrentConditions(  
                location=location,  
                temperature_f=int(current["temp_F"]),  
                condition=current["weatherDesc"][0]["value"],  
                humidity_pct=int(current["humidity"]),  
                wind_mph=int(current["windspeedMiles"]),  
            )  
        except (KeyError, IndexError, ValueError, TypeError):  
            return None  
  
    def get_forecast(self, location, days=5):  
        data = self._fetch(location)  
  
        if not data:  
            return []  
  
        forecast = []  
  
        try:  
            for day in data.get("weather", [])[:days]:  
                hourly = day.get("hourly", [])  
                midday = hourly[4] if len(hourly) > 4 else (hourly[0] if hourly else {})  
                forecast.append(  
                    ForecastDay(  
                        label=day.get("date", ""),  
                        high_f=int(day["maxtempF"]),  
                        low_f=int(day["mintempF"]),  
                        condition=midday.get("weatherDesc", [{}])[0].get("value", ""),  
                    )  
                )  
        except (KeyError, IndexError, ValueError, TypeError):  
            return []  
  
        return forecast  

def create_weather_provider(config=None):  
    """Return the best available provider, falling back to NullWeatherProvider.  
  
    Mirrors create_renderer(): returns a live network-backed provider when  
    `requests` is importable, otherwise the offline null default. The live  
    provider itself is offline-safe (guarded fetch), so this never raises.  
    """  
  
    try:  
        import requests  # noqa: F401  
    except ImportError:  
        Logger.info("Weather: requests unavailable; using NullWeatherProvider.")  
        return NullWeatherProvider()  
  
    Logger.info("Weather: using LiveWeatherProvider (wttr.in).")  
    return LiveWeatherProvider()