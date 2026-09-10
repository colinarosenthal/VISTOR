"""
VISTOR Breakpoint Detector

Derives commercial-break offsets (seconds) from a downloaded media file using
the ffmpeg/ffprobe toolchain already required by MetadataProbe. No new
dependency and no network. Two authentic signals plus a runtime safety net:

  Tier 1  Container chapters   (ffprobe -show_chapters)
  Tier 2  Black + silence      (ffmpeg blackdetect + silencedetect intersect)
  Tier 3  Runtime spacing      (Design Bible fallback; even ~10-min gaps)

Everything is best-effort: a missing binary or a parse failure degrades to []
so a download never fails on breakpoint detection.
"""

import json
import re
import shutil
import subprocess
from pathlib import Path

from core.logger import Logger


class BreakpointDetector:
    """Detect commercial-break offsets from a file on disk."""

    # blackdetect: min black duration / pixel + picture thresholds.
    BLACK_FILTER = "blackdetect=d=0.10:pic_th=0.98:pix_th=0.10"
    # silencedetect: below -30 dB for at least 0.3s counts as a dip.
    SILENCE_FILTER = "silencedetect=noise=-30dB:d=0.3"

    # A black interval and a silence interval are treated as the same break
    # when their midpoints fall within this many seconds of each other.
    PROXIMITY_SECONDS = 2.0

    # Tier 3 fallback: aim for a break roughly every this many seconds.
    FALLBACK_SPACING_SECONDS = 600  # ~10 minutes

    def detect(self, asset, path):
        """Return a sorted list of break offsets (seconds) for `asset`."""

        path = Path(path)

        breaks = self._chapters(path)
        if breaks:
            Logger.info(
                f"Breakpoints (chapters) for '{asset.get_asset_id()}': {breaks}."
            )
            return breaks

        breaks = self._black_and_silence(path)
        if breaks:
            Logger.info(
                f"Breakpoints (black+silence) for "
                f"'{asset.get_asset_id()}': {breaks}."
            )
            return breaks

        breaks = self._runtime_fallback(asset)
        Logger.info(
            f"Breakpoints (runtime fallback) for "
            f"'{asset.get_asset_id()}': {breaks}."
        )
        return breaks

    # ------------------------------------------------------------------
    # Tier 1 - container chapters
    # ------------------------------------------------------------------

    def _chapters(self, path):
        if shutil.which("ffprobe") is None:
            return []

        try:
            out = subprocess.run(
                [
                    "ffprobe", "-v", "quiet",
                    "-print_format", "json",
                    "-show_chapters",
                    str(path),
                ],
                capture_output=True, text=True, check=True,
            )
            data = json.loads(out.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError, OSError):
            return []

        starts = []
        for chapter in data.get("chapters", []):
            try:
                start = float(chapter.get("start_time", 0.0))
            except (TypeError, ValueError):
                continue
            # Ignore a chapter that starts at 0 (that's the program start,
            # not a break).
            if start > 1.0:
                starts.append(round(start, 2))

        return sorted(set(starts))

    # ------------------------------------------------------------------
    # Tier 2 - black frame + silence intersection
    # ------------------------------------------------------------------

    def _black_and_silence(self, path):
        if shutil.which("ffmpeg") is None:
            return []

        try:
            proc = subprocess.run(
                [
                    "ffmpeg", "-hide_banner", "-nostats",
                    "-i", str(path),
                    "-vf", self.BLACK_FILTER,
                    "-af", self.SILENCE_FILTER,
                    "-f", "null", "-",
                ],
                capture_output=True, text=True,
            )
        except OSError:
            return []

        # ffmpeg writes filter output to stderr.
        log = proc.stderr or ""

        black_mids = self._black_midpoints(log)
        silence_mids = self._silence_midpoints(log)

        # Keep only black points that coincide with a silence point.
        breaks = []
        for black in black_mids:
            for silent in silence_mids:
                if abs(black - silent) <= self.PROXIMITY_SECONDS:
                    breaks.append(round(black, 2))
                    break

        return sorted(set(breaks))

    def _black_midpoints(self, log):
        mids = []
        for match in re.finditer(
            r"black_start:(?P<start>[\d.]+)\s+black_end:(?P<end>[\d.]+)", log
        ):
            start = float(match.group("start"))
            end = float(match.group("end"))
            mids.append((start + end) / 2.0)
        return mids

    def _silence_midpoints(self, log):
        starts = [float(m.group(1))
                  for m in re.finditer(r"silence_start:\s*([\d.]+)", log)]
        ends = [float(m.group(1))
                for m in re.finditer(r"silence_end:\s*([\d.]+)", log)]
        mids = []
        for start, end in zip(starts, ends):
            mids.append((start + end) / 2.0)
        return mids

    # ------------------------------------------------------------------
    # Tier 3 - runtime spacing fallback
    # ------------------------------------------------------------------

    def _runtime_fallback(self, asset):
        try:
            runtime = int(asset.get_runtime_seconds() or 0)
        except (TypeError, ValueError):
            return []

        if runtime <= self.FALLBACK_SPACING_SECONDS:
            return []

        breaks = []
        offset = self.FALLBACK_SPACING_SECONDS
        while offset < runtime - 60:  # no break in the last minute
            breaks.append(offset)
            offset += self.FALLBACK_SPACING_SECONDS

        return breaks
