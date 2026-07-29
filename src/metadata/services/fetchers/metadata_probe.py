"""  
VISTOR Metadata Probe  
  
Extracts technical metadata from a downloaded file and writes it onto the  
MediaAsset. Uses ffprobe (if available on PATH) for full video info, and  
falls back to mutagen / stdlib for what it can. Everything is best-effort:  
a missing tool degrades gracefully instead of failing the download.  
"""  
  
import json  
import shutil  
import subprocess  
from pathlib import Path  
  
from core.logger import Logger  
  
  
class MetadataProbe:  
    """Populate a MediaAsset's technical fields from a file on disk."""  
  
    def populate(self, asset, path):  
        path = Path(path)  
  
        # Always-available basics.  
        try:  
            asset.file_size = path.stat().st_size  
        except OSError:  
            pass  
  
        # ffprobe gives the richest data if present.  
        info = self._ffprobe(path)  
  
        if info:  
            self._apply_ffprobe(asset, info)  
        else:  
            Logger.warning(  
                f"ffprobe unavailable; only file_size set for "  
                f"'{asset.get_asset_id()}'."  
            )  
  
        asset.container = path.suffix.lstrip(".").lower()  
  
        Logger.info(  
            f"Probed '{asset.get_asset_id()}': "  
            f"{asset.runtime_seconds}s "  
            f"{asset.width}x{asset.height} "  
            f"{asset.video_codec}/{asset.audio_codec}."  
        )  
  
    # ------------------------------------------------------------------  
    # Internals  
    # ------------------------------------------------------------------  
  
    def _ffprobe(self, path):  
        if shutil.which("ffprobe") is None:  
            return None  
  
        try:  
            out = subprocess.run(  
                [  
                    "ffprobe", "-v", "quiet",  
                    "-print_format", "json",  
                    "-show_format", "-show_streams",  
                    str(path),  
                ],  
                capture_output=True, text=True, check=True,  
            )  
            return json.loads(out.stdout)  
        except (subprocess.CalledProcessError, json.JSONDecodeError, OSError):  
            return None  
  
    def _apply_ffprobe(self, asset, info):  
        fmt = info.get("format", {})  
  
        try:  
            asset.runtime_seconds = int(float(fmt.get("duration", 0)))  
        except (TypeError, ValueError):  
            pass  
  
        for stream in info.get("streams", []):  
            kind = stream.get("codec_type")  
  
            if kind == "video":  
                asset.video_codec = stream.get("codec_name", "")  
                asset.width = int(stream.get("width", 0) or 0)  
                asset.height = int(stream.get("height", 0) or 0)  
                asset.frame_rate = self._parse_rate(  
                    stream.get("avg_frame_rate", "0/0")  
                )  
            elif kind == "audio":  
                asset.audio_codec = stream.get("codec_name", "")  
  
    def _parse_rate(self, rate):  
        try:  
            num, _, den = rate.partition("/")  
            den = float(den) if den else 0.0  
            return round(float(num) / den, 3) if den else 0.0  
        except (ValueError, ZeroDivisionError):  
            return 0.0