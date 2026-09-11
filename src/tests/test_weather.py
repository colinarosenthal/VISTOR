"""  
VISTOR Weather Subsystem Tests  
  
Offline-safe. Verifies the WeatherService respects Config.is_weather_enabled(),  
returns placeholder data via NullWeatherProvider, and mints a generated  
WeatherSegment. Run standalone: python src/tests/test_weather.py  
"""  
  
import sys  
from pathlib import Path  
  
sys.path.append(str(Path(__file__).resolve().parent.parent))  
  
from core.config import Config  
from weather.weather_service import WeatherService  
from weather.weather_provider import NullWeatherProvider  
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
  
print("Weather service verified.")  
print("\nWeather tests passed.")