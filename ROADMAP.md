# VISTOR Roadmap

**Project Status:** Alpha

**Current Version:** 0.8.1

**Last Updated:** September 10, 2026

---

# Purpose

The VISTOR Roadmap defines the planned development path of the project from its initial planning phase through Version 1.0 and beyond.

Unlike the Design Bible, which establishes the vision, philosophy, and long-term goals of VISTOR, the Roadmap serves as the project's active development plan. It identifies major milestones, tracks progress, and helps prioritize work.

The Roadmap is intended to be a living document and will evolve throughout development. Items may be added, removed, or reprioritized as development continues.

---

# Development Philosophy

VISTOR will be developed incrementally.

Each completed milestone should leave the project in a functional and stable state before development proceeds to the next stage.

The primary objective is not rapid development, but consistent progress while maintaining a solid architecture.

Major features should be completed one at a time and thoroughly tested before additional complexity is introduced.

---

# Documentation Set

The project documentation now lives in Docs/:

- VISTOR_Design_Bible.md   — vision and philosophy
- VISTOR_Developer_Guide.md — architecture and implementation reference
- VISTOR_User_Manual.md     — end-user instructions

The Design Bible remains the authoritative description of VISTOR's vision;
implementation detail belongs in the Developer Guide.

---

# Current Milestone

**Phase 8 — Broadcast Programming**

---

# Phase 1 — Project Foundation

## Documentation

- [x] Create Design Bible
- [x] Complete Design Bible
- [x] Create README.md
- [x] Create ROADMAP.md
- [x] Create CHANGELOG.md
- [x] Create Hardware.md
- [x] Create Ideas.md

---

## Project Structure

- [x] Finalize folder structure
- [x] Create setup.ps1
- [x] Create requirements.txt
- [x] Create .gitignore
- [x] Initialize Git repository
- [x] Create first commit
- [x] Create GitHub repository
- [x] Push initial project

---

## Development Environment

- [x] Install Visual Studio Code
- [x] Install Python
- [x] Install Git
- [x] Configure workspace
- [x] Verify relative path support

---

## Application Skeleton

- [x] Create Python entry point (`main.py`)
- [x] Implement application startup sequence
- [x] Implement application shutdown sequence
- [x] Establish application lifecycle
- [x] Build configuration management system
- [x] Initialize logging system
- [x] Implement project path management
- [x] Verify project directory structure
- [x] Build runtime engine skeleton
- [x] Define engine lifecycle
- [x] Display startup banner and version information

---

## Milestone

VISTOR has a complete project structure and is ready for software development.

---

# Phase 2 — Metadata Engine

## Metadata Architecture

- [x] Finalize metadata architecture
- [x] Finalize metadata package organization
- [x] Define metadata inheritance strategy
- [x] Define metadata relationship model
- [x] Document metadata architecture
- [x] Create metadata package structure
- [x] Establish metadata import system
- [x] Verify metadata package loading
- [x] Verify metadata object construction

---

## Metadata Package Structure

The metadata system is organized into:

- `enums/` — fixed classifications and metadata types
- `vocabulary/` — expandable descriptive values
- `library/` — persistent catalog entities
- `media/` — media content models
- `relationships/` — connections between metadata objects
- `services/` — metadata management operations

---

# Metadata Models

## Foundation

- [x] Implement MediaItem
- [x] Implement MediaAsset

---

## Relationships

- [x] Implement Appearance

---

## Media Organization

- [x] Implement Collection

Collection represents curated groupings of media items based on shared creative, thematic, historical, scheduling, or broadcast relationships.

Examples include:
- Programming blocks
- Curated themes
- Broadcast marathons
- Related media groupings

---

## Library Entities

- [x] Implement Person
- [x] Implement MediaLibrary
- [x] Implement Franchise
- [x] Implement Series
- [x] Implement Season
- [x] Implement Advertiser
- [x] Implement Product
- [x] Implement Campaign
- [x] Implement Network
- [x] Implement Studio

---

## Vocabulary

- [x] Implement Genre
- [x] Implement Music Genre
- [x] Implement Language
- [x] Implement Country
- [x] Implement Tag
- [x] Implement Theme
- [x] Implement Content Rating

---

## Television

- [x] Implement Episode
- [x] Implement NewsSegment
- [x] Implement WeatherSegment
- [x] Implement SportsEvent
- [x] Implement SportsTalkShow

---

## Film

- [x] Implement Movie
- [x] Implement Documentary

---

## Advertising

- [x] Implement Commercial
- [x] Implement Promo
- [x] Implement StationID
- [x] Implement Infomercial

---

## Music

- [x] Implement MusicVideo
- [x] Implement Concert

---

## Miscellaneous

- [x] Implement Ambient

---

# Metadata Services

## Architecture

- [x] Create metadata services package
- [x] Implement Metadata Loader
- [x] Implement Metadata Serializer
- [x] Implement Metadata Validator
- [x] Implement Metadata Search
- [x] Implement Metadata Management Service

---

# Metadata Testing

- [x] Create metadata import test
- [x] Verify package exports
- [x] Verify model construction
- [x] Verify relationship creation
- [x] Verify collection behavior
- [x] Verify media library behavior
- [x] Verify metadata population
- [x] Verify serialization round-trip
- [x] Verify metadata loading and relationship resolution

---

# Metadata Population

## Vocabulary Population

- [x] Populate Genres
- [x] Populate Music Genres
- [x] Populate Themes
- [x] Populate Countries
- [x] Populate Tags
- [x] Populate Languages
- [x] Populate Content Ratings

---

## Commercial Library

- [x] Populate Networks
- [x] Populate Advertisers
- [x] Populate Products
- [x] Populate Campaigns

---

## Initial Metadata

- [x] Create Television Metadata
- [x] Create Movie Metadata
- [x] Create Commercial Metadata
- [x] Create Music Metadata

---

## Milestone

VISTOR possesses a complete metadata engine capable of describing, organizing, validating, searching, and managing all supported broadcast assets.

---

# Phase 3 — Media Library

## Metadata Persistence

- [x] Serialize populated vocabulary to JSON
- [x] Serialize library entities to JSON
- [x] Serialize media objects to JSON
- [x] Define on-disk metadata directory layout
- [x] Verify round-trip (populate → serialize → load)

---

## Metadata Loader

- [x] Implement library loading stage
- [x] Implement people loading stage
- [x] Implement series loading stage
- [x] Implement season loading stage
- [x] Implement media loading stage
- [x] Resolve object relationships
- [x] Handle missing or malformed metadata files

---

## Library Organization

- [x] Finalize physical media folder structure
- [x] Organize existing media library
- [x] Normalize filenames
- [x] Verify media assets

---

## Library Population

- [x] Scan Media Library
- [x] Associate Metadata
- [x] Validate Media Library
- [x] Resolve Missing Assets

---

## Milestone

VISTOR possesses a fully populated broadcast library ready for scheduling.

---

# Phase 4 — Playback System

## Channel Management

- [x] Channel Definitions
- [x] Channel Manager
- [x] Previous Channel Support
- [x] Numeric Channel Entry

---

## Player

- [x] Video Playback
- [x] Playlist Management
- [x] Channel Switching
- [x] Resume Playback After Channel Changes
- [x] Persistent Playback
- [x] Remote Controls

---

## Milestone

VISTOR behaves like a functional cable box using the keyboard.

---

# Phase 5 — Cable Box Experience

## On-Screen Display

- [x] Channel Banner
- [x] Program Information
- [x] Volume Indicator
- [x] Mute Indicator
- [x] Clock
- [x] Fade Animations

---

## TV Guide

- [x] Guide Layout
- [x] Current Program
- [x] Upcoming Program
- [x] Time Display
- [x] Navigation

---

## Milestone

VISTOR provides a cable television user interface.

---

# Phase 6 — Intelligent Content Management

_Milestone: availability becomes a runtime state; files can be evicted and
re-fetched without losing metadata or fingerprints._

## Intelligent Content Management

### Asset State Foundation

- [x] Download Status
- [x] Last-Played Tracking
- [x] Ranked Source Descriptors
- [x] Asset Serialization

---

### Keyframe Fingerprinting

- [x] Fingerprint Generation
- [x] Fingerprint Persistence
- [x] Keyframe Match Search

---

### Multi-Archive Resolver

- [x] Source Registry
- [x] Takedown Handling
- [x] Fingerprint-Based Replacement Search
- [x] Relevant-Media Substitution Fallback

---

### Scoring

- [x] Broadcast Score
- [x] Retention Score
- [x] Pinning

---

### Rolling Cache

- [x] Rolling Episode Window
- [x] Retention-Driven Eviction
- [x] Deleted-Content Metadata Retention

---

# Phase 7 — Media Acquisition Pipeline

_Milestone: any dropped URL becomes a fully enriched, downloaded,
fingerprinted media.json record; VISTOR can also grow its own catalogue._

## Media Acquisition

### Infrastructure

- [x] Multi-Provider Download Layer (Internet Archive, YouTube, Direct URL)
- [x] Provider Registry + Fetcher Routing
- [x] Technical Metadata Extraction (ffprobe/mutagen)
- [x] Fingerprint-on-Download
- [x] JSON Media Ingestion Service
- [x] Auto-Resolve Undownloaded Assets on Ingest
- [x] `add_media` CLI Entry Point
- [x] Descriptive Metadata Scraping (title/year/genre)
- [ ] Batch Folder Ingestion
- [x] Rolling Episode Window (per-series, window-gated)

### Library Maintenance

- [x] LibraryReconciler (merge scanner/verifier/validator into one janitor)
- [x] Remove dead MediaFetcher / MediaAssociator
- [x] Flag-by-default dangling-asset resolution (metadata survives)

### Asset Sidecar

- [x] Sidecar Writer (`<file>.vistor.json` next to each download)
- [x] Sidecar Reader + Media-Tree Scan
- [x] Rebuild media.json from sidecars (catalog-loss / marathon recovery)
- [x] Eviction preserves sidecar (metadata survives file deletion)

### Link-Driven Ingestion

- [x] Link Resolver (URL -> provider + reference)
- [x] Media Describer (scrape title / year / description / runtime)
- [x] Media Classifier (type + vocabulary genre guess)
- [x] Record Builder (override > TMDB > classified > scraped > default)
- [x] Media Ingestor (dedupe-by-id, self-healing retry, write-back)
- [x] add_media CLI (link or JSON drop-in)
- [x] Archive-Aware Classifier (weak Movie vote; Artist-Track + music tag out-votes)
- [x] Query Title Normalization (strip MTV / (Official Video) / lyric-video noise)
- [x] Internet Archive Signal Scrape (mediatype/collection/subject + poster_url)

### Web Ingest UI

- [x] Flask drag-and-drop front-end (`add_media_web.py` + `src/ingest/web_app.py`)
- [x] IngestSession backend seam (build / candidates / build-from-tmdb / commit)
- [x] Live preview card (poster, title, year, runtime, genres, description)
- [x] TMDB "did you mean?" candidate picker
- [x] Overwrite-on-commit (replace existing id)
- [x] Launcher env bootstrap (ffmpeg PATH + TMDB_API_KEY + browser auto-open)
- [x] Genre vocabulary bootstrap fix (populate genres.json for round-trip)
- [x] Media-type override dropdown (Auto / Movie / MusicVideo / Episode / Commercial)
- [ ] Persist vocabulary buckets on setup (genres/tags/themes/countries/languages)

### Content-Based Type Detection

- [x] Provider Signal Surfacing (categories/duration/tags/channel + Archive signals)
- [x] ContentProfile (provider-agnostic normalized signal bag)
- [x] TypeScorer (weighted multi-signal voting)
- [x] Confidence Floor + Tie Handling (undecidable -> default/override)
- [x] Internet Archive MusicVideo Detection (music bucket + Artist-Track shape)
- [x] AcoustID / Chromaprint Audio Refiner — deferred
- [x] Per-signal Weight Tuning from labeled sample — deferred

### Authoritative Enrichment

- [x] Authoritative Source Interface (pluggable lookup provider)
- [x] TMDB Lookup Backend (title/year search)
- [x] Genre Mapping (external -> controlled Genre vocabulary)
- [x] Metadata Enricher (overrides > authoritative > classified > default)
- [x] Authoritative Year Precedence (TMDB year over scraped year)
- [x] Cast / Crew Credits Enrichment (TMDB -> people.json + appearances)
- [x] Studio Enrichment (TMDB production companies -> studios.json)
- [x] Graceful Offline Degradation (no key / no network -> fall back)
- [x] TMDB Candidate List (search_candidates -> picker)
- [x] TMDB Lookup-by-ID (chosen candidate -> full credits + poster)
- [x] Poster / Cover Art (poster_url on results)
- [x] MusicBrainz Lookup Backend (keyless recording lookup)
- [x] CompositeSource (TMDB for film/TV, MusicBrainz for music)
- [x] Type-Routed Enrichment (media type selects backend)
- [x] MusicBrainz Original-Year Precedence (earliest release-group date)
- [x] MusicBrainz Genre Mapping (artist genres/tags -> MusicGenre)
- [x] MusicBrainz Original-Type Preference (Single/Album/EP over compilation)
- [x] Title Noise Stripping (trailing MTV/VEVO/HD/HQ/4K)
- [x] Lyrics Enrichment (keyless lyrics.ovh -> MusicVideo caption)
- [ ] TMDB Year+Match Scoring (smarter default pick)
- [ ] IMDb / Wikidata Backends — deferred
- [ ] LLM Classifier Backend — deferred

### Autonomous Catalogue Expansion

- [x] RecommendationSource (TMDB /recommendations -> similar titles)
- [x] Config recommended_media toggle + recommendation_mode
- [x] DiscoveryLoop (seed -> suggest -> source-discover -> acquire)
- [x] Suggest-Only mode (queue suggestions; no download)
- [x] Assisted mode (auto-find candidate URL; human confirms)
- [x] Automatic mode (auto URL-discovery + ingest, week-capped)
- [x] Source URL Discovery backend (archive search for a suggested title)
- [x] Config Persistence (JSON load/save; recommended_media toggle)
- [x] seed_source + max_auto_additions_per_week config fields

---

# Playback & Rendering

_Milestone: the headless Player drives a real on-screen video/audio surface;
the watched channel renders while all others advance headlessly._

- [x] Renderer abstraction (`src/player/renderer.py`: base + Null + Mpv)
- [x] NullRenderer headless fallback (`create_renderer()` when libmpv absent)
- [x] MpvRenderer real libmpv audio/video output
- [x] Player mirrors load/play/pause/stop/volume/mute onto the renderer
- [x] libmpv-2.dll absolute-path PATH bootstrap before `import mpv`
- [x] Engine builds + attaches the shared renderer to the watched channel
- [x] Renderer swap on channel change (old -> NullRenderer, new -> Mpv)
- [x] set_renderer resurfaces the in-progress item on swap
- [x] OSD drawn on the mpv surface each Engine tick (`render_osd`)
- [x] `_format_overlay` maps OSD payloads to on-screen text
- [x] `test_playback.py` (wiring, audio, missing-asset, fallback, real mpv, overlay, resurface)
- [x] Position-sync on channel switch (resume mid-program instead of restart)

---

# Storage & Configuration Foundation

Milestone: media storage is portable and budget-managed, and settings are
adjustable from the TV — so content population is safe on any drive. This
foundation precedes Phase 8 content population._

## Storage

- [x] Configurable media root (Config-driven `Paths`; absolute/external drive support)
- [x] Storage-budget setting + wire `evict_to_budget` into the runtime

## Settings Surface

- [x] TV Settings Menu on the remote (OSD settings overlay + `settings` binding)

## Broadcast Realism

- [x] Broadcast Events model + Broadcast Modes (Off / Between Programs / Mid-Program)

## Scheduling Content (metadata-only)

- [x] Seasonal scheduling logic (Clock calendar helpers → Scheduler selection)
- [x] Schedule authoring (populate `Schedules/`, referencing media by metadata id)

---

# Phase 8 — Broadcast Programming

_Milestone: each content category and channel is populated and schedulable._

### Programming

- [ ] Television Shows
- [ ] Movies
- [ ] Sports
- [ ] News
- [ ] Documentaries
- [ ] Game Shows
- [ ] Talk Shows

---

### Supporting Content

- [ ] Commercials
- [ ] Station IDs
- [ ] Network Promos
- [ ] Music Videos
- [ ] Infomercials
- [ ] Ambient Loops

---

## Channels

- [x] Nickelodeon (#1)
- [x] VISTOR General (#2)
- [x] VISTOR Toons (#3)
- [x] VISTOR Movies (#4)
- [x] VISTOR Kids (#5)
- [x] VISTOR Hits (#6)
- [x] VISTOR Sports (#7)
- [x] VISTOR News (#8)
- [x] VISTOR Docs (#9)
- [x] VISTOR Classic (#10)
- [x] VISTOR Infomercials (#11)
- [x] VISTOR Aquarium (#12)
- [x] VISTOR Fireplace (#13)
- [x] VISTOR Public Access (#14)
- [x] VISTOR Weather (#15)
- [x] VISTOR Seasonal (#16)

> Note: channel objects are defined and load from `channels.json`, but every
> `programming_sources` / `commercial_pools` / `promotional_material` /
> `station_id_graphics` array is still empty. Actual programming is tracked
> in the "Programming", "Supporting Content", and "Commercial System" sections.


---

## Commercial System

- [x] Commercial Pools
- [x] Network Promos
- [x] Station IDs
- [x] Time-Based Commercial Selection
- [x] Seasonal Commercial Selection

---

## Seasonal Programming

- [x] Halloween Marathons
- [x] Thanksgiving Specials
- [x] Christmas Programming
- [x] Summer Programming
- [x] Weekend Marathons

---

## Weather Channel

- [x] Live Weather API
- [x] Forecast Generation
- [ ] Radar Graphics
- [x] Local Forecast
- [ ] Classic Weather Channel Styling

---

## Milestone

VISTOR delivers a television broadcast experience.

---

# Phase 9 — Raspberry Pi Deployment

## Hardware

- [ ] Purchase Raspberry Pi 5
- [ ] Purchase SSD
- [ ] Purchase Cooling Case
- [ ] Purchase IR Receiver
- [ ] Connect CRT Television

---

## Deployment

- [ ] Transfer Project
- [ ] Configure Auto Boot
- [ ] Boot Directly Into VISTOR
- [ ] Full-Screen Startup
- [ ] CRT Output Testing
- [ ] Performance Optimization

---

## Remote Control

- [ ] IR Receiver
- [ ] Channel Up / Down
- [ ] Numeric Entry
- [ ] Previous Channel
- [ ] Volume
- [ ] Mute

---

## Milestone

VISTOR operates as a dedicated standalone cable box.

---

# Phase 10 — Version 1.0

## Final Polish

- [ ] Performance Optimization
- [ ] Bug Fixes
- [ ] Complete Documentation
- [ ] Final Testing
- [ ] Release Version 1.0

---

## Milestone

VISTOR Version 1.0 is complete.

---

# Future Development

Potential additions after Version 1.0 include:

- Remote tape/record function preventing
episode/movie deletion
- Additional regional channel lineups
- Local access channels
- Public bulletin board channel
- Emergency Alert System simulation
- Interactive cable guide enhancements
- Additional broadcast eras
- Plugin architecture
- Optional DVR mode
- Expanded weather features

---

# Documentation Expansion Reminder

The Design Bible is currently the primary project reference.

Once development reaches a stable architecture, expand the documentation into:

- VISTOR.md
- VISTOR_Developer_Guide.md
- VISTOR_User_Manual.md

Until that point, continue maintaining the Design Bible as the authoritative description of VISTOR.

---

# Development Log

## 2026-04-27 (Pre-Git RetroTV prototype)

- Early local development under the working title RetroTV
- Explored core media-playback concepts prior to version control.

## 2026-07-23 (Migration & reset to VISTOR)

- Migrated the project to Git and established version history.
- Reset and rebuilt the project as VISTOR using the RetroTV prototype as its basis.

## 2026-07-23

- Created initial project folder structure.
- Established project documentation structure.
- Completed the Design Bible (Version 1.0).
- Created the Roadmap.
- Created Hardware.md.
- Created Ideas.md.
- Created VISTOR_Specifications.md.
- Created VISTOR_Developer_Guide.md.
- Created VISTOR_User_Manual.md.

---

## 2026-07-24

- Implemented Engine architecture.
- Completed Clock subsystem.
- Added weekday, weekend, and holiday detection.
- Implemented ScheduleType system.
- Implemented ProgrammingBlock.
- Implemented Schedule.
- Implemented Scheduler architecture.
- Established scheduling pipeline foundation for ScheduleLoader.
- Standardized Design Bible formatting for future contributions.
- Completed metadata package architecture.
- Implemented metadata enums and vocabulary systems.
- Implemented library entity models.
- Implemented media models.
- Implemented relationship models.
- Implemented Collection system for curated media groupings.
- Implemented MediaLibrary catalog structure.
- Created metadata smoke testing framework.
- Verified metadata imports, object creation, and relationships.
- Confirmed metadata architecture is ready for service layer development.

---

## 2026-07-25

- Implemented `MetadataPopulation.build_library` to assemble a full media library.
- Populated all vocabulary and commercial-library entities.
- Created initial television, movie, commercial, and music metadata.
- Implemented `MetadataSerializer.save_to_directory` and `_media_to_dictionary` reference flattening.
- Implemented `MetadataLoader` load stages and `_resolve_relationships`.
- Fixed `MetadataLibrary.__init__` missing buckets and removed duplicate accessors.
- Verified full save → load metadata round-trip via `test_metadata.py`.

---

## 2026-07-26

- Completed metadata reference round-trip (genres, tags, themes, languages, countries, networks, franchises, advertisers, products, campaigns, music genres resolved in _resolve_relationships).
- Added new loader stages (_load_advertisers, _load_products, _load_campaigns) and hardened _resolve_relationships against missing _pending refs.
- Added graceful handling of missing/malformed metadata files via the _read_json helper, routed through Logger.
- Closed the episode round-trip gap so series/seasons serialize and episodes reconstruct on load.
- Added MediaVerifier service and filename normalization (normalize_filename).
- Added MediaScanner for physical media discovery under Media/.
- Added MediaAssociator for manifest-driven asset association.
- Added MediaValidator and missing-asset resolution.
- Integrated PlaybackQueue (injectable ordering strategy) into the headless Player.
- Added BroadcastController and wired the Engine pipeline (Scheduler -> Broadcast Controller -> Playback Queue -> Player) with real elapsed time from Clock.

---

## 2026-07-27

- Integrated `PlaybackQueue` (injectable ordering strategy) into the headless `Player` as its `MediaSource`, completing Playlist Management.
- Added `BroadcastController` between Scheduler and Playback Queue; it owns queue population (`clear` + `enqueue`) with an injectable broadcast mode, so the Player never makes scheduling decisions.
- Wired `Engine.update()` to drive the Scheduler -> Broadcast Controller -> Playback Queue -> Player pipeline using real elapsed time diffed from `Clock`.
- Added `Channel` (owns its own Scheduler / Broadcast Controller / Playback Queue / Player) and `ChannelManager` (tracks active + previous channel; ticks every channel each update so all channels stay time-synced).
- Rewired `Engine` to drive all channels through a single shared `Clock` via `ChannelManager` instead of one `Scheduler`, satisfying "channels never stop."
- Added `set_channel_by_number` for on-screen numeric channel selection.
- Added `ChannelLoader` and externalized channel definitions to `channels.json` (add/edit channels with no code changes).
- Added the headless `RemoteController` in `src/remote/` mapping remote keys (channel up/down, numeric entry + enter, previous channel) to `ChannelManager` actions; unbound keys log a warning instead of crashing.
Rewired the Engine to drive all channels through a single shared `Clock` via `ChannelManager` so every channel stays time-synced regardless of which is being watched.
- Added `set_channel_by_number` to `ChannelManager` for on-screen numeric entry.
- Added `scheduling_priority` to `MediaItem` (with serializer/loader round-trip) and `download_status`/`last_played` to `MediaAsset` (model-only for now).
- Fixed duplicated `Channel.__init__` block that discarded constructor args and created inconsistent field names; consolidated to canonical plural names (`programming_sources`, `commercial_pools`, `promotional_material`, `station_id_graphics`).
- Added headless volume/mute state to `Player` (`set_volume`/`volume_up`/`volume_down`/`set_mute`/`toggle_mute`, `get_volume`/`is_muted`, clamped 0-100).
- Wired `ChannelManager` and `OSDManager` into `Engine.initialize()`; `Engine.update()` now ticks channels and the OSD with real elapsed seconds.
- Added an OSD-agnostic `on_channel_change` callback on `ChannelManager` so the Engine raises the channel banner on every switch path without the Channel/Player depending on the OSD.
- Channel Banner, Volume Indicator, and Mute Indicator now fire and auto-hide in the runtime; verified via `test_metadata.py`.
- Added a `PROGRAM_INFO` overlay to `OSDManager` with `show_program_info()`, reusing the shared timed-visibility/fade model.
- Panel reads the now-playing `MediaItem` (title, description, year, runtime, rating, genres, media type) defensively and folds in the active `ProgrammingBlock` time-slot context.
- Wired `Engine.show_info()` to raise the panel for the active channel; verified via `test_metadata.py`.
- Added the Clock OSD overlay: `Engine.show_clock()` formats the current `Clock` time as a 12-hour cable-box string and raises `OSDOverlay.CLOCK` through the shared timed-visibility model.
- Formalized Fade Animations: `OSDManager.get_opacity()` now applies smoothstep easing (`_ease`) to fade-in/out instead of a raw linear ramp, added `is_fading()` and `get_phase()` accessors.
- Completed the Phase 5 On-Screen Display section; verified via `test_metadata.py`.
- Added a headless `Guide` subsystem (`src/guide/guide.py`) that builds an electronic program guide from every channel's Scheduler ProgrammingBlocks: one row per channel with current + upcoming program labels/time-slots, a 12-hour time display, and a clamped selection cursor.
- Wired `Engine.open_guide`/`close_guide`/`toggle_guide`/`guide_up`/`guide_down`; `Engine.update()` refreshes the guide's time while open.
- Added an optional remote `"guide"` button routing through `Engine.toggle_guide()`.
- Added `DownloadStatus` enum and extended `MediaAsset` with availability state (`download_status`, `sources`, `pinned`, `broadcast_score`, `retention_score`, `fingerprint`, `last_played`) plus `to_dictionary()`/`from_dictionary()`, `needs_download()`, `is_available()`.
- Taught `MetadataSerializer._media_to_dictionary` to emit an `"assets"` block and `MetadataLoader._load_media` to rebuild assets; fixed a loader key mismatch (`"media_assets"` -> `"assets"`) that dropped assets on reload.
- Fixed `Theme` `parent_theme` serialization (two-pass parent resolution) that broke `save_to_directory`.
- Verified the full asset persistence round-trip via `test_metadata.py`.

---

## 2026-07-28

- Added a headless keyframe fingerprint service that computes a deterministic, zero-dependency fingerprint for each `MediaAsset` and stores it via `set_fingerprint()`, so identical/twin assets hash identically and distinct assets differ.
- Implemented keyframe match search: given a fingerprint, the service returns matching assets, enabling replacement lookup for missing media.
- Fingerprints persist across the save -> load round-trip (survive eviction) through the existing `MediaAsset.to_dictionary()`/`from_dictionary()` and the serializer/loader `"assets"` block.
- Extended `MediaAsset.add_source` with a `date_posted` field and added `get_source_age_days()` so source age can feed the retention "at-risk" term (older postings imply lower takedown risk / lower retention priority).
- Verified fingerprint generation, twin-matching, and source-age via `test_metadata.py` (all tests pass).
- Added a headless multi-archive `SourceResolver` service that walks each `MediaAsset`'s ranked source list, fetching through a mockable fetcher interface so tests never hit the network.
- Handles takedowns cleanly: `404`/`403` responses warn and fall through to the next ranked source, driving `DownloadStatus` transitions (success → `DOWNLOADED`, exhausted → `FAILED`).
- On total source failure, falls back to a fingerprint-based replacement search, substituting a matching asset (e.g. `res_twin`) when one exists; logs an error only when no source and no replacement resolve.
- Verified via `test_metadata.py` (`=== Testing Multi-Archive Resolver ===`), which exercises the success, 404/403-rebind, fingerprint-substitution, and unresolvable-orphan paths.
- Added a headless `AssetScorer` service (`src/metadata/services/asset_scorer.py`) computing the two independent scores per `MediaAsset`.
- Broadcast Score is airplay-only (repurposability across channels, evergreen vs seasonal bracket, appeal); Retention Score combines broadcast, source fragility (scarcity + posting age via `get_source_age_days()`), and storage footprint.
- `should_evict()` enforces pinning as a hard override — pinned assets are never evicted regardless of score.
- Verified broadcast ordering, retention ordering, and pin/eviction behavior via `test_metadata.py`.
- Added headless `RollingCache` service (`src/metadata/services/rolling_cache.py`)
  implementing the rolling episode window (keep/fetch/evict planning),
  retention-driven eviction (lowest retention_score first, ties by larger
  file_size, pinned assets never evicted), and deleted-content metadata
  retention (eviction sets download_status -> MISSING and keeps the asset +
  MediaItem in the library so fingerprint/sources survive for re-fetch).
- Completes the Intelligent Content Management section of Phase 6.
- Verified via test_metadata.py.
- Added a pluggable multi-provider fetcher so acquisition is provider-agnostic
  (Internet Archive, YouTube, Smithsonian, etc.): each provider is a backend
  behind a common fetch(provider, reference) -> FetchResult interface, with an
  unknown provider returning a 501-style unsupported result. Keeps the network
  mockable and out of the test run.
- Added a headless rolling acquisition loop that fetches missing in-window
  episodes and reports aired episodes as evictable, tying the rolling window
  to the fetcher so the queue stays filled as episodes air.
- Added the ChannelDiscovery service: ranks catalog MediaItems against a
  Channel's spec using richer criteria (primary genre + target audience +
  tag overlap), with programming_sources acting as a hard allow-list when
  non-empty, so free disk space can be filled with channel-appropriate content.
- Renamed the Audience enum member CHILDREN -> KIDS and updated all references.
- Recorded the deferred uncatalogued-internet-search feature under
  Docs/Ideas.md "Catalogue Expansion".
- Verified fetcher dispatch/unsupported-provider, acquisition-loop
  fetch/evict planning, and channel discovery ranking + allow-list filtering
  via test_metadata.py.
- Added a real multi-provider acquisition layer under `src/metadata/services/fetchers/`, replacing the mock-only fetcher with concrete network fetchers that all satisfy the existing `SourceResolver` contract `fetch(provider, reference) -> FetchResult`, so `SourceResolver` itself is unchanged.
- `RealFetcher` routes each `(provider, reference)` through `ProviderRegistry` to the correct fetcher; unknown providers fall back to `GenericHttpFetcher` (treats the reference as a direct URL), covering "any website."
- Provider fetchers ranked by reliability: `InternetArchiveFetcher` (archive.org download URL), `YouTubeFetcher` (yt-dlp; "unavailable/private/removed" mapped to takedown `410`), `GenericHttpFetcher` (streamed HTTP GET).
- `BaseFetcher` owns the shared lifecycle: temp-download -> verify non-empty -> `MetadataProbe` fills technical fields (runtime, codecs, resolution, frame rate, file size, container via ffprobe when present) -> `KeyframeFingerprintService.ensure_fingerprint()` fingerprints before eviction is ever possible -> atomically move into the asset's final path. Non-200/`403`/`404`/`410` results map back to `FetchResult.failure(...)` so the resolver advances to the next ranked source.
- Promoted `requests`, `yt-dlp`, and `mutagen` from planned/commented to active dependencies in `requirements.txt`; all network imports are lazy so the headless test suite still runs offline.
- Added offline `ProviderRegistry` routing + `RealFetcher` delegation tests to `test_metadata.py`, mirroring the existing `_FakeFetcher` pattern (no real network calls).
- Expanded `ChannelConfigs/channels.json` from 2 to 15 channels (numbers 2-16) covering the Design Bible Section 3.8 / ROADMAP categories: Toons, Kids, Movies, Music, Sports, News, Docs, Classic, Infomercials, Aquarium, Fireplace, Public Access, Weather, Seasonal, plus General.
- Extended `MetadataPopulation.create_genres()` with `Variety`, `Weather`, `Ambient`, and `Film` so the new channels' `primary_genre` values exist in the vocabulary.
- Updated the channel-up adjacency assertion in `test_metadata.py` for the expanded lineup (channel_up from #2 now lands on #3, not #4).
- Documented the acquisition layer as Section 7.11 in `Docs/VISTOR_Developer_Guide.md`.
- Verified via `test_metadata.py` (all tests pass, including `=== Testing Provider Registry + RealFetcher (offline) ===`).
- Added a URL-first ingestion front-end so a pasted link becomes a full media
record without hand-authored JSON.
- `LinkResolver` parses a pasted YouTube / Internet Archive / direct URL into
the `(provider, reference)` pair the fetchers expect (youtu.be & `watch?v=` -> youtube video id; `archive.org/download/<id>/<file>` -> internet_archive `<id>/<file>`; anything else -> `direct_url`).
- `MediaDescriber` harvests yt-dlp's info-dict (title, upload year, duration,  description) with no second tool, auto-filling the descriptive fields.
- Added `MediaClassifier`: `classify_type` maps the yt-dlp category/duration to the `MediaType` vocabulary and `classify_genres` maps YouTube categories/tags through a controlled table to VISTOR's 13 `Genre` names only (unmapped tags dropped) — a best-guess with a logged warning, not a hard truth.
- `RecordBuilder` assembles a media.json-shaped record; precedence is overrides > classified/scraped > default, so `--type`/`--genres` always win.
- `add_media.py` gained a `--link`/URL mode with `--type`/`--genres` now optional (omitting them triggers auto-classification); JSON-file mode kept.
- All network/yt-dlp imports remain lazy so the headless smoke test still runs offline with no third-party packages installed.
- Verified via `test_metadata.py` (all tests pass).
- Added an authoritative metadata enrichment layer: a pluggable AuthoritativeSource abstraction with a TMDB backend that looks a title up by name/year and returns canonical title, release_year, genres, description, and runtime.
- Added MetadataEnricher, which fills only empty/zero descriptive fields on a built record so the precedence chain overrides > authoritative > classified > scraped > default holds and manual flags / confident classifier guesses are never overwritten.
- Wired MetadataEnricher into RecordBuilder.build() so a pasted link now flows: LinkResolver -> MediaDescriber -> MediaClassifier -> MetadataEnricher -> ingest-ready record.
- Kept the layer offline-safe: with no TMDB_API_KEY the lookup returns None and the enricher is a no-op, so test_metadata.py still runs with no network or API key.
- Verified fill, override-preservation, and no-op behavior via test_metadata.py (=== Testing MetadataEnricher (offline) ===).
- Added the JSON-drop-in / link ingestion front-end: `add_media.py` -> `LinkResolver` (URL -> provider+reference) -> `MediaDescriber` (yt-dlp info-dict -> title/year/description) -> `MediaClassifier` (deterministic media-type + controlled-vocabulary genre guess) -> `MetadataEnricher` + `TMDBSource` (authoritative fill) -> `RecordBuilder` -> ingest-ready record.
- `MediaIngestor` merges records into `media.json` (dedupe by id), reloads via `MetadataLoader`, and auto-resolves NOT_DOWNLOADED assets through `RealFetcher` + `SourceResolver`, so adding media also downloads, probes, and fingerprints it.
- Made a failed download self-heal: records whose assets are MISSING/FAILED/NOT_DOWNLOADED are retry-eligible on the next run instead of being permanently skipped by id.
- Added write-back: after resolution the reloaded library is re-serialized to `media.json`, so the persisted record carries the resolved `download_status` and `fingerprint` (JSON is the durable source of truth).
- Fixed the yt-dlp merged-container path mismatch in `YouTubeFetcher._download` so the produced file is handed to `BaseFetcher` for probe/fingerprint/move.
- Kept the whole layer offline-safe (lazy yt-dlp/network imports; no TMDB_API_KEY -> enricher no-op); verified via `test_metadata.py` (`=== Testing MediaIngestor Write-Back (offline) ===`) and a live YouTube run.

---

## 2026-07-29

- Fixed release_year precedence: TMDB's authoritative year now overwrites a provisional scraped year (e.g. the YouTube upload year), while an explicit --year override is still never clobbered.
- Extended TMDBSource to return cast/crew/studios (from the TMDB credits endpoint + production_companies) in addition to the descriptive fields.
- Added MediaIngestor credit upsert: people are deduped into people.json and studios into studios.json by stable TMDB id, and each record's credits are rewritten as a normalized appearances array + a studios id list.
- Wired appearances/studios end-to-end through the serializer and loader so a reloaded MediaItem re-links to shared Person and Studio objects instead of duplicating them.
- Added a studios field (add_studio/get_studios) to MediaItem so studios attach to the media item, mirroring the committed appearances handling.
- Hardened media.json read/write so a malformed or empty file no longer soft-fails to an empty catalog and re-triggers a full re-download.
- Verified offline via test.py and end-to-end with the Redline youtu.be link (--reenrich): media.json, people.json, and studios.json all populate and re-link on reload with no asset re-download.
- Added TMDB TV-chain lookup so dropping one episode link enriches and expands the whole series: franchise -> series -> seasons -> per-episode records.
- MediaIngestor now upserts franchises.json/series.json/seasons.json and writes one media.json record per episode (id tmdb-tv-<id>-sNeM), mapping the dropped asset onto its real chain slot rather than a parallel slug-id record.
- Gated episode downloads through RollingCache.plan_window: only window_size upcoming episodes are fetched; aired episodes are reported evictable and the rest stay NOT_DOWNLOADED with their metadata/sources retained.
- add_media.py parses --season/--episode as ints (mirroring --year).
- Added periodic download-progress logging to InternetArchiveFetcher/HttpFetcher so a large streaming .mkv is visibly progressing instead of appearing frozen.
- Verified with the Evangelion ep1 archive link: 26-episode chain built, ep1 holds the dropped file, downloads limited to the backlog window.
- Added a TMDB candidate list (`TMDBSource.search_candidates`) and `lookup_by_id`, plus `poster_url` on normalized results, so ambiguous titles (e.g. Redline 2007 live-action vs 2009 anime) surface a "did you mean ...?" picker instead of blindly taking results[0].
- Added `src/ingest/` package: `IngestSession` (pass-through to RecordBuilder / TMDBSource / MediaIngestor) and a local Flask `web_app` with a drag-and-drop page, cover/year/genre/description preview card, candidate picker, and Confirm/Cancel before commit.
- Added `add_media_web.py` launcher and promoted Flask to an active dependency.
- Added a local drag-and-drop web ingest UI: `add_media_web.py` launcher bootstraps the environment (puts `src/` on `sys.path`, injects the winget ffmpeg `bin` folder onto PATH so yt-dlp can merge, sets `TMDB_API_KEY`, auto-opens the browser) then serves a Flask single-page app on `127.0.0.1:5000`.
- Added `src/ingest/` package: `IngestSession` is a thin pass-through backend seam over the existing services (`build` -> RecordBuilder, `candidates` -> TMDB search, `build_from_tmdb` -> chosen candidate, `commit` -> MediaIngestor), and `web_app.py` exposes `/preview`, `/choose`, `/commit` routes.
- Added a "did you mean?" candidate picker: extended `TMDBSource` with `search_candidates()` / `lookup_by_id()` returning the full ranked results (with poster_url) instead of silently taking `results[0]`, so the wrong same-title film (e.g. 2007 vs. 2009 anime Redline) can be corrected before commit.
- Added `overwrite` to `MediaIngestor.ingest_records`: an existing id is replaced and re-resolved instead of dedupe-skipped, wired through `IngestSession.commit` and the `/commit` route so a corrected record can overwrite a prior one.
- Stripped the display-only `poster_url` key before commit so it never pollutes `media.json`.
- Fixed empty-genre round-trip: populated `Metadata/data/genres.json` from `MetadataPopulation.create_genres()` so the loader's exact-name relinking has a vocabulary to match against; genres (e.g. Animation / Action / Science Fiction) now survive ingest instead of dropping to `[]`.
- Promoted `Flask`, `Pillow`, and `tkinterdnd2` to active dependencies in `requirements.txt`.
- Verified end-to-end via the web UI: dropped the Redline youtu.be link, picked the 2009 anime candidate, confirmed with overwrite, and got `1 added / 1 downloaded` with a fingerprinted `.mkv` and full cast/crew/studios/genres in `media.json`.
- Added RecommendationSource (TMDB /{movie|tv}/{id}/recommendations) that suggests similar titles for a known TMDB id; offline-safe, returns [] with no key/network.
- Replaced Config.load() placeholder with real JSON load/save to Metadata/data/config.json, plus a `recommended_media` toggle and  `recommendation_mode` field (default "suggest_only"; no auto-commit yet).

---

## 2026-07-30

- Added a Recommended Media feature slice: `RecommendationSource` calls TMDB's `/recommendations` endpoint and normalizes results into the same candidate shape the UI already renders. Surfaced through a new `IngestSession.recommendations(tmdb_id, media_type)` method, a `/recommendations` route, and a "You might also add..." panel in `web_app.py`.
- Replaced the placeholder `Config.load()` (which just `pass`ed) with real JSON load/save and a `recommended_media` toggle plus a `recommendation_mode` field defaulting to `suggest_only`; recommendations are gated on this toggle. No auto URL-discovery or auto-commit yet — suggestions are human-confirmed.
- Fixed the recommendation sidebar being cleared when switching between "did you mean?" candidates (`choose()` no longer wipes the candidate/rec panel).
- Added a multi-backend `EnrichmentRouter` that dispatches `lookup()` by `media_type`: TMDB for Movie/Episode, `SportsSource` (TheSportsDB, chosen for its 1980s-onward historical backlog on a permanent free tier) for sports, MusicBrainz for music, and a Wikipedia fallback for everything else. All network imports stay lazy so the headless test suite runs offline.
- Wired `EnrichmentRouter` into `RecordBuilder` via `MetadataEnricher`, replacing the hardcoded `TMDBSource`. Empty/unknown media_type routes to TMDB so plain movie drops still resolve correctly.
- Fixed a year-precedence regression introduced by the router swap: dropping the Redline link again correctly returns `release_year` 2009 instead of the scraped 2019.
- Recorded the Recommended Media feature (auto-suggest / future auto-acquire toggle) in `Docs/Ideas.md`.
- Verified: `EnrichmentRouter().lookup('Redline', media_type='Movie')` returns 2009 with full genres, `RecordBuilder().build(...)` returns 2009, and `IngestSession.recommendations(11970, 'Movie')` returns 8 candidates with the config toggle on.
- Added enrichment backends sports_source.py / musicbrainz_source.py / wikipedia_source.py, each returning the same normalized dict shape as TMDBSource.lookup() and degrading to None offline; enrichment/__init__.py exports them plus EnrichmentRouter, and record_builder.py builds MetadataEnricher(EnrichmentRouter()).
- Replaced the placeholder Config.load() (was `pass`) with JSON load/save and a recommended_media toggle (recommendation_mode default "suggest_only"); added RecommendationSource (TMDB /recommendations) wired into IngestSession so the web UI can surface a config-gated "You might also add..." list.
- Added Ambient as the first persistable non-TMDB type: metadata_loader.py reconstructs Ambient records, MetadataSerializer already emits the correct type via type(item).__name__ (no change needed), and RecordBuilder.LOCAL_DIRS gained an Ambient folder mapping — verified the serializer round-trips type "Ambient".

---

## 2026-08-03

- Added `MusicBrainzSource`, a free/keyless authoritative backend that enriches `MusicVideo` records TMDB structurally cannot match, returning the true original release year and a controlled `MusicGenre`.
- Added `CompositeSource` and `default_source()` presenting a ranked chain (TMDB for film/TV, MusicBrainz for music) to `MetadataEnricher` as a single source.
- Routed enrichment by media type in `RecordBuilder`: the classifier's type is resolved first, then the authoritative backend appropriate for that type runs.
- Pinned the true original release year (1996 for Jamiroquai "Virtual Insanity" instead of the 2009 upload year) by adding a release-group search and taking the earliest first-release-date across recording/releases/release-groups.
- Carried the specific `music_genre` style through `MetadataEnricher.enrich()` and displayed it on the web preview card, and prioritized artist-level genres/tags so styles resolve correctly.
- Cleaned scraped YouTube descriptions: stripped subscribe/WATCH/social URL lines and trailing hashtag blocks while preserving lyrics with real line breaks (`white-space:pre-wrap`).
- Captured the YouTube thumbnail as `poster_url` (display-only; popped before `media.json` write) so music-video previews show a cover.
- Verified end-to-end via the web UI: dropped the Jamiroquai link and got `MusicVideo - 1996 - Jazz`, a cleaned lyrics description, a thumbnail, and `1 added / 1 downloaded` on commit.
- Added a download-stage `AudioRefiner` (`src/metadata/services/audio_refiner.py`): once a MusicVideo file is downloaded, Chromaprint fingerprints the audio and AcoustID resolves it to a MusicBrainz recording MBID, which `MusicBrainzSource.lookup_by_mbid()` turns into a definitive first-release year + controlled MusicGenre — overriding the noisier title-search guess.
- Kept it fully optional/offline-safe: `pyacoustid` and the `fpcalc` binary are imported lazily and `ACOUSTID_API_KEY` is read from the environment; any of them missing makes `refine()` a no-op, so `test.py` still runs offline.
- Wired the refiner into `MediaIngestor` asset resolution so the corrected year/genre is persisted by the existing media.json write-back.
- Made `MediaClassifier` weights data-driven: it now loads `Metadata/data/classifier_weights.json` over its in-code defaults, so tuned weights ship as data, not a code change.
- Added `tools/tune_classifier_weights.py`, a deterministic coordinate-ascent tuner that maximizes `classify_type` accuracy over a labeled sample set (`Metadata/data/classifier_samples.json`) and writes the best weights.
- Promoted `pyacoustid` to requirements (native Chromaprint `fpcalc` still required on PATH for a real match).
- Keyless lyrics.ovh integration in `MusicBrainzSource`: fetches song lyrics as the `MusicVideo` description, keyed on the recording's canonical artist/track (falls back to the parsed title pair).
- Bare-trailing-noise stripping in `MusicBrainzSource._split` (`MTV`, `VEVO`, `HD`, `HQ`, `4K`) so the recording, release-group, and lyrics queries all run on a clean `artist`/`track`.
- Original-release preference in `_release_group_year`: prefers the earliest Single/Album/EP release group over later compilation/live/soundtrack re-issues, pinning the true first-release year.
- Archive-aware voting in `MediaClassifier`: Internet Archive `mediatype=movies` is a weak Movie signal, out-voted by an "Artist - Track" title shape plus a music collection/subject tag.
- `MediaDescriber` now surfaces Internet Archive `mediatype`, `collection`, `subject`, and the item thumbnail (`poster_url`).
- `RecordBuilder` Layer 4 no longer fills a `MusicVideo` description from the scraped archive blurb — music captions are lyrics-or-empty, never source noise.
- Recording selection prefers a high-score match that already carries a first-release-date instead of blindly taking `recordings[0]`.
- Consolidated `MediaScanner`, `MediaVerifier`, and `MediaValidator` into one `LibraryReconciler` (`src/metadata/services/library_reconciler.py`) — a disk-vs-catalog janitor (scan / verify / validate / resolve) for the marathon / re-download use case, separate from the ingest path. Kept `normalize_filename`. Dangling-asset resolution now defaults to flag (not drop) so metadata survives for re-fetch.
- Deleted dead services with no production callers: `media_fetcher.py` (superseded by `RealFetcher`/`ProviderRegistry`/`fetchers/`) and `media_associator.py` (superseded by the media.json-embedded asset model), plus the now-merged scanner/verifier/validator modules.
- Added `DiscoveryLoop` (`src/metadata/services/discovery_loop.py`): autonomous catalogue expansion (seed -> suggest -> source-discover -> acquire) over the existing `RecommendationSource` + `RecordBuilder` -> `MediaIngestor` seam, with suggest_only / assisted / automatic modes. Gated on `recommended_media`; offline-safe no-op without a TMDB key.
- Added `Config` fields `seed_source` and `max_auto_additions_per_week` (load/save) to bound the discovery loop.
- Split the old Phase 6 "Broadcast Experience" block into Phase 6 (Intelligent Content Management), Phase 7 (Media Acquisition Pipeline, with new Library Maintenance + Autonomous Catalogue Expansion sub-sections), and Phase 8 (Broadcast Programming); shortened long step descriptions.
- Updated `Docs/VISTOR_Developer_Guide.md` Section 7.8 service inventory to  drop the deleted services and add `LibraryReconciler` and `DiscoveryLoop`.
- Consolidated authoritative enrichment onto `EnrichmentRouter` and retired `CompositeSource`. Enrichment now dispatches to exactly ONE backend per media type (TMDB for film/TV, MusicBrainz for music, SportsSource for sports, Wikipedia as generic fallback) instead of running every backend and merging per-field. This fixes both the long load times (one network call, not all of them) and the overwrite bug where `TMDBSource` — which lacked a `handles()` hook — ran on `MusicVideo` lookups and won the year/genre/description fields before MusicBrainz could fill them.
- Added `search_candidates`, `lookup_by_id`, and `lookup_tv_chain` pass-throughs (to the TMDB backend) on `EnrichmentRouter` so the web "did you mean...?" picker and the TV-episode chain keep working. Note: `IngestSession` already calls these on its own `TMDBSource` instance, so the picker was never at risk; the pass-throughs cover callers that read them off `MetadataEnricher.source`.
- `default_source()` now returns `EnrichmentRouter()`; `RecordBuilder` is unchanged (it constructs `MetadataEnricher(default_source())`), only its stale CompositeSource comment was updated.
- Deleted `src/metadata/services/enrichment/composite_source.py` and removed it from the enrichment package `__all__`.
- Repaired `test.py`: the earlier service cleanup deleted `MediaVerifier`, `MediaScanner`, `MediaAssociator`, and `MediaValidator` but left their import blocks in the smoke test, which crashed with `ModuleNotFoundError`. Replaced all four with a single `LibraryReconciler` block (scan / verify / validate / resolve + `normalize_filename` assertions).
- Fixed InternetArchiveFetcher for /details/ drops: a bare identifier now resolves the item's primary playable file (largest media file) from the archive metadata API before downloading, and any text/html response is rejected (routed through the takedown path) so a directory-listing page can no longer be saved, probed, and fingerprinted as fake .mkv media. Verified with the Buggles link: 134 MB .mkv, probed 199s 720x480 mpeg2video/mp3.
- Improved MusicVideo enrichment accuracy: the MusicBrainz release-group search now queries on the track title only and relies on the in-loop artist-credit filter, so the original 1979 Buggles year wins over the 1998 reissue; the music genre now displays; lyrics fall back to alternate artist spellings and degrade to empty on a 404.
- KNOWN ISSUE (next up): genres and music_genre are dropped on commit write-back. MetadataLoader never loads music_genres.json (no _load_music_genres in _load_vocabulary), and genres.json / music_genres.json are empty on disk, so name-based relinking has nothing to match. Fix: add _load_music_genres and repopulate both vocabulary files from MetadataPopulation.

---

## 2026-08-03

- Fixed the vocabulary-link regression: MetadataLoader never loaded music_genres.json (no _load_music_genres in _load_vocabulary) and both genres.json / music_genres.json were empty, so name-based relinking in _resolve_relationships dropped genres and music_genre on every reload. Added _load_music_genres, repopulated both files from MetadataPopulation, and expanded _TAG_TO_MUSIC_GENRE to the full controlled MusicGenre set.
- Resolved the KNOWN ISSUE from 2026-08-03: genres and music_genre were dropped on commit write-back because MetadataLoader never loaded music_genres.json and the vocabulary files were empty on disk.
- Added `_load_music_genres` to MetadataLoader (two-pass; resolves `parent_genre` by name, mirroring `_load_themes`) and wired it plus content-rating loading into `_load_vocabulary`.
- MetadataSerializer now writes `music_genres.json` and `content_ratings.json` so all seven controlled-vocabulary types round-trip on save/load.
- Seeded all seven controlled-vocabulary files (genres, music_genres, tags, themes, languages, countries, content_ratings) straight from MetadataPopulation so the loader's exact-name relinking has a full vocabulary to match against.
- Expanded `_TAG_TO_MUSIC_GENRE` to cover every controlled MusicGenre; remapped synth-pop/synthpop -> "Synth Pop" so The Buggles resolves to a real controlled style instead of collapsing to plain Pop.
- Added the missing `import time` to `media_describer.py` and a bounded retry/backoff on the Internet Archive metadata scrape, so a single 10s ReadTimeout no longer degrades a record to `Untitled`.
- Verified: re-dropping the Buggles archive.org link with Confirm & replace persists `genres: ["Music"]` and `music_genre: "Synth Pop"`; `test.py` round-trip loads all vocabulary offline.
- Completed controlled-vocabulary round-trip: added MetadataLoader._load_content_rating and wired it into _load_vocabulary, and MetadataSerializer now writes content_ratings.json, so all seven controlled types (genres, music_genres, tags, themes, languages, countries, content_ratings) reload instead of dropping.
- Seeded the remaining five vocabulary files (tags, themes, languages, countries, content_ratings) from MetadataPopulation; genres.json and music_genres.json were populated in the prior step.
- Added AssetSidecar (`src/metadata/services/asset_sidecar.py`): writes a `<file>.vistor.json` next to every downloaded media file carrying the exact media.json record for the owning item (schema_version + record), so an evicted or externally-deleted file keeps its metadata, ranked sources, and fingerprint on disk.
- Wired sidecar emission into MediaIngestor._resolve_new_assets after the media.json write-back, scoped to just-added/-retried ids; sidecar failures warn but never fail an ingest.
- Added MediaIngestor.rebuild_from_sidecars() and AssetSidecar.scan() to reconstruct media.json from the Media tree (catalog-loss recovery and the marathon re-catalogue use case), deduped by record id.
- Made re-download self-healing: `_reconcile_status_against_disk` downgrades any restored asset whose file is absent (`asset.exists()` is False) from `DOWNLOADED` to `MISSING` before resolution, so `needs_download()` returns True and `SourceResolver` re-fetches automatically -- the "reconcile disk against catalog" job scoped for `LibraryReconciler`.
- Added `rebuild_media.py` CLI: `python rebuild_media.py` rebuilds and downloads; `--no-download` rebuilds catalog-only.
- Verified end-to-end: deleted `Media/MusicVideos/the_buggles_video_killed_the_radio_star_mtv.mkv`, ran the rebuild -> reconcile flipped the asset to MISSING, re-fetched the 134 MB `.mkv` (probed 199s 720x480 mpeg2video/mp3), and `media.json` returned to `download_status: DOWNLOADED`.

---

## 2026-08-29

- Added a real playback/rendering layer behind the headless Player (`src/player/renderer.py`): a `Renderer` base with `NullRenderer` (headless no-op) and `MpvRenderer` (libmpv audio/video), plus `create_renderer()` which returns an `MpvRenderer` when libmpv is importable and falls back to `NullRenderer` otherwise — so unwatched channels and offline tests never decode.
- `Player` now mirrors `load` / `play` / `pause` / `stop` / `set_volume` / `set_mute` onto an injected renderer (defaults to `NullRenderer`), resolving the on-disk file via `_resolve_source_path`; missing-asset items warn and skip `load` instead of crashing.
- `Player.set_renderer` pushes current volume/mute onto the new backend and resurfaces the in-progress item (load + play when state is PLAYING) so a channel switch shows the running program immediately.
- Wired the renderer into `Engine`: build one shared renderer in `initialize()`, `_attach_renderer_to_active()` hands it to the watched channel's Player (previous surfaced player reset to `NullRenderer`), `_on_channel_change` moves it on every switch, and `update()` calls `renderer.render_osd(self.osd)` after the OSD tick so banner/volume/mute/clock overlays paint on the mpv surface. `MpvRenderer._format_overlay` maps the real OSD payload keys (channel_banner `number`/`name`/`program`; program_info `title`/`channel_name`; volume `level`/`muted`; mute `muted`; clock `time`).
- Bootstrapped `libmpv-2.dll` onto PATH via an absolute path before `import mpv` (python-mpv's loader rejects DLLs found under relative %PATH% entries).
- Added `test_playback.py`: Player→renderer wiring, audio propagation, missing-asset safety, headless `NullRenderer` fallback, real mpv playback (auto-skips if libmpv/media absent), `_format_overlay` pure-function coverage, and `set_renderer` swap+resurface.
- Verified end-to-end: real mpv playback of `Media/Episodes/neon_genesis_evangelion.mkv` reported `time_pos ≈ 1.189` after ~2s; all seven tests pass, and `create_renderer()` falls back cleanly when libmpv is absent.
- Flipped `DiscoveryLoop` and `Suggest-Only mode` to done in Phase 7 (verified in `src/metadata/services/discovery_loop.py`); assisted/automatic/source-URL-discovery remained open at this point pending the source-discovery backend (later delivered via `ArchiveSearchSource`, see 2026-08-31 below).
## 2026-08-30 (Storage foundation #1)
- Made the media storage root fully configurable (Design Bible 3.6 / 4.3): `Paths.media` now derives from `Config().load().get_media_directory()`, using an absolute value as-is (external USB SSD / Raspberry Pi drive) and anchoring a relative value under the project root.
- Removed hardcoded `"Media/"` strings from `record_builder.py` (`_path_for` builds from `Paths()`; `LOCAL_DIRS` fallback changed `"Media"` -> `""` to stop double-nesting), `media_ingestor.py` (backlog episode path), and `base_fetcher.py` (default `media_root` falls back to `Paths()` so the `tmp` staging dir shares the destination drive for atomic moves).
- `Paths.verify()` now warns instead of raising when a configured absolute media root is not mounted, so a missing external drive never crashes boot; missing local dirs are created.
- `library_reconciler.py` needed no change — it already resolves through `Paths().get_media_directory()`.
- Verified: default resolves under the project root; an absolute override (`D:\VISTOR_Media`) redirected `Paths`, `RecordBuilder`, and `BaseFetcher` together; `verify()` warned without crashing on an absent drive; `test.py` and `test_playback.py` pass with no leftover hardcoded paths.
- Storage-budget setting + eviction wired. Added a persisted `storage_budget_bytes` config field (default 0 = disabled) with `get_storage_budget_bytes()` / `is_storage_budget_enabled()` accessors.
- Fixed `RollingCache.evict_to_budget` to physically delete files from disk (it previously only flipped `download_status` to MISSING and never freed space); fingerprint + sources are retained for re-fetch (Deleted-Content Metadata Retention).
- Added `StorageManager` to collect resident (downloaded, unpinned) assets from the library and enforce the budget; a no-op when disabled.
- Eviction stays off until an external drive is in place and a nonzero budget is set.
- New `SettingsMenu` (`src/settings/settings_menu.py`) wrapping `Config`, with `bool`, `bytes` (1 GiB step), and `choice` field kinds.
- New `OSDOverlay.SETTINGS` + `OSDManager.show_settings(rows)`.
- New `settings` remote binding + `RemoteController._on_settings`.
- Engine control: `toggle_settings`, `settings_up/down/left/right`, `_refresh_settings_overlay`.
- `MpvRenderer._format_overlay` `settings` case for on-screen rendering.
- New `Config` settings `captions_enabled` and `broadcast_mode` (`off` / `between_programs` / `mid_program`) + getters; persisted in `Config.save()`.
- Storage budget wired into the runtime via `StorageManager.enforce_budget()`.
- Verified via `test.py` and `test_playback.py` (both pass to completion).
- Added position-sync so switching to a channel resumes its program mid-play instead of restarting from 0. Every channel's headless `Player` already advances `position_seconds` on every engine tick (channels never stop); the gap was that `Player.set_renderer` re-`load`ed the file on the newly-surfaced backend but never seeked to that tracked position, so the mpv surface restarted the program at 0.
- Added a `seek(seconds)` method to the renderer interface: `Renderer.seek` (contract), `NullRenderer.seek` (headless log), and `MpvRenderer.seek` (absolute `seek` command, guarded so a not-yet-loaded file can't crash the swap).
- `Player.set_renderer` now seeks the new backend to `self.position_seconds` (when > 0) after `load` and before `play`, so a channel switch shows the live program at the correct offset.
- Added `test_playback.py` Test 8 (position-sync): advance a playing Player 3s, swap in a `RecordingRenderer`, and assert the new backend receives load -> seek(3) -> play; extended `RecordingRenderer` with a `seek` recorder.
- Verified: `test.py` and `test_playback.py` both pass to completion.

---

## 2026-08-30

- Added `src/metadata/services/fetchers/breakpoint_detector.py`: a `BreakpointDetector` that derives commercial-break offsets offline via the existing ffmpeg/ffprobe toolchain (no new dependency), in three tiers: (1) container chapters (`ffprobe -show_chapters`, ignoring the 0s program start), (2) black-frame + silence intersection (`ffmpeg blackdetect` + `silencedetect`, keeping only black midpoints that coincide with a silence midpoint within 2s), (3) runtime-spacing fallback (~every 10 min) per Design Bible 3.4. Every tier degrades to [] when a binary is missing or parsing fails, so a download never fails on detection.
- Persisted a new `breakpoints` field on `MediaAsset` (constructor, `get_breakpoints`/`set_breakpoints`, `to_dictionary`/`from_dictionary`) and in `MetadataSerializer._media_asset_to_dictionary`, so offsets round-trip and survive eviction like the fingerprint.
- Wired detection into `BaseFetcher._finalize` after probe + fingerprint (runs on the temp file before the atomic move), guarded so a failure never fails the download.
- Verified in `test.py` (`=== Testing Breakpoint Detection ===`): breakpoints round-trip through serialization; black/silence stderr parsers intersect correctly; runtime fallback yields even 10-min spacing for a 30-min asset and nothing for a 5-min clip. `test.py` and `test_playback.py` both pass to completion.
- KNOWN LIMITATION: breakpoints are now detected and stored, but `MidProgramMode` cannot consume them yet (broadcast_modes.py not present) and the item-based Player/PlaybackQueue still can't split a file mid-play. Black/silence is a heuristic and may fire on in-content fades.

## 2026-09-08

- Added `src/scheduler/broadcast_event.py`: a `BroadcastEvent` model + `BroadcastEventType` enum (COMMERCIAL_BLOCK / STATION_ID / NETWORK_PROMO, plus reserved BREAKING_NEWS / EMERGENCY_ALERT / WEATHER) so interruptions are first-class items the Broadcast Controller can enqueue without the Player making scheduling decisions. `make_commercial_block()` is the convenience constructor for the common case; real commercial/station-ID media can be attached later via `items` without touching the modes.
- Added `src/scheduler/broadcast_modes.py`: the three concrete Broadcast Modes behind the existing `BroadcastController` seam — `OffMode` (programs in order, parity with `mode=None`), `BetweenProgramsMode` (one commercial block after each program), and `MidProgramMode` (a block per detected breakpoint, falling back to ~10-min runtime spacing, airing whole when neither breakpoints nor runtime are known). `create_broadcast_mode(name)` maps the persisted `Config.broadcast_mode` string (`off` / `between_programs` / `mid_program`) to an instance and defaults unknown values to Off. Item introspection is duck-typed (`get_breakpoints` / `get_runtime_seconds` on the item or its `MediaAsset`) so it works before program items settle on one type.
- Resolved the prior KNOWN LIMITATION: `MidProgramMode` now consumes the breakpoints stored on `MediaAsset` by `BreakpointDetector`. The item-based Player/PlaybackQueue still cannot split a single file mid-play, so for now the program is enqueued once and its breakpoints drive how many commercial blocks follow; the mid-file split remains future work.
- Wired mode selection from Config into the pipeline: `Engine.initialize()` injects `create_broadcast_mode(config.get_broadcast_mode())` into the broadcast controller after `Config().load()`, and `Channel.set_broadcast_mode(name)` lets the ChannelManager propagate the same setting to every channel's own controller.
- Added `=== Testing Broadcast Modes ===` to `test.py`: Off order/no-events, Between-Programs interleave, Mid-Program per-breakpoint split, runtime-spacing fallback, short-program whole-airing, and factory mapping (including the unknown-value default). `test.py` and `test_playback.py` both pass to completion.

## 2026-09-09

- Completed seasonal schedule selection: `Clock` now detects every holiday declared in `ScheduleType` (New Year's Day/Eve, Valentine's, St. Patrick's, Independence Day, Halloween, Thanksgiving [4th Thursday of November], Christmas Eve/Day) and `get_schedule_type()` selects them ahead of the weekday/weekend fallback, so a holiday that lands on a weekend still selects its holiday lineup. Previously only Halloween, Christmas Day, and weekend/weekday were reachable.
- Added `src/scheduler/scheduled_item.py`: `ScheduledItem` references programming by its stable metadata id (`MediaItem.get_id()`) with an optional `resolved` MediaItem slot, so schedules are authored metadata-only — declaring what airs and when without depending on a downloaded file or a loaded MetadataLibrary. Resolution to concrete media is a later (Phase 8) step.
- Rewrote `src/scheduler/schedule_loader.py` to load authored `*.json` schedules from `Paths.get_schedules_directory()`. Each file maps a `schedule_type` string straight onto the `ScheduleType` enum and defines time-slot blocks whose `items` are metadata ids (loaded as `ScheduledItem`s). Malformed files and unknown schedule types are skipped with a warning; when no authored schedules exist, the loader falls back to the prior in-code full-day defaults so the Scheduler always has a lineup. `ScheduleLoader(schedules_directory=...)` is injectable for testing.
- Populated `Schedules/` with authored `weekday.json`, `weekend.json`, and `halloween.json` (contiguous time-slot structure; `items` left empty until content population, since unresolved id-references are not yet fed to the Player).
- Added `=== Testing Seasonal Schedule Selection ===` and `=== Testing Authored Schedule Loading ===` to `test.py`: every holiday/weekday/weekend selection path, Thanksgiving computed dynamically as the fourth Thursday, JSON authoring with media-by-id `ScheduledItem`s, and the empty-directory default fallback. `test.py` and `test_playback.py` both pass.
- Added `src/metadata/services/enrichment/archive_search_source.py`: the Source URL Discovery backend. `ArchiveSearchSource.find_source_url(title, year, media_type)` queries the Internet Archive advanced-search API and returns a `/details/<identifier>` URL for the best match. Best-effort and offline-safe — no key required, `requests` imported lazily, and it returns None with no network / on any failure / when nothing matches. The returned URL flows straight through the existing LinkResolver -> RecordBuilder -> InternetArchiveFetcher path.
- Wired the backend into `DiscoveryLoop`: `_discover_source_url` now delegates to an injectable `source_search` (defaults to `ArchiveSearchSource`) instead of the previous hardcoded `return None`, so assisted and automatic modes are live.
- Assisted mode now surfaces results: the loop records each candidate (with its discovered `source_url`) into a new `report["needs_confirm"]` list for the same human-confirm step the web UI uses, and downloads nothing.
- Automatic mode acquires end-to-end: candidates with a discovered URL are built + ingested with `download=True`, hard-capped by `max_auto_additions_per_week` (overflow recorded in `skipped_cap`). Still gated entirely on `recommended_media`, so it stays OFF by default.
- Corrected the `Config.recommendation_mode` comment to document the values the loop actually branches on (`suggest_only` / `assisted` / `automatic`) instead of the stale `auto_commit`.
- Added `=== Testing Catalogue Expansion (assisted/automatic) ===` to `test.py`: disabled no-op, suggest_only, assisted queueing (with and without a found URL), automatic weekly-cap enforcement, and the offline-safe empty-title path. `test.py` and `test_playback.py` both pass.
- Added a full serialization round-trip test in `test.py` (save populated library -> load -> assert reconstructed counts/references).

## 2026-09-11

- Activated `CommercialSelector` time-of-day / seasonal weighting by adding `airs_at_hour` / `airs_in_season` to the `Commercial` model; the selector's duck-typed eligibility hooks now fire. Wired a per-channel selector into every broadcast mode via `set_broadcast_mode`.
- Generalized `CommercialSelector` into `PoolSelector` (`src/scheduler/pool_selector.py`), a pool-agnostic break filler that keeps the same `select(count, hour, season)` signature and duck-typed `airs_at_hour`/`airs_in_season` weighting, so it fills commercial, network-promo, and station-ID breaks identically.  
- Added `make_network_promo()` and `make_station_id()` constructors to `broadcast_event.py`, mirroring `make_commercial_block()` and reusing the existing `NETWORK_PROMO` / `STATION_ID` event types.  
- Broadcast modes now accept commercial / promo / station-ID selectors; `_make_break` returns the full list of events for a break and modes `extend` rather than `append`. Empty pools still emit empty placeholder blocks (legacy behavior preserved).  
- `Channel.set_broadcast_mode` builds three `PoolSelector`s from `get_commercial_pools()`, `get_promotional_material()`, and `get_station_id_graphics()` and injects them via `create_broadcast_mode(...)`; the engine's per-channel loop drives this unchanged.  
- Flipped `Network Promos` and `Station IDs` to done in Phase 8 Commercial System. All 12 test modules pass.
- Added `ScheduleType.SUMMER` + `Clock.is_summer()` (meteorological June-August), selected after holidays and before the weekday/weekend fallback so summer days get a distinct lineup while holidays like Independence Day still win. Gave `SUMMER` a code default in `ScheduleLoader`.  
- Authored the remaining seasonal schedules under `Schedules/` (`thanksgiving.json`, `christmas_eve.json`, `christmas_day.json`, `summer.json`) and added a "Weekend Marathon" block to `weekend.json`; all metadata-only with empty `items` until content population.  
- Added `LiveWeatherProvider` (keyless wttr.in, lazy `requests` import, guarded fetch) behind `create_weather_provider()`, which now returns it when `requests` is importable and falls back to `NullWeatherProvider` otherwise. Offline-safe: any failure degrades to None/[].  
- Extended `test_scheduling.py` (summer selection + April weekday/weekend) and `test_weather.py` (live-provider parsing + no-network fallback). Full suite passes.