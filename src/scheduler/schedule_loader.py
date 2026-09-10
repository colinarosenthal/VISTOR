"""  
VISTOR Schedule Loader  
  
Builds the schedule library consumed by the Scheduler. Schedules are  
authored as JSON under the project's Schedules/ directory (metadata-only:  
each block references media by metadata id, not by file path). When no  
authored schedules exist, safe full-day defaults are built in code so the  
scheduler always has a lineup to select.  
  
Authored schedule file format (one file per schedule type):  
  
    {  
      "schedule_type": "weekday",  
      "name": "Weekday",  
      "blocks": [  
        {  
          "name": "Primetime",  
          "start_hour": 20, "start_minute": 0,  
          "end_hour": 23, "end_minute": 0,  
          "items": ["ep_some_series_s01e01", "mv_some_music_video"]  
        }  
      ]  
    }  
  
`schedule_type` must match a ScheduleType value (weekday, weekend,  
halloween, christmas_day, thanksgiving, ...). `items` are metadata ids  
resolved to concrete media later in the pipeline.  
"""  
  
import json  
  
from core.logger import Logger  
from core.paths import Paths  
  
from scheduler.schedule import Schedule  
from scheduler.programming_block import ProgrammingBlock  
from scheduler.schedule_type import ScheduleType  
from scheduler.scheduled_item import ScheduledItem  
  
  
class ScheduleLoader:  
    """Builds and loads schedules for the scheduler."""  
  
    # ------------------------------------------------------------------  
    # Lifecycle  
    # ------------------------------------------------------------------  
  
    def __init__(self, schedules_directory=None):  
        # Directory is injectable so tests can point at a temp dir without  
        # touching the real project Schedules/ tree.  
        if schedules_directory is not None:  
            self.schedules_directory = schedules_directory  
        else:  
            self.schedules_directory = Paths().get_schedules_directory()  
  
        self.schedule_library = {}  
  
        self.loaded = False  
  
    def load(self):  
        """Load all schedules (authored JSON first, then defaults)."""  
  
        Logger.info("Loading schedules...")  
  
        authored = self._load_from_directory()  
  
        if not authored:  
            Logger.info(  
                "No authored schedules found; building code defaults."  
            )  
            self._load_defaults()  
  
        self.loaded = True  
  
        Logger.info("Schedules loaded.")  
  
    def unload(self):  
        """Unload all schedules."""  
  
        self.schedule_library.clear()  
  
        self.loaded = False  
  
    def is_loaded(self):  
        """Return whether schedules have been loaded."""  
  
        return self.loaded  
  
    # ------------------------------------------------------------------  
    # Schedule Access  
    # ------------------------------------------------------------------  
  
    def get_schedule_library(self):  
        """Return the complete schedule library."""  
  
        return self.schedule_library  
  
    def get_schedule(self, schedule_type):  
        """Return a schedule by type."""  
  
        return self.schedule_library.get(schedule_type)  
  
    # ------------------------------------------------------------------  
    # Authored (JSON) Loading  
    # ------------------------------------------------------------------  
  
    def _load_from_directory(self):  
        """Load every *.json schedule under the schedules directory.  
  
        Returns True if at least one authored schedule was loaded.  
        """  
  
        directory = self.schedules_directory  
  
        if directory is None or not directory.exists():  
            return False  
  
        loaded_any = False  
  
        for path in sorted(directory.glob("*.json")):  
            try:  
                with open(path, "r", encoding="utf-8") as handle:  
                    data = json.load(handle)  
            except (OSError, ValueError) as error:  
                Logger.warning(  
                    f"Skipping schedule '{path.name}': {error}."  
                )  
                continue  
  
            schedule_type = self._resolve_schedule_type(  
                data.get("schedule_type")  
            )  
  
            if schedule_type is None:  
                Logger.warning(  
                    f"Schedule '{path.name}' has unknown schedule_type "  
                    f"'{data.get('schedule_type')}'; skipping."  
                )  
                continue  
  
            schedule = self._build_schedule(data)  
  
            self.schedule_library[schedule_type] = schedule  
            loaded_any = True  
  
            Logger.info(  
                f"Loaded authored schedule '{path.name}' "  
                f"-> {schedule_type.value}."  
            )  
  
        return loaded_any  
  
    def _build_schedule(self, data):  
        """Build a Schedule (with blocks + metadata-id items) from JSON."""  
  
        schedule = Schedule(data.get("name", "Unnamed"))  
  
        for block_data in data.get("blocks", []):  
            block = ProgrammingBlock(  
                block_data.get("name", "Programming"),  
                block_data.get("start_hour", 0),  
                block_data.get("start_minute", 0),  
                block_data.get("end_hour", 23),  
                block_data.get("end_minute", 59),  
            )  
  
            for media_id in block_data.get("items", []):  
                block.add_item(ScheduledItem(media_id))  
  
            schedule.add_block(block)  
  
        schedule.load()  
  
        return schedule  
  
    def _resolve_schedule_type(self, value):  
        """Map a schedule_type string to a ScheduleType (or None)."""  
  
        if not value:  
            return None  
  
        try:  
            return ScheduleType(value)  
        except ValueError:  
            return None  
  
    # ------------------------------------------------------------------  
    # Code Defaults (fallback when no authored schedules exist)  
    # ------------------------------------------------------------------  
  
    def _load_defaults(self):  
        """Build safe full-day placeholder schedules with no media items."""  
  
        self._load_weekday_schedule()  
        self._load_weekend_schedule()  
        self._load_holiday_schedules()  
  
    def _load_weekday_schedule(self):  
        """Create the default weekday schedule."""  
  
        schedule = Schedule("Weekday")  
  
        schedule.add_block(  
            ProgrammingBlock("Default Programming", 0, 0, 23, 59)  
        )  
  
        schedule.load()  
  
        self.schedule_library[ScheduleType.WEEKDAY] = schedule  
  
    def _load_weekend_schedule(self):  
        """Create the default weekend schedule."""  
  
        schedule = Schedule("Weekend")  
  
        schedule.add_block(  
            ProgrammingBlock("Weekend Programming", 0, 0, 23, 59)  
        )  
  
        schedule.load()  
  
        self.schedule_library[ScheduleType.WEEKEND] = schedule  
  
    def _load_holiday_schedules(self):  
        """Create default placeholder holiday schedules."""  
  
        holidays = [  
            ScheduleType.NEW_YEARS_DAY,  
            ScheduleType.VALENTINES_DAY,  
            ScheduleType.ST_PATRICKS_DAY,  
            ScheduleType.INDEPENDENCE_DAY,  
            ScheduleType.HALLOWEEN,  
            ScheduleType.THANKSGIVING,  
            ScheduleType.CHRISTMAS_EVE,  
            ScheduleType.CHRISTMAS_DAY,  
            ScheduleType.NEW_YEARS_EVE,  
        ]  
  
        for holiday in holidays:  
            schedule = Schedule(holiday.name.title().replace("_", " "))  
  
            schedule.add_block(  
                ProgrammingBlock("Holiday Programming", 0, 0, 23, 59)  
            )  
  
            schedule.load()  
  
            self.schedule_library[holiday] = schedule