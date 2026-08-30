"""  
VISTOR Renderer  
  
Real audio/video output layer that sits BEHIND the headless Player.  
  
The Player remains the authoritative transport state machine; the renderer  
only mirrors its decisions onto an actual media surface. A NullRenderer  
keeps everything headless (tests, CI, unwatched channels), while MpvRenderer  
drives libmpv for real playback + on-screen OSD text.  
"""  
  
from __future__ import annotations  
  
from core.logger import Logger  
  
  
class Renderer:  
    """Interface every playback backend implements."""  
  
    def load(self, path):  
        """Open a media file at `path` (paused/ready)."""  
  
    def play(self):  
        """Begin/resume output."""  
  
    def pause(self):  
        """Pause output, preserving position."""  
  
    def stop(self):  
        """Stop output and release the current file."""  
  
    def set_volume(self, level):  
        """Set output volume (0-100)."""  
  
    def set_mute(self, flag):  
        """Set output mute state."""  
  
    def render_osd(self, osd_manager):  
        """Draw the current OSD overlay (banner/volume/clock/...) on screen."""  
  
    def shutdown(self):  
        """Tear down the backend."""  
  
  
class NullRenderer(Renderer):  
    """Headless no-op backend. Every VISTOR test path uses this."""  
  
    def load(self, path):  
        Logger.info(f"NullRenderer: load '{path}' (no output).")  
  
    def play(self):  
        Logger.info("NullRenderer: play (no output).")  
  
    def pause(self):  
        Logger.info("NullRenderer: pause (no output).")  
  
    def stop(self):  
        Logger.info("NullRenderer: stop (no output).")  
  
    def set_volume(self, level):  
        Logger.info(f"NullRenderer: volume {level} (no output).")  
  
    def set_mute(self, flag):  
        Logger.info("NullRenderer: " + ("mute" if flag else "unmute") + " (no output).")  
  
    def render_osd(self, osd_manager):  
        pass  
  
    def shutdown(self):  
        pass  
  
  
class MpvRenderer(Renderer):  
    """libmpv-backed video/audio output with on-screen OSD text.  
  
    python-mpv is imported lazily so importing this module never fails on a  
    headless box. Use create_renderer() to get an MpvRenderer with an  
    automatic NullRenderer fallback.  
    """  
  
    def __init__(self, fullscreen=True):  
        import mpv  # lazy: only required when a real surface is wanted  
  
        self._mpv = mpv.MPV(  
            fullscreen=fullscreen,  
            input_default_bindings=False,  
            osc=False,  
            keep_open="yes",   # don't close the window when a file ends  
        )  
        self._loaded_path = None  
        Logger.info("MpvRenderer: libmpv surface created.")  
  
    def load(self, path):  
        self._loaded_path = str(path)  
        # loadfile then immediately pause so Player.play() controls start.  
        self._mpv.play(self._loaded_path)  
        self._mpv.pause = True  
        Logger.info(f"MpvRenderer: loaded '{self._loaded_path}'.")  
  
    def play(self):  
        self._mpv.pause = False  
  
    def pause(self):  
        self._mpv.pause = True  
  
    def stop(self):  
        self._mpv.command("stop")  
        self._loaded_path = None  
  
    def set_volume(self, level):  
        self._mpv.volume = max(0, min(100, int(level)))  
  
    def set_mute(self, flag):  
        self._mpv.mute = bool(flag)  
  
    def render_osd(self, osd_manager):  
        """Mirror the OSDManager's current overlay onto the mpv OSD layer."""  
        if osd_manager is None or not osd_manager.is_visible():  
            return  
  
        payload = osd_manager.get_payload() or {}  
        text = self._format_overlay(osd_manager.get_overlay(), payload)  
  
        if text:  
            # visible_duration is in seconds; mpv wants milliseconds. The  
            # OSDManager already governs auto-hide, so a short re-show per  
            # tick keeps it painted while it is meant to be up.  
            self._mpv.command("show-text", text, "1000")  
  
    @staticmethod  
    def _format_overlay(self, overlay, payload):  
        """Map an OSD overlay + payload to one on-screen text line.  
  
        Keys mirror what OSDManager puts in each payload  
        (src/osd/osd_manager.py):  
          channel_banner -> number, name, program  
          program_info   -> title, channel_name  
          volume         -> level, muted  
          mute           -> muted  
          clock          -> time  
        """  
  
        kind = getattr(overlay, "value", overlay)  
        payload = payload or {}  
  
        if kind == "channel_banner":  
            line = f"{payload.get('number', '')}  {payload.get('name', '')}".strip()  
            program = payload.get("program")  
            return f"{line}\n{program}" if program else line  
  
        if kind == "program_info":  
            title = payload.get("title") or "No Program"  
            return f"{title}\n{payload.get('channel_name', '')}".strip()  
  
        if kind == "volume":  
            return "Muted" if payload.get("muted") else f"Volume {payload.get('level', 0)}"  
  
        if kind == "mute":  
            return "Muted" if payload.get("muted") else "Unmuted" 

        if kind == "settings":  
            rows = payload.get("rows", [])  
            lines = ["SETTINGS"]  
            for row in rows:  
                marker = ">" if row.get("selected") else " "  
                lines.append(f"{marker} {row.get('label')}: {row.get('value')}")  
            return "\n".join(lines)  
  
        if kind == "clock":  
            return str(payload.get("time", ""))  
  
        return ""
  
    def shutdown(self):  
        try:  
            self._mpv.terminate()  
        except Exception:  
            pass  
  
  
def create_renderer(fullscreen=True):  
    """Return an MpvRenderer if libmpv is available, else a NullRenderer.  
  
    This keeps headless environments (tests, CI, boxes with no display or no  
    python-mpv installed) working without any config.  
    """  
    try:  
        return MpvRenderer(fullscreen=fullscreen)  
    except Exception as error:  # ImportError, no display, no libmpv, ...  
        Logger.warning(  
            f"create_renderer: falling back to NullRenderer ({error})."  
        )  
        return NullRenderer()