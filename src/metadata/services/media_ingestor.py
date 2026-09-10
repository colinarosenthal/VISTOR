"""
VISTOR Media Ingestor

Single entry point for adding media to VISTOR from JSON.

A drop-in JSON file describes one or more media items (each optionally
carrying an `assets` array with ranked `sources`). The ingestor:

    1. Reads and validates the drop-in records.
    2. Upserts any TMDB credit payload (`cast`/`crew`/`studios`) into
       <metadata>/people.json + studios.json (dedupe by id) and rewrites it
       as a normalized `appearances` array plus a `studios` id-list on each
       record.
    3. Merges the records into <metadata>/media.json (dedupe by id, but
       records whose asset still needs downloading are RETRIED, not skipped).
    4. Reloads the library via MetadataLoader so every record becomes a
       fully-wired MediaItem + MediaAsset (JSON -> object).
    5. Auto-resolves any asset that still needs downloading using the
       production RealFetcher + SourceResolver, so adding media also
       downloads, probes, and fingerprints it.
    6. Writes the resolved library back to media.json (re-attaching the
       `appearances` and `studios` arrays the serializer does not emit) so
       the persisted record carries post-download download_status +
       fingerprint + technical metadata AND its credits.

This is the seam a future UI targets: the GUI hands a record dict here.
"""

import json

from pathlib import Path

from core.logger import Logger

from metadata.services.metadata_loader import MetadataLoader
from metadata.services.metadata_serializer import MetadataSerializer
from metadata.services.source_resolver import SourceResolver
from metadata.services.fetchers.real_fetcher import RealFetcher

from metadata.services.rolling_cache import RollingCache
from metadata.media.television.episode import Episode
from metadata.services.asset_sidecar import AssetSidecar
from metadata.enums.download_status import DownloadStatus


class MediaIngestor:
    """Adds media to VISTOR from JSON drop-in records."""

    # TMDB crew "job" -> VISTOR RoleType name. Unmapped jobs are skipped
    # rather than mislabeled (RoleType has no generic "crew" member).
    _CREW_ROLE_MAP = {
        "Director": "DIRECTOR",
        "Producer": "PRODUCER",
        "Executive Producer": "EXECUTIVE_PRODUCER",
        "Writer": "WRITER",
        "Screenplay": "SCREENWRITER",
        "Original Music Composer": "COMPOSER",
        "Music": "COMPOSER",
        "Editor": "EDITOR",
        "Director of Photography": "CINEMATOGRAPHER",
    }

    def __init__(self, metadata_path="Metadata/data"):
        self.metadata_path = Path(metadata_path)
        self.media_json = self.metadata_path / "media.json"

    # ------------------------------------------------------------------
    # Public Interface
    # ------------------------------------------------------------------

    def ingest_file(self, path, download=True, fetcher=None):
        """Ingest one drop-in JSON file (a single record or a list)."""

        records = self._read_records(path)

        if not records:
            Logger.warning(f"No ingestable records found in {path}.")

        return self.ingest_records(records, download=download, fetcher=fetcher)

    def ingest_records(self, records, download=True, fetcher=None, overwrite=False):
        """Merge `records` into media.json, then optionally resolve assets.

        overwrite=True replaces an existing record of the same id with the
        incoming one (and re-resolves its asset) instead of skipping it.
        """

        report = {
            "added": [],
            "retried": [],
            "skipped": [],
            "resolved": [],
            "unresolved": [],
        }

        # Persist any credit payload into people.json/studios.json and
        # rewrite `cast`/`crew`/`studios` as a normalized `appearances`
        # array plus a `studios` id-list BEFORE merging, so the credits
        # land in media.json too.
        self._upsert_episode_chain(records)
        self._upsert_credits(records)

        existing = self._read_media_json()
        existing_by_id = {r.get("id"): r for r in existing if r.get("id")}

        for record in records:
            media_id = record.get("id")

            if not media_id:
                report["skipped"].append((None, "record has no id"))
                Logger.warning("Skipping record with no id.")
                continue

            prior = existing_by_id.get(media_id)

            if prior is None:
                # Brand-new record: append it.
                existing.append(record)
                existing_by_id[media_id] = record
                report["added"].append(media_id)
                Logger.success(f"Ingested media record '{media_id}'.")
            elif overwrite:
                # Force-replace the existing record with the incoming one and
                # re-resolve its asset. Because the new record carries no
                # download_status: DOWNLOADED, putting its id in `added` makes
                # _resolve_new_assets re-download and re-fingerprint it.
                existing[existing.index(prior)] = record
                existing_by_id[media_id] = record
                report["added"].append(media_id)
                Logger.info(f"Overwriting media record '{media_id}'.")
            elif self._record_needs_download(prior):
                # Present but its asset never landed -> retry (self-heal).
                # Refresh credits/appearances/studios from the incoming record.
                prior["appearances"] = record.get(
                    "appearances", prior.get("appearances", [])
                )
                prior["studios"] = record.get(
                    "studios", prior.get("studios", [])
                )
                report["retried"].append(media_id)
                Logger.info(
                    f"Retrying media record '{media_id}': "
                    f"asset not yet downloaded."
                )
            else:
                # Present and already satisfied -> genuine skip.
                report["skipped"].append(
                    (media_id, "id already exists in media.json")
                )
                Logger.warning(
                    f"Skipping media record '{media_id}': "
                    f"id already exists in media.json."
                )

        # Persist the merged catalog before reloading.
        self._write_media_json(existing)

        if download and (report["added"] or report["retried"]):
            self._resolve_new_assets(report, fetcher=fetcher)

        Logger.info(
            f"Ingestion complete: {len(report['added'])} added, "
            f"{len(report['retried'])} retried, "
            f"{len(report['skipped'])} skipped, "
            f"{len(report['resolved'])} downloaded."
        )
        return report

    def rebuild_from_sidecars(self, download=False, overwrite=True):
        """
        Rebuild media.json from on-disk sidecars (catalog loss recovery /
        marathon re-catalogue). download=False re-catalogs metadata only;
        download=True also re-fetches the files.
        """
        from core.paths import Paths

        records = AssetSidecar.scan(Paths().get_media_directory())
        if not records:
            Logger.info("No sidecars found; nothing to rebuild.")
            return {}
        return self.ingest_records(
            records, download=download, overwrite=overwrite
        )

    # ------------------------------------------------------------------
    # Resolution + write-back
    # ------------------------------------------------------------------

    def _resolve_new_assets(self, report, fetcher=None):
        """
        Reload the merged library and resolve assets that still need
        downloading. Standalone media resolve directly; episodes are gated
        through RollingCache.plan_window so only the in-window backlog is
        fetched (not the whole season).
        """

        library = MetadataLoader().load(self.metadata_path)

        real = fetcher or RealFetcher()
        resolver = SourceResolver(real)

        target_ids = set(report["added"]) | set(report["retried"])

        # Self-heal: reconcile catalog status against disk before resolving.
        # A record can read DOWNLOADED in media.json while its file was
        # deleted underneath us (exactly the sidecar-rebuild case). Downgrade
        # those to MISSING so needs_download() qualifies them for re-fetch --
        # no hand-editing media.json required.
        self._reconcile_status_against_disk(library, target_ids)

        episodes_by_series = {}
        standalone = []

        for item in library.get_media():
            if item.get_id() not in target_ids:
                continue
            if isinstance(item, Episode):
                series_id = item.get_series().get_id()
                episodes_by_series.setdefault(series_id, []).append(item)
            else:
                standalone.append(item)

        # Standalone media (Movie / MusicVideo / ...): resolve directly.
        for item in standalone:
            self._resolve_item_assets(item, real, resolver, report)

        # Episodes: only fetch the in-window backlog per series. On a fresh
        # ingest nothing has aired yet, so aired_count = 0.
        cache = RollingCache()  # window_size default; per-series config later
        for episodes in episodes_by_series.values():
            episodes.sort(
                key=lambda e: (
                    e.get_season().get_season_number(),
                    e.get_episode_number(),
                )
            )
            plan = cache.plan_window(episodes, aired_count=0)
            for episode in plan["fetch"]:
                self._resolve_item_assets(episode, real, resolver, report)

        # Durable source of truth: re-serialize the resolved library.
        serialized = self._serialize_media(library)
        self._write_media_json(serialized)

        # Write a metadata sidecar next to each downloaded file so an evicted
        # or externally-deleted file keeps its metadata/sources/fingerprint
        # on disk and can be re-fetched (or drive a marathon rebuild) later.
        target_ids = set(report["added"]) | set(report["retried"])
        for record in serialized:
            if record.get("id") in target_ids:
                AssetSidecar.write(record)

    def _reconcile_status_against_disk(self, library, target_ids):
        """Downgrade any asset that is DOWNLOADED in the catalog but whose
        file is absent on disk to MISSING, so needs_download() returns True
        and SourceResolver re-fetches it.

        This is the ingest-path version of the "reconcile disk against
        catalog" check that LibraryReconciler.verify() performs as a
        standalone maintenance pass. Downgrading only affects genuinely
        missing files, so it is safe on the normal ingest path too.
        """
        for item in library.get_media():
            if item.get_id() not in target_ids:
                continue
            for asset in item.get_media_assets():
                if (
                    asset.get_download_status() == DownloadStatus.DOWNLOADED
                    and not asset.exists()
                ):
                    asset.set_download_status(DownloadStatus.MISSING)
                    Logger.info(
                        f"Reconcile: asset '{asset.get_asset_id()}' file "
                        f"absent on disk; status -> MISSING (will re-fetch)."
                    )

    def _resolve_item_assets(self, item, real, resolver, report):
        """Resolve every asset on `item` that still needs downloading."""

        for asset in item.get_media_assets():
            if not asset.needs_download():
                continue

            # RealFetcher needs the asset bound so technical fields land;
            # fake/injected fetchers don't implement bind().
            if hasattr(real, "bind"):
                real.bind(asset)

            result = resolver.resolve(asset)

            if result["resolved"]:
                report["resolved"].append(item.get_id())
            else:
                report["unresolved"].append(item.get_id())

    # ------------------------------------------------------------------
    # Credit upsert (cast / crew / studios -> people.json / studios.json)
    # ------------------------------------------------------------------

    def _upsert_episode_chain(self, records):
        """
        Consume the transient `tv_chain` payload an episode record may carry.
        Persist Franchise/Series/Season buckets (dedupe by id) and expand the
        chain into one media record per episode (dropped episode keeps the
        real source; siblings get an empty source list to resolve later).
        """
        franchises = self._read_bucket("franchises.json")
        series_bucket = self._read_bucket("series.json")
        seasons_bucket = self._read_bucket("seasons.json")

        fr_by_id = {f.get("id"): f for f in franchises if f.get("id")}
        se_by_id = {s.get("id"): s for s in series_bucket if s.get("id")}
        sn_by_id = {s.get("id"): s for s in seasons_bucket if s.get("id")}

        expanded = []
        touched = False

        for record in list(records):
            chain = record.pop("tv_chain", None)
            if not chain:
                expanded.append(record)
                continue
            touched = True

            series_info = chain.get("series", {})
            series_title = series_info.get("series_title") or record["title"]
            tv_id = chain.get("tmdb_tv_id")
            series_id = f"tmdb-tv-{tv_id}" if tv_id else self._slug(series_title)
            franchise_id = f"{series_id}-franchise"

            # One franchise per series (TMDB has no franchise concept).
            if franchise_id not in fr_by_id:
                fr_by_id[franchise_id] = {
                    "id": franchise_id,
                    "name": series_title,
                    "description": series_info.get("description", ""),
                }
            if series_id not in se_by_id:
                se_by_id[series_id] = {
                    "id": series_id,
                    "title": series_title,
                    "franchise": franchise_id,
                    "description": series_info.get("description", ""),
                    "premiere_year": series_info.get("release_year", 0),
                    "finale_year": 0,
                }

            dropped_sn = record.get("season_number", 1)
            dropped_ep = record.get("episode_number", 1)

            for season in chain.get("seasons", []):
                s_num = season.get("season_number", 0)
                if s_num == 0:
                    continue  # skip "Specials"
                season_id = f"{series_id}-s{s_num}"
                if season_id not in sn_by_id:
                    sn_by_id[season_id] = {
                        "id": season_id,
                        "series": series_id,
                        "season_number": s_num,
                        "title": season.get("title", ""),
                        "description": season.get("description", ""),
                        "premiere_year": season.get("premiere_year", 0),
                    }

                for ep in season.get("episodes", []):
                    e_num = ep.get("episode_number", 0)
                    is_dropped = (s_num == dropped_sn and e_num == dropped_ep)
                    ep_id = f"{series_id}-s{s_num}e{e_num}"
                    air = (ep.get("air_date") or "")[:4]
                    ep_record = {
                        "type": "Episode",
                        "id": ep_id,
                        "title": ep.get("title", ""),
                        "description": ep.get("description", ""),
                        "release_year": int(air) if air.isdigit() else 0,
                        "runtime_minutes": ep.get("runtime_minutes", 0),
                        "season": season_id,
                        "episode_number": e_num,
                        "genres": list(series_info.get("genres", [])),
                    }
                    if is_dropped:
                        # Carry the real source + credits from the dropped record.
                        ep_record["assets"] = record.get("assets", [])
                        for k in ("cast", "crew", "studios"):
                            if record.get(k):
                                ep_record[k] = record[k]
                    else:
                        # Backlog episode: no source yet (acquisition loop fills).
                        from core.paths import Paths
                        _ep_path = str(
                            Paths().get_media_directory()
                            / "Episodes"
                            / f"{ep_id}.mkv"
                        )
                        ep_record["assets"] = [{
                            "asset_id": f"{ep_id}-asset-1",
                            "path": _ep_path,
                            "sources": [],
                        }]
                    expanded.append(ep_record)

        if touched:
            records[:] = expanded
            self._write_bucket("franchises.json", list(fr_by_id.values()))
            self._write_bucket("series.json", list(se_by_id.values()))
            self._write_bucket("seasons.json", list(sn_by_id.values()))

    def _upsert_credits(self, records):
        """
        Consume the transient TMDB credit payload (`cast`/`crew`/`studios`)
        each enriched record may carry, upsert unique Person and Studio
        entries into people.json / studios.json (dedupe by id), and replace
        those keys with a normalized `appearances` array (person ids) plus a
        `studios` id-list on the record.
        """

        people = self._read_bucket("people.json")
        studios = self._read_bucket("studios.json")

        people_by_id = {p.get("id"): p for p in people if p.get("id")}
        studios_by_id = {s.get("id"): s for s in studios if s.get("id")}

        changed_people = False
        changed_studios = False

        for record in records:
            media_id = record.get("id")
            if not media_id:
                continue

            cast = record.pop("cast", []) or []
            crew = record.pop("crew", []) or []
            studio_entries = record.pop("studios", []) or []

            appearances = []
            studio_ids = []

            # --- Cast (performers) -----------------------------------
            for entry in cast:
                person_id, name = self._person_identity(entry)
                if not person_id:
                    continue
                if person_id not in people_by_id:
                    people_by_id[person_id] = self._new_person(person_id, name)
                    changed_people = True
                appearances.append({
                    "id": f"{media_id}-{person_id}-actor",
                    "person": person_id,
                    "role": "ACTOR",
                    "role_name": self._get(entry, "character"),
                    "billing_order": self._get(entry, "order", 0) or 0,
                    "credited": True,
                })

            # --- Crew (production) -----------------------------------
            for entry in crew:
                role = self._crew_role(entry)
                if role is None:
                    continue  # job not in our controlled RoleType map
                person_id, name = self._person_identity(entry)
                if not person_id:
                    continue
                if person_id not in people_by_id:
                    people_by_id[person_id] = self._new_person(person_id, name)
                    changed_people = True
                appearances.append({
                    "id": f"{media_id}-{person_id}-{role.lower()}",
                    "person": person_id,
                    "role": role,
                    "role_name": self._get(entry, "job"),
                    "billing_order": 0,
                    "credited": True,
                })

            # --- Studios ---------------------------------------------
            for studio in studio_entries:
                studio_id, studio_name = self._studio_identity(studio)
                if not studio_id:
                    continue
                if studio_id not in studios_by_id:
                    studios_by_id[studio_id] = {
                        "id": studio_id,
                        "name": studio_name,
                        "country": "",
                        "founded_year": 0,
                        "description": "",
                    }
                    changed_studios = True
                if studio_id not in studio_ids:
                    studio_ids.append(studio_id)

            if appearances:
                record["appearances"] = appearances
            if studio_ids:
                record["studios"] = studio_ids

        if changed_people:
            self._write_bucket("people.json", list(people_by_id.values()))
        if changed_studios:
            self._write_bucket("studios.json", list(studios_by_id.values()))

    def _crew_role(self, entry):
        job = self._get(entry, "job")
        return self._CREW_ROLE_MAP.get(job)

    def _person_identity(self, entry):
        """Return (stable_person_id, display_name) for a cast/crew entry."""

        if isinstance(entry, dict):
            name = entry.get("name") or entry.get("credit_name") or ""
            raw_id = entry.get("id") or entry.get("tmdb_id")
            pid = f"tmdb-person-{raw_id}" if raw_id else self._slug(name)
            return (pid if name else None), name
        if isinstance(entry, str):
            return (self._slug(entry) if entry else None), entry
        return None, ""

    def _studio_identity(self, studio):
        """Return (stable_studio_id, name). Handles str or dict shapes."""

        if isinstance(studio, dict):
            name = studio.get("name") or ""
            raw_id = studio.get("id")
            sid = f"tmdb-studio-{raw_id}" if raw_id else self._slug(name)
            return (sid if name else None), name
        if isinstance(studio, str):
            return (self._slug(studio) if studio else None), studio
        return None, ""

    @staticmethod
    def _new_person(person_id, name):
        """A people.json record matching MetadataLoader._load_people()."""

        return {
            "id": person_id,
            "name": name,
            "stage_name": "",
            "aliases": [],
            "birth_date": "",
            "death_date": "",
            "nationality": "",
            "biography": "",
        }

    @staticmethod
    def _get(entry, key, default=""):
        return entry.get(key, default) if isinstance(entry, dict) else default

    @staticmethod
    def _slug(text):
        slug = "".join(c if c.isalnum() else "_" for c in (text or "").lower())
        return slug.strip("_")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _record_needs_download(self, record):
        """
        A merged record is retry-eligible if any of its assets is missing
        or not in a satisfied download state, judged from the JSON alone.
        """

        assets = record.get("assets", [])

        if not assets:
            return False

        for asset in assets:
            status = asset.get("download_status", "NOT_DOWNLOADED")
            if status != "DOWNLOADED":
                return True
            if not Path(asset.get("path", "")).exists():
                return True

        return False

    def _serialize_media(self, library):
        """
        Flatten every MediaItem in `library` to its media.json shape, then
        re-attach the `appearances` and `studios` arrays the serializer does
        not emit (read back from the just-merged media.json) so credits
        survive the write-back round-trip.
        """

        serializer = MetadataSerializer(library)

        prior_by_id = {
            r.get("id"): r
            for r in self._read_media_json()
            if r.get("id")
        }

        serialized = []
        for item in library.get_media():
            record = serializer._media_to_dictionary(item)
            prior = prior_by_id.get(record.get("id"))
            if prior and prior.get("appearances"):
                record["appearances"] = prior["appearances"]
            if prior and prior.get("studios"):
                record["studios"] = prior["studios"]
            serialized.append(record)

        return serialized

    def _read_records(self, path):
        """Read a drop-in file into a list of record dicts."""

        path = Path(path)

        if not path.exists():
            Logger.error(f"Drop-in file not found: {path}.")
            return []

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            Logger.error(f"Could not read {path}: {error}")
            return []

        if isinstance(data, dict):
            return [data]

        return data if isinstance(data, list) else []

    def _read_media_json(self):
        """Read the current media.json into a list (empty if absent)."""

        if not self.media_json.exists():
            return []

        try:
            with open(self.media_json, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            Logger.error(f"Could not read {self.media_json}: {error}")
            return []

        return data if isinstance(data, list) else []

    def _read_bucket(self, filename):
        """Read an arbitrary metadata bucket (people.json, studios.json)."""

        path = self.metadata_path / filename

        if not path.exists():
            return []

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            Logger.error(f"Could not read {path}: {error}")
            return []

        return data if isinstance(data, list) else []

    def _write_bucket(self, filename, records):
        """Write an arbitrary metadata bucket back to disk."""

        self.metadata_path.mkdir(parents=True, exist_ok=True)

        with open(self.metadata_path / filename, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)

    def _write_media_json(self, records):
        """Write the merged media list back to media.json."""

        self.metadata_path.mkdir(parents=True, exist_ok=True)

        with open(self.media_json, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)
