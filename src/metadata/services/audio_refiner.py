"""
VISTOR Audio Refiner (download-stage, definitive music match)

After a MusicVideo file is downloaded, we can do better than a title-based
MusicBrainz search: we fingerprint the actual AUDIO with Chromaprint and ask
AcoustID which MusicBrainz recording it is. AcoustID returns MusicBrainz
recording MBIDs, so a positive match is handed straight to MusicBrainzSource
to fill the definitive first-release year and controlled MusicGenre.

Everything here is optional and offline-safe:
  * `acoustid` (pyacoustid) + the Chromaprint `fpcalc` binary are imported
    lazily; if either is missing, refine() is a no-op and returns the record
    unchanged.
  * The AcoustID web service needs a free application API key in the
    ACOUSTID_API_KEY environment variable; without it we no-op.

So the headless smoke test never touches the network or a decoder.
"""

import os

from core.logger import Logger


# AcoustID only trusts a match above this fingerprint score (0.0 - 1.0).
_MIN_SCORE = 0.5


class AudioRefiner:
    """Refine a MusicVideo record from its downloaded audio via AcoustID."""

    def __init__(self, mb_source=None, api_key=None):
        # Lazy import so a missing package doesn't break unrelated imports.
        if mb_source is None:
            try:
                from metadata.services.enrichment.musicbrainz_source import (
                    MusicBrainzSource,
                )
                mb_source = MusicBrainzSource()
            except Exception:  # noqa: BLE001
                mb_source = None
        self.mb_source = mb_source
        self.api_key = api_key or os.environ.get("ACOUSTID_API_KEY", "")

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def refine(self, record, audio_path):
        """
        Return `record` with release_year / music_genre corrected from a
        definitive AcoustID audio match, or unchanged if we can't match.

        Only runs for MusicVideo records; anything else passes through.
        """

        if not record or record.get("type") != "MusicVideo":
            return record

        mbid, score = self._lookup_mbid(audio_path)
        if not mbid:
            return record

        Logger.info(
            f"AcoustID matched '{record.get('title', '?')}' -> "
            f"recording {mbid} (score={score:.2f})."
        )

        result = self._lookup_recording(mbid)
        if not result:
            return record

        # Definitive audio match OUTRANKS the title-search guess: overwrite
        # the two fields the audio can speak to authoritatively.
        year = result.get("release_year") or 0
        if year:
            record["release_year"] = year
        genre = result.get("music_genre") or ""
        if genre:
            record["music_genre"] = genre

        Logger.success(
            f"AcoustID refined '{record.get('title', '?')}' -> "
            f"{record.get('release_year', '?')} "
            f"(genre={record.get('music_genre') or '?'})."
        )
        return record

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _lookup_mbid(self, audio_path):
        """Chromaprint-fingerprint the file and ask AcoustID for its MBID."""

        if not self.api_key:
            Logger.info("ACOUSTID_API_KEY not set; skipping audio refine.")
            return (None, 0.0)

        try:
            import acoustid  # lazy: pyacoustid + fpcalc; keeps test offline
        except ImportError:
            Logger.info("acoustid/Chromaprint not installed; skipping refine.")
            return (None, 0.0)

        try:
            # match() yields (score, recording_id, title, artist) tuples,
            # already ordered best-first. fpcalc must be on PATH.
            best = None
            for score, rec_id, _title, _artist in acoustid.match(
                self.api_key, str(audio_path)
            ):
                if rec_id and score >= _MIN_SCORE:
                    best = (rec_id, float(score))
                    break
            return best or (None, 0.0)
        except acoustid.NoBackendError:
            Logger.warning("Chromaprint fpcalc not found; skipping refine.")
            return (None, 0.0)
        except acoustid.FingerprintGenerationError:
            Logger.warning(f"Could not fingerprint audio '{audio_path}'.")
            return (None, 0.0)
        except Exception as exc:  # noqa: BLE001 - never fail a download
            Logger.warning(f"AcoustID lookup failed: {exc!r}.")
            return (None, 0.0)

    def _lookup_recording(self, mbid):
        """Turn an AcoustID recording MBID into year + controlled genre."""

        if self.mb_source is None:
            return None
        try:
            return self.mb_source.lookup_by_mbid(mbid)
        except Exception as exc:  # noqa: BLE001
            Logger.warning(f"MusicBrainz MBID lookup failed: {exc!r}.")
            return None
