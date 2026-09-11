"""  
VISTOR Weather Subsystem Tests  
  
Offline-safe. Verifies the WeatherService respects Config.is_weather_enabled(),  
returns placeholder data via NullWeatherProvider, and mints a generated  
WeatherSegment. Also verifies LiveWeatherProvider parsing against a canned  
payload (no network). Run standalone: python src/tests/test_weather.py  
"""  
  
import sys  
from pathlib import Path  
  
sys.path.append(str(Path(__file__).resolve().parent.parent))  
  
from core.config import Config  
from weather.weather_service import WeatherService  
from weather.weather_provider import NullWeatherProvider, LiveWeatherProvider  
from metadata.media.television.weather_segment import WeatherSegment  
  
print("\n=== Testing Weather Service ===")  
  
# Enabled path.  
config = Config(path=None)  
config.weather_enabled = True  
  
service = WeatherService(config, provider=NullWeatherProvider(), location="Testville")  
assert service.is_enabled(), "Weather should be enabled."  
  
service.refresh()  
current = service.get_current()  
assert current is not None, "Enabled refresh should populate current conditions."  
assert current.get_location() == "Testville"  
  
segment = service.build_segment("weather-test-1")  
assert isinstance(segment, WeatherSegment), "Should mint a WeatherSegment."  
assert segment.is_generated(), "Generated weather segment should be flagged."  
  
# Disabled path.  
config.weather_enabled = False  
service.refresh()  
assert service.get_current() is None, "Disabled service should hold no conditions."  
assert service.build_segment("weather-test-2") is None, "Disabled build returns None."  
  
# Live provider parsing (offline: canned payload, no network).  
live = LiveWeatherProvider()  
live._fetch = lambda location: {  
    "current_condition": [{  
        "temp_F": "72",  
        "humidity": "40",  
        "windspeedMiles": "8",  
        "weatherDesc": [{"value": "Sunny"}],  
    }],  
    "weather": [{  
        "date": "2026-07-04",  
        "maxtempF": "88",  
        "mintempF": "65",  
        "hourly": [{"weatherDesc": [{"value": "Clear"}]}] * 5,  
    }],  
}  
  
live_current = live.get_current("Testville")  
assert live_current is not None and live_current.get_temperature_f() == 72  
assert live_current.get_condition() == "Sunny"  
  
live_forecast = live.get_forecast("Testville")  
assert len(live_forecast) == 1 and live_forecast[0].get_high_f() == 88  
  
# No-network path degrades to None / [] rather than raising.  
live_dead = LiveWeatherProvider()  
live_dead._fetch = lambda location: None  
assert live_dead.get_current("Testville") is None  
assert live_dead.get_forecast("Testville") == []  
  
print("Live weather provider parsing verified.")  
  
print("Weather service verified.")  
print("\nWeather tests passed.")