# VISTOR Roadmap

**Project Status:** Pre-Alpha

**Current Version:** 0.6.0

**Last Updated:** July 27, 2026

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

# Current Milestone

**Phase 6 — Broadcast Experience**

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

# Phase 6 — Broadcast Experience  
  
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
  
## Media Acquisition  

### Infrastructure    
  
## Media Acquisition    
    
### Infrastructure    
    
- [x] Multi-Provider Download Layer (Internet Archive, YouTube, Direct URL)    
- [x] Provider Registry + Fetcher Routing    
- [x] Automatic Technical Metadata Extraction (ffprobe/mutagen)    
- [x] Fingerprint-on-Download    
- [x] JSON Media Ingestion Service    
- [x] Auto-Resolve Undownloaded Assets on Ingest    
- [x] `add_media` CLI Entry Point    
- [ ] Descriptive Metadata Scraping (title/year/genre from provider)    
- [ ] Batch Folder Ingestion    
    
---

### Acquisition Engine    
    
- [x] Provider-Agnostic Fetcher    
- [x] Per-Provider Backends (Internet Archive, YouTube, Smithsonian, ...)    
- [x] Rolling Acquisition Loop    
- [x] Channel-Spec Discovery (known catalog)    
- [ ] Catalogue Expansion (uncatalogued search) — deferred    

---
  
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
  
- [x] Cartoon Network  
- [ ] Nickelodeon  
- [x] Movie Channel  
- [x] Music Video Channel  
- [x] Sports Channel  
- [x] News Channel  
- [x] Weather Channel  
- [x] Aquarium Channel  
- [x] Fireplace Channel  
- [x] Infomercial Channel  
  
---  
  
## Commercial System  
  
- [ ] Commercial Pools  
- [ ] Network Promos  
- [ ] Station IDs  
- [ ] Time-Based Commercial Selection  
- [ ] Seasonal Commercial Selection  
  
---  
  
## Seasonal Programming  
  
- [ ] Halloween Marathons  
- [ ] Thanksgiving Specials  
- [ ] Christmas Programming  
- [ ] Summer Programming  
- [ ] Weekend Marathons  
  
---  
  
## Weather Channel  
  
- [ ] Live Weather API  
- [ ] Forecast Generation  
- [ ] Radar Graphics  
- [ ] Local Forecast  
- [ ] Classic Weather Channel Styling  
  
---  
  
## Milestone  
  
VISTOR delivers a television broadcast experience.  
  
---

# Phase 7 — Raspberry Pi Deployment

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

# Phase 8 — Version 1.0

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

## 2026-07-23

- Created initial project folder structure.
- Established project documentation structure.
- Completed the Design Bible (Version 1.0).
- Created the Roadmap.
- Created Hardware.md.
- Created Ideas.md.
- Created VISTOR_Specification.md.
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
- Extended `MetadataPopulation.create_genres()` with `Variety`, `Weather`, and `Ambient` so the new channels' `primary_genre` values exist in the vocabulary.  
- Updated the channel-up adjacency assertion in `test_metadata.py` for the expanded lineup (channel_up from #2 now lands on #3, not #4).  
- Documented the acquisition layer as Section 7.11 in `Docs/VISTOR_Developer_Guide.md`.  
- Verified via `test_metadata.py` (all tests pass, including `=== Testing Provider Registry + RealFetcher (offline) ===`).