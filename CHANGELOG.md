# Changelog

All notable changes to VISTOR will be documented in this file.

The format is based on *Keep a Changelog*, adapted for the long-term development of VISTOR.

---

## [0.1.0] — Core Foundation

### Added

#### Project

- Initial project architecture
- Standardized project folder structure
- Bootstrap installer (`setup.ps1`)
- Relative path installation support
- Git repository
- GitHub repository
- Python virtual environment
- Project dependency management

#### Documentation

- Complete Design Bible
- README
- Roadmap
- Changelog
- Hardware documentation
- Ideas document
- Developer Guide
- User Manual
- Technical Notes

#### Core Application

- Application entry point
- Engine architecture
- Engine lifecycle
- Runtime loop foundation
- Startup sequence
- Shutdown sequence
- Project path management
- Configuration system foundation
- Logging system foundation

#### Scheduling Foundation

- Clock subsystem
- Calendar detection
- Weekday detection
- Weekend detection
- Holiday detection
- ScheduleType
- ProgrammingBlock
- Schedule
- Scheduler architecture

#### Architecture

- Relative Paths philosophy
- Bootstrap Installer philosophy
- Configuration Through Data philosophy
- Project portability architecture

### Milestone

VISTOR possesses a complete project foundation and application skeleton ready for subsystem development.

## [0.2.0] — Metadata Architecture

### Added

- Designed the complete metadata engine architecture.
- Established `MediaItem` as the common base model for every playable broadcast asset.
- Designed reusable library models:
  - Media Library
  - Franchise
  - Series
  - Season
  - Advertiser
  - Product
  - Campaign
- Designed relationship models:
  - Person
  - Appearance
  - Media Asset
- Designed specialized media models for:
  - Television
  - Film
  - Advertising
  - Music
  - Miscellaneous media
- Designed metadata service layer:
  - Metadata Loader
  - Metadata Library
  - Metadata Search
  - Metadata Serializer
  - Metadata Validator
- Added metadata package documentation (`README.md`).
- Expanded the Developer Guide with complete metadata architecture documentation.
- Documented:
  - Metadata architecture philosophy
  - MediaItem philosophy
  - Appearance relationship philosophy
  - Franchise philosophy
  - Commercial hierarchy philosophy
  - Folder organization philosophy
  - Organizational vs. playable media philosophy

### Changed

- Reorganized the metadata package around architectural responsibility rather than file type.
- Replaced the original metadata structure with six primary subsystems:
  - Enums
  - Vocabulary
  - Library
  - Relationships
  - Media
  - Services
- Reorganized media models into functional categories:
  - Advertising
  - Film
  - Music
  - Television
  - Miscellaneous
- Updated the project roadmap to establish the Metadata Engine as its own development phase.
- Refined the overall project architecture to support long-term scalability and reduce metadata duplication.

## [0.3.0] — Metadata Serialization & Round-Trip

### Added

- Implemented `MetadataSerializer.save_to_directory()` to write per-type,
  human-readable JSON files (media, people, networks, studios, vocabulary).
- Implemented `MetadataSerializer._media_to_dictionary()` to flatten nested
  media references into stable id/name keys before serialization.
- Implemented `MetadataLoader` loading stages (`_load_library`, `_load_people`,
  `_load_series`, `_load_seasons`, `_load_media`) and `_resolve_relationships`
  to reconstruct objects and re-link references after loading.
- Added a full serialization round-trip test in `test_metadata.py`
  (save populated library -> load -> assert reconstructed counts/references).

### Changed

- `MetadataLibrary.__init__` now initializes all buckets used by `add_*`
  methods (added `content_ratings`, `music_genres`).
- Removed duplicate `add_*`/`get_*` method definitions in `metadata_library.py`.
- Reference flattening standardized: id-keyed for Network/Studio/Franchise/
  Series/Season/Advertiser/Product/Campaign; name-keyed for Language/Genre/
  Tag/Theme/Country; ContentRating keyed by system:name.

  ## [0.4.0] — Playback & Broadcast Runtime

### Added

- Completed the metadata reference round-trip for all vocabulary, franchise,
  advertiser, product, campaign, and episode relationships in
  `_resolve_relationships`, with new loader stages and graceful handling of
  missing/malformed files via `_read_json`.
- Added the physical-media service layer: `MediaVerifier` (with
  `normalize_filename`), `MediaScanner`, `MediaAssociator`, and `MediaValidator`.
- Integrated `PlaybackQueue` (injectable ordering strategy) into the headless
  `Player` as its media source, completing Playlist Management.
- Added `BroadcastController` between the Scheduler and PlaybackQueue so the
  Player never makes scheduling decisions.
- Added `Channel` and `ChannelManager`, driven by a single shared `Clock`, so
  every channel advances in real time whether or not it is being watched;
  added numeric channel entry (`set_channel_by_number`) and previous-channel.
- Externalized channel definitions to `ChannelConfigs/channels.json` via
  `ChannelLoader`.
- Added the headless `RemoteController` (`src/remote/`) mapping remote keys to
  ChannelManager actions; unbound keys warn instead of crashing.
- Added the OSD subsystem (`src/osd/`): channel banner, volume, mute, program
  info, and clock overlays with smoothstep fade-in/hold/fade-out.
- Added the headless `Guide` subsystem (`src/guide/`) building an electronic
  program guide from every channel's ProgrammingBlocks.

### Changed

- Rewired the Engine to drive all channels through `ChannelManager` on one
  shared `Clock` instead of a single Scheduler.
- Consolidated a duplicated `Channel.__init__` onto canonical plural field
  names (`programming_sources`, `commercial_pools`, `promotional_material`,
  `station_id_graphics`).

### Fixed

- Fixed a loader key mismatch (`"media_assets"` -> `"assets"`) that dropped
  assets on reload, and `Theme.parent_theme` serialization via two-pass
  resolution.

## [0.5.0] — Intelligent Content Management

### Added

- Added a deterministic, zero-dependency keyframe fingerprint service and
  fingerprint-match search for missing-media replacement lookup.
- Added the multi-archive `SourceResolver`, which walks each asset's ranked
  source list through a mockable fetcher, handles 404/403 takedowns by falling
  through to the next source, and falls back to fingerprint-based replacement.
- Added `AssetScorer` (independent broadcast and retention scores) with a hard
  pin override in `should_evict()`.
- Added `RollingCache` (keep/fetch/evict planning with deleted-content
  metadata retention) and a rolling acquisition loop.
- Added `ChannelDiscovery`, ranking catalog items against a channel spec with
  `programming_sources` acting as a hard allow-list when non-empty.

### Changed

- Renamed the `Audience` enum member `CHILDREN` -> `KIDS` across the codebase.

## [0.6.0] — Media Acquisition & Ingestion Pipeline

### Added

- Added a real multi-provider acquisition layer (`src/metadata/services/fetchers/`):
  `RealFetcher` + `ProviderRegistry` routing to `InternetArchiveFetcher`,
  `YouTubeFetcher` (yt-dlp), and `GenericHttpFetcher`, all behind the existing
  `fetch(provider, reference) -> FetchResult` contract; `BaseFetcher` owns the
  download -> probe (`MetadataProbe`/ffprobe) -> fingerprint -> atomic-move
  lifecycle.
- Added the URL-first ingestion front end: `LinkResolver`, `MediaDescriber`
  (yt-dlp info-dict), `MediaClassifier` (deterministic type + controlled-
  vocabulary genre guess), and `RecordBuilder`.
- Added the authoritative enrichment layer (`MetadataEnricher` + `TMDBSource`),
  filling only empty fields so overrides > authoritative > classified >
  scraped > default holds; offline-safe with no API key.
- Added `MediaIngestor`: merges records into `media.json`, auto-resolves
  assets, self-heals failed downloads, and writes back resolved
  status/fingerprint.
- Added TMDB credits (cast/crew/studios) and TV-chain expansion
  (franchise -> series -> seasons -> per-episode records), upserting
  `people.json` / `studios.json` / `franchises.json` / `series.json` /
  `seasons.json`.
- Added the local drag-and-drop web ingest UI: `add_media_web.py` launcher +
  `src/ingest/` package (`IngestSession`, `web_app.py`) with a cover/year/genre
  preview card and a TMDB "did you mean?" candidate picker.
- Added `RecommendationSource` (TMDB `/recommendations`) and a config-gated
  "You might also add..." panel.
- Added the multi-backend `EnrichmentRouter` dispatching by media type (TMDB
  for film/TV, MusicBrainz for music, TheSportsDB for sports, Wikipedia
  fallback).
- Expanded `ChannelConfigs/channels.json` from 2 to 15 channels.

### Changed

- Promoted `requests`, `yt-dlp`, `mutagen`, and `Flask` to active dependencies;
  all network imports stay lazy so the offline smoke test still runs.

### Fixed

- Fixed release-year precedence so TMDB's authoritative year overwrites a
  scraped upload year while an explicit `--year` override is never clobbered.
- Fixed empty-genre round-trip by seeding `Metadata/data/genres.json`.

## [0.7.0] — Music Enrichment, Library Maintenance & Sidecars

### Added

- Added `MusicBrainzSource` (keyless, with lyrics.ovh descriptions) and a
  download-stage `AudioRefiner` (AcoustID/Chromaprint -> definitive first-
  release year + controlled `MusicGenre`); both optional and offline-safe.
- Made `MediaClassifier` weights data-driven (`Metadata/data/classifier_weights.json`)
  and added `Tools/tune_classifier_weights.py`, a coordinate-ascent tuner.
- Added `DiscoveryLoop` for autonomous catalogue expansion
  (suggest_only / assisted / automatic), gated on `recommended_media`.
- Added `AssetSidecar` (`<file>.vistor.json`) so evicted/deleted files keep
  their metadata, sources, and fingerprint; added
  `MediaIngestor.rebuild_from_sidecars()` and the `rebuild_media.py` CLI.

### Changed

- Consolidated `MediaScanner` / `MediaVerifier` / `MediaValidator` into one
  `LibraryReconciler`, and retired `CompositeSource` in favor of the single-
  backend `EnrichmentRouter`.
- Replaced the placeholder `Config.load()` with real JSON load/save
  (`Metadata/data/config.json`) plus `recommended_media`, `recommendation_mode`,
  `seed_source`, and `max_auto_additions_per_week`.

### Removed

- Deleted dead services `media_fetcher.py`, `media_associator.py`, and the
  merged scanner/verifier/validator modules.

### Fixed

- Fixed the vocabulary-link regression: added `MetadataLoader._load_music_genres`
  and `_load_content_rating`, wrote `music_genres.json` / `content_ratings.json`,
  and seeded all seven controlled-vocabulary files so genres/music_genre no
  longer drop on reload.
- Fixed `InternetArchiveFetcher` to resolve the primary playable file for
  `/details/` drops and reject HTML directory listings.

## [0.8.0] — Playback Rendering, Storage & Settings

### Added

- Added the real rendering layer (`src/player/renderer.py`): `Renderer` base,
  `NullRenderer` (headless), `MpvRenderer` (libmpv), and `create_renderer()`
  fallback, wired into the Engine and swapped/resurfaced on channel change with
  position-sync (`seek`) so switching resumes mid-program.
- Made the media storage root configurable (external USB SSD / Pi drive) via
  `Config` + `Paths.get_media_directory()`.
- Added `StorageManager` + `storage_budget_bytes` and taught
  `RollingCache.evict_to_budget` to physically free disk while retaining
  fingerprint/sources.
- Added `SettingsMenu` (`src/settings/`), an `OSDOverlay.SETTINGS` overlay, a
  `settings` remote binding, plus `captions_enabled` and `broadcast_mode`
  config fields.
- Added `BreakpointDetector` (chapters / black-frame+silence / runtime-spacing)
  persisting `breakpoints` on `MediaAsset`.
- Added `test_playback.py` covering renderer wiring, fallback, overlays, and
  position-sync.

## [0.8.1] — Broadcast Programming

### Added

- Added `BroadcastEvent` + `BroadcastEventType` (commercial block / station ID /
  network promo, plus reserved breaking-news / emergency / weather) as
  first-class enqueue-able interruptions.
- Added the three broadcast modes (`OffMode`, `BetweenProgramsMode`,
  `MidProgramMode`) behind `BroadcastController`, selected from
  `Config.broadcast_mode`; `MidProgramMode` consumes stored breakpoints.
- Completed seasonal schedule selection in `Clock` (all declared holidays,
  including dynamically computed Thanksgiving).
- Added `ScheduledItem` (metadata-id references) and rewrote `ScheduleLoader`
  to load authored `Schedules/*.json` with an in-code default fallback;
  seeded `weekday.json`, `weekend.json`, `halloween.json`.
- Added `ArchiveSearchSource` (Internet Archive Source URL Discovery), wiring
  `DiscoveryLoop` assisted/automatic modes end to end.# Changelog

All notable changes to VISTOR will be documented in this file.

The format is based on *Keep a Changelog*, adapted for the long-term development of VISTOR.

---

## [0.1.0] — Core Foundation

### Added

#### Project

- Initial project architecture
- Standardized project folder structure
- Bootstrap installer (`setup.ps1`)
- Relative path installation support
- Git repository
- GitHub repository
- Python virtual environment
- Project dependency management

#### Documentation

- Complete Design Bible
- README
- Roadmap
- Changelog
- Hardware documentation
- Ideas document
- Developer Guide
- User Manual
- Technical Notes

#### Core Application

- Application entry point
- Engine architecture
- Engine lifecycle
- Runtime loop foundation
- Startup sequence
- Shutdown sequence
- Project path management
- Configuration system foundation
- Logging system foundation

#### Scheduling Foundation

- Clock subsystem
- Calendar detection
- Weekday detection
- Weekend detection
- Holiday detection
- ScheduleType
- ProgrammingBlock
- Schedule
- Scheduler architecture

#### Architecture

- Relative Paths philosophy
- Bootstrap Installer philosophy
- Configuration Through Data philosophy
- Project portability architecture

### Milestone

VISTOR possesses a complete project foundation and application skeleton ready for subsystem development.

## [0.2.0] — Metadata Architecture

### Added

- Designed the complete metadata engine architecture.
- Established `MediaItem` as the common base model for every playable broadcast asset.
- Designed reusable library models:
  - Media Library
  - Franchise
  - Series
  - Season
  - Advertiser
  - Product
  - Campaign
- Designed relationship models:
  - Person
  - Appearance
  - Media Asset
- Designed specialized media models for:
  - Television
  - Film
  - Advertising
  - Music
  - Miscellaneous media
- Designed metadata service layer:
  - Metadata Loader
  - Metadata Library
  - Metadata Search
  - Metadata Serializer
  - Metadata Validator
- Added metadata package documentation (`README.md`).
- Expanded the Developer Guide with complete metadata architecture documentation.
- Documented:
  - Metadata architecture philosophy
  - MediaItem philosophy
  - Appearance relationship philosophy
  - Franchise philosophy
  - Commercial hierarchy philosophy
  - Folder organization philosophy
  - Organizational vs. playable media philosophy

### Changed

- Reorganized the metadata package around architectural responsibility rather than file type.
- Replaced the original metadata structure with six primary subsystems:
  - Enums
  - Vocabulary
  - Library
  - Relationships
  - Media
  - Services
- Reorganized media models into functional categories:
  - Advertising
  - Film
  - Music
  - Television
  - Miscellaneous
- Updated the project roadmap to establish the Metadata Engine as its own development phase.
- Refined the overall project architecture to support long-term scalability and reduce metadata duplication.

## [0.3.0] — Metadata Serialization & Round-Trip

### Added

- Implemented `MetadataSerializer.save_to_directory()` to write per-type,
  human-readable JSON files (media, people, networks, studios, vocabulary).
- Implemented `MetadataSerializer._media_to_dictionary()` to flatten nested
  media references into stable id/name keys before serialization.
- Implemented `MetadataLoader` loading stages (`_load_library`, `_load_people`,
  `_load_series`, `_load_seasons`, `_load_media`) and `_resolve_relationships`
  to reconstruct objects and re-link references after loading.
- Added a full serialization round-trip test in `test_metadata.py`
  (save populated library -> load -> assert reconstructed counts/references).

### Changed

- `MetadataLibrary.__init__` now initializes all buckets used by `add_*`
  methods (added `content_ratings`, `music_genres`).
- Removed duplicate `add_*`/`get_*` method definitions in `metadata_library.py`.
- Reference flattening standardized: id-keyed for Network/Studio/Franchise/
  Series/Season/Advertiser/Product/Campaign; name-keyed for Language/Genre/
  Tag/Theme/Country; ContentRating keyed by system:name.

  ## [0.4.0] — Playback & Broadcast Runtime

### Added

  source list through a mockable fetcher, handles 404/403 takedowns by falling
  through to the next source, and falls back to fingerprint-based replacement.
- Added `AssetScorer` (independent broadcast and retention scores) with a hard
  pin override in `should_evict()`.
- Added `RollingCache` (keep/fetch/evict planning with deleted-content
  metadata retention) and a rolling acquisition loop.
- Added `ChannelDiscovery`, ranking catalog items against a channel spec with
  `programming_sources` acting as a hard allow-list when non-empty.


### Added

- Added a real multi-provider acquisition layer (`src/metadata/services/fetchers/`):
  `RealFetcher` + `ProviderRegistry` routing to `InternetArchiveFetcher`,
  `YouTubeFetcher` (yt-dlp), and `GenericHttpFetcher`, all behind the existing
  `fetch(provider, reference) -> FetchResult` contract; `BaseFetcher` owns the
  download -> probe (`MetadataProbe`/ffprobe) -> fingerprint -> atomic-move
  lifecycle.
- Added the URL-first ingestion front end: `LinkResolver`, `MediaDescriber`
  scraped upload year while an explicit `--year` override is never clobbered.
- Fixed empty-genre round-trip by seeding `Metadata/data/genres.json`.

## [0.7.0] — Music Enrichment, Library Maintenance & Sidecars

### Added

- Added `MusicBrainzSource` (keyless, with lyrics.ovh descriptions) and a
  download-stage `AudioRefiner` (AcoustID/Chromaprint -> definitive first-
  release year + controlled `MusicGenre`); both optional and offline-safe.
- Made `MediaClassifier` weights data-driven (`Metadata/data/classifier_weights.json`)
  and added `Tools/tune_classifier_weights.py`, a coordinate-ascent tuner.
- Added `DiscoveryLoop` for autonomous catalogue expansion
  (suggest_only / assisted / automatic), gated on `recommended_media`.
- Added `AssetSidecar` (`<file>.vistor.json`) so evicted/deleted files keep
  their metadata, sources, and fingerprint; added
  `MediaIngestor.rebuild_from_sidecars()` and the `rebuild_media.py` CLI.

### Changed

- Consolidated `MediaScanner` / `MediaVerifier` / `MediaValidator` into one
  `LibraryReconciler`, and retired `CompositeSource` in favor of the single-
  backend `EnrichmentRouter`.
- Replaced the placeholder `Config.load()` with real JSON load/save
  (`Metadata/data/config.json`) plus `recommended_media`, `recommendation_mode`,
  `seed_source`, and `max_auto_additions_per_week`.

### Removed

- Deleted dead services `media_fetcher.py`, `media_associator.py`, and the
  merged scanner/verifier/validator modules.

### Fixed

- Fixed the vocabulary-link regression: added `MetadataLoader._load_music_genres`
  and `_load_content_rating`, wrote `music_genres.json` / `content_ratings.json`,
  and seeded all seven controlled-vocabulary files so genres/music_genre no
  longer drop on reload.
- Fixed `InternetArchiveFetcher` to resolve the primary playable file for
  `/details/` drops and reject HTML directory listings.

## [0.8.0] — Playback Rendering, Storage & Settings

### Added

- Added the real rendering layer (`src/player/renderer.py`): `Renderer` base,
  `NullRenderer` (headless), `MpvRenderer` (libmpv), and `create_renderer()`
  fallback, wired into the Engine and swapped/resurfaced on channel change with
  position-sync (`seek`) so switching resumes mid-program.
- Made the media storage root configurable (external USB SSD / Pi drive) via
  `Config` + `Paths.get_media_directory()`.
- Added `StorageManager` + `storage_budget_bytes` and taught
  `RollingCache.evict_to_budget` to physically free disk while retaining
  fingerprint/sources.
- Added `SettingsMenu` (`src/settings/`), an `OSDOverlay.SETTINGS` overlay, a
  `settings` remote binding, plus `captions_enabled` and `broadcast_mode`
  config fields.
- Added `BreakpointDetector` (chapters / black-frame+silence / runtime-spacing)
  persisting `breakpoints` on `MediaAsset`.
- Added `test_playback.py` covering renderer wiring, fallback, overlays, and
  position-sync.

## [0.8.1] — Broadcast Programming

### Added

- Added `BroadcastEvent` + `BroadcastEventType` (commercial block / station ID /
  network promo, plus reserved breaking-news / emergency / weather) as
  first-class enqueue-able interruptions.
- Added the three broadcast modes (`OffMode`, `BetweenProgramsMode`,
  `MidProgramMode`) behind `BroadcastController`, selected from
  `Config.broadcast_mode`; `MidProgramMode` consumes stored breakpoints.
- Completed seasonal schedule selection in `Clock` (all declared holidays,
  including dynamically computed Thanksgiving).
- Added `ScheduledItem` (metadata-id references) and rewrote `ScheduleLoader`
  to load authored `Schedules/*.json` with an in-code default fallback;
  seeded `weekday.json`, `weekend.json`, `halloween.json`.
- Added `ArchiveSearchSource` (Internet Archive Source URL Discovery), wiring
  `DiscoveryLoop` assisted/automatic modes end to end.

## [0.9.0] — Weather & Commercial System  
  
### Added  
  
- Added the headless Weather subsystem (`src/weather/`): `WeatherProvider` +  
  offline-safe `NullWeatherProvider`, `WeatherService` building `WeatherSegment`  
  items, and `create_weather_provider()` fallback.  
- Added `CommercialSelector` (`src/scheduler/commercial_selector.py`) filling  
  commercial blocks from each channel's `commercial_pools`, with time-of-day /  
  seasonal weighting via optional `Commercial.airs_at_hour` / `airs_in_season`.  
- Wired a per-channel selector into all broadcast modes through  
  `create_broadcast_mode(mode_name, selector=...)` and `set_broadcast_mode`.  
- Repaired channel-to-media auto-matching (genre vocabulary, audience  
  normalization, logo casing) and added `test_channels.py`.  
- Added `test_weather.py` and `test_commercials.py`.

## [0.9.1] — Seasonal Programming & Live Weather  
  
### Added  
  
- Added `ScheduleType.SUMMER` + `Clock.is_summer()` and authored the  
  remaining seasonal schedules (`thanksgiving`, `christmas_eve`,  
  `christmas_day`, `summer`) plus a weekend marathon block.  
- Added `LiveWeatherProvider` (keyless wttr.in) behind  
  `create_weather_provider()`, with an offline-safe fallback to  
  `NullWeatherProvider`.  
- Extended `test_scheduling.py` and `test_weather.py` accordingly.