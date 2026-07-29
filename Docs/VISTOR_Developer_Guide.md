# VISTOR Developer Guide  
  
**Version:** 0.5.0  
  
**Last Updated:** July 28, 2026  
  
---  
  
## Table of Contents  
  
1. Introduction  
    1.1 Purpose  
    1.2 Intended Audience  
    1.3 Development Philosophy  
  
2. Coding Standards  
    2.1 Formatting  
    2.2 Documentation  
    2.3 Architecture  
    2.4 Dependencies  
  
3. Project Architecture  
    3.1 Source Tree  
    3.2 Dependency Direction  
  
4. Core  
    4.1 application.py  
    4.2 clock.py  
    4.3 config.py  
    4.4 logger.py  
    4.5 paths.py  
    4.6 version.py  
  
5. Engine  
    5.1 engine.py  
  
6. Scheduler  
    6.1 scheduler.py  
    6.2 schedule.py  
    6.3 schedule_loader.py  
    6.4 programming_block.py  
    6.5 schedule_type.py  
  
7. Metadata  
    7.1 Purpose  
    7.2 Package Structure  
    7.3 Enums  
    7.4 Vocabulary  
    7.5 Library Models  
    7.6 Relationship Models  
    7.7 Media Models  
    7.8 Metadata Services    
    7.9 Serialization and Loading    
    7.10 Metadata Population    
    7.11 Media Acquisition and Source Resolution
  
8. Subsystems (Not Yet Implemented)  
    8.1 Player  
    8.2 Channel Manager  
    8.3 OSD  
    8.4 Weather  
    8.5 Remote  
    8.6 Guide  
  
9. Testing  
  
10. Contribution Guidelines  
  
11. Future Expansion  
  
---  
  
# 1. Introduction  
  
## 1.1 Purpose  
  
The VISTOR Developer Guide serves as the primary technical reference for contributors.  
  
Unlike the Design Bible, which defines the vision and philosophy of VISTOR, the Developer Guide explains how the software is organized, how its systems interact, and how new functionality should be implemented.  
  
This document is intended to ensure that every contributor develops VISTOR consistently while preserving the project's architecture.  
  
---  
  
## 1.2 Intended Audience  
  
This guide is intended for:  
  
- Core developers  
- Contributors  
- Future maintainers  
- Anyone wishing to understand VISTOR's internal architecture  
  
---  
  
## 1.3 Development Philosophy  
  
Every subsystem should have a single, clearly defined responsibility.  
  
Subsystems communicate through well-defined interfaces rather than directly manipulating one another.  
  
Architecture should remain modular.  
  
When adding new functionality:  
  
- Extend existing systems where appropriate.  
- Avoid introducing unnecessary dependencies.  
- Prefer composition over duplication.  
- Preserve subsystem independence whenever possible.  
  
The objective is long-term maintainability rather than rapid feature development.  
  
---  
  
# 2. Coding Standards  
  
## 2.1 Formatting  
  
- Follow PEP 8.  
- Use descriptive variable names.  
- Avoid unnecessary abbreviations.  
- Keep methods focused on a single responsibility.  
  
---  
  
## 2.2 Documentation  
  
Every public class and method should contain a docstring.  
  
Complex logic should include comments explaining *why* something is being done rather than *what* the code is doing.  
  
---  
  
## 2.3 Architecture  
  
Subsystems should communicate through exposed methods.  
  
Avoid directly modifying another subsystem's internal state.  
  
When possible:  
  
```  
Subsystem A  
        |  
Public Interface  
        |  
Subsystem B  
```  
  
instead of  
  
```  
Subsystem A  
        |  
Internal Variables  
        |  
Subsystem B  
```  
  
---  
  
## 2.4 Dependencies  
  
Dependencies should always point downward through the architecture.  
  
For example:  
  
```  
Engine  
    |  
Scheduler  
    |  
Schedule  
    |  
Programming Block  
```  
  
Not:  
  
```  
Programming Block  
        |  
Engine  
```  
  
Lower-level systems should never depend upon higher-level systems.  
  
---  
  
# 3. Project Architecture  
  
The following sections describe every folder, subsystem, and major source file within VISTOR.  
  
As development continues, this section will expand into a complete architectural reference.  
  
---  
  
## 3.1 Source Tree  
  
```  
src/  
    core/  
    engine/  
    scheduler/  
    metadata/  
    main.py  
```  
  
The `core/`, `engine/`, `scheduler/`, and `metadata/` packages are implemented. Additional subsystems (Player, Channel Manager, OSD, Weather, Remote, Guide) are planned but not yet present in the source tree; they are documented in Section 8.  
  
---  
  
## 3.2 Dependency Direction  
  
VISTOR enforces a strict downward dependency flow. Lower-level packages (such as `core`) must never import from higher-level runtime packages (such as `engine` or `scheduler`).  
  
```  
core  
    |  
metadata  
    |  
scheduler  
    |  
engine  
```  
  
---

# 4. Core  
  
The `core` package contains the foundational runtime services every other  
subsystem depends on: application lifecycle, configuration, logging, timing,  
version reporting, and path resolution.  
  
## 4.1 application.py  
  
Coordinates application startup and shutdown.  
  
Responsibilities:  
- Initialize subsystems in dependency order  
- Start the engine  
- Shut down gracefully  
  
## 4.2 config.py  
  
Holds runtime configuration values, including the active version string.  
  
Note: the version constant here must stay in sync with `version.py`.  
  
## 4.3 logger.py  
  
Provides the shared `Logger` used across subsystems for INFO/SUCCESS/ERROR  
output with timestamps.  
  
## 4.4 version.py  
  
Defines the single `VERSION` constant reported by the application.  
  
## 4.5 paths.py  
  
Resolves all top-level project directories relative to the project root.  
Directory names follow a capitalized convention: `Assets`, `Media`, `Logs`,  
`Config`, `Metadata`, `Schedules`. Consumers should resolve paths through  
`Paths` rather than hardcoding strings, so casing never drifts.  
  
## 4.6 clock.py  
  
Provides current time information for VISTOR and derives the active schedule  
type from the calendar.  
  
Key behavior:  
- `initialize()` / `update()` capture the current `datetime`  
- Calendar helpers: `is_weekday()`, `is_weekend()`, `is_halloween()`,  
  `is_christmas_day()`, `is_holiday()`  
- `get_schedule_type()` returns the correct `ScheduleType` for the current  
  date, falling back to `WEEKDAY`  
  
The Clock consumes the `ScheduleType` enum defined by the scheduler subsystem.  
  
---  
  
# 5. Engine  
  
The engine owns the primary runtime loop and coordinates the Clock and  
Scheduler.  
  
Responsibilities:  
- Construct and initialize the Clock and Scheduler  
- Advance the Clock and Scheduler on each tick  
- Expose the current schedule and programming block to consumers  
- Shut subsystems down in reverse dependency order  
  
Dependencies point downward: Engine → Scheduler → Schedule → Programming Block.  
  
---  
  
# 6. Scheduler  
  
The scheduler selects and advances the active broadcast schedule based on the  
current time.  
  
## 6.1 schedule_type.py  
  
Defines the `ScheduleType` enum — the fixed set of daily/holiday schedule  
classifications (WEEKDAY, WEEKEND, and holiday variants such as HALLOWEEN and  
CHRISTMAS_DAY).  
  
## 6.2 scheduler.py  
  
Manages the active schedule and current programming block.  
  
Key behavior:  
- `initialize()` loads all schedules via `ScheduleLoader` into a  
  `schedule_library` keyed by `ScheduleType`  
- `update()` asks the Clock for the current `ScheduleType`, selects the  
  matching schedule, and resolves the current programming block (or clears it  
  when no schedule matches)  
- `shutdown()` clears the library and current state  
  
## 6.3 schedule_loader.py  
  
Discovers and constructs the schedule library consumed by the Scheduler.  
  
## 6.4 schedule.py / programming_block.py  
  
Represent an individual schedule and the ordered programming blocks within it.  
`Schedule.get_current_block(clock)` resolves which block is active for the  
current time.  
  
---

# 7. Metadata  
  
The metadata system is the descriptive backbone of VISTOR. It separates media  
files from the information that describes them, allowing the scheduler to build  
realistic lineups without depending on folder structure.  
  
## 7.1 Purpose  
  
Metadata answers "what piece of programming is this?" independently of where a  
file is stored or whether a playable file currently exists. Every persistent  
object (Series, Season, Episode, Movie, Commercial, Network, Person, Studio,  
Franchise) carries a stable identifier that does not change with storage  
location.  
  
## 7.2 Package Structure  
  
The `metadata` package is organized into six areas:  
  
- enums/          Fixed architectural classifications  
- vocabulary/     Standardized, expandable descriptive values  
- library/        Persistent library entities  
- media/          Playable broadcast asset models  
- relationships/  Links between people and media  
- services/       Loading, searching, validation, serialization, population  
  
## 7.3 Enums  
  
Enums define how the application understands media. They are stable  
classifications, not per-item descriptions:  
  
- media_type.py         MediaType  
- presentation_type.py  PresentationType  
- audience.py           Audience  
- commercial_type.py    CommercialType  
- role_type.py          RoleType  
  
## 7.4 Vocabulary  
  
Vocabulary provides standardized descriptive values expected to expand as the  
library grows:  
  
- genre.py          Genre (name, description)  
- theme.py          Theme (name, description)  
- tag.py            Tag (name, description, category)  
- country.py        Country (name, iso_alpha2, iso_alpha3, region)  
- language.py       Language  
- content_rating.py ContentRating (system, name)  
- music_genre.py    MusicGenre  
  
## 7.5 Library Models  
  
Persistent entities that own stable identifiers and are referenced (not  
duplicated) throughout the library:  
  
- person.py       Person (id, name, stage_name, aliases, biography, ...)  
- network.py      Network (id, name, abbreviation, description)  
- studio.py       Studio (id, name, country, founded_year, description)  
- franchise.py    Franchise  
- series.py       Series  
- season.py       Season  
- advertiser.py   Advertiser (id, name; now exposes get_id())  
- product.py      Product  
- campaign.py     Campaign  
- media_library.py MediaLibrary (catalog: movies, episodes, music videos,  
                    commercials, with total-count helpers)  
  
Reference philosophy: dependent entities are assembled so shared references  
stay consistent — Advertiser → Product → Campaign → Commercial — preserving a  
single source of truth and preventing duplicate entities.  
  
## 7.6 Media Models  
  
All playable assets inherit from `MediaItem` (media/media_item.py), the common  
base carrying id, title, description, release_year, runtime_minutes,  
media_type, presentation_type, content_rating, audience, original_network,  
production_country, languages, genres, tags, themes, appearances, and  
media_assets.  
  
Concrete media types, grouped by domain:  
  
- film/          movie.py, documentary.py  
- television/    episode.py, special.py, talk_show.py, news_segment.py,  
                 weather_segment.py  
- advertising/   commercial.py, infomercial.py, promo.py, station_id.py  
- music/         music_video.py, concert.py, live_performance.py  
- sports/        sports_event.py, sports_highlight.py, sports_talk_show.py  
- miscellaneous/ ambient.py  
  
collection.py provides curated groupings of media items.  
  
Note: Episode requires a Season instance at construction, so episodes depend on  
the franchise → series → season chain being present to reconstruct.  
  
## 7.7 Relationship Models  
  
- appearance.py   Appearance — a person's participation in a media item  
                  (person, media_item, role, credit_name, role_name,  
                  organization, billing_order, credited, notes)  
- media_asset.py  MediaAsset — links a media item to a concrete playable file  
  
## 7.8 Services  
  
- metadata_library.py    MetadataLibrary — central in-memory container for all  
                         loaded objects (media, people, networks, studios,  
                         vocabulary buckets, relationships) with add_/get_  
                         accessors and total-count helpers  
- metadata_population.py MetadataPopulation — builds a fully populated library  
                         (build_library) using shared references  
- metadata_search.py     MetadataSearch — query helpers over the library  
- metadata_validator.py  MetadataValidator — integrity checks over loaded data  
- metadata_serializer.py MetadataSerializer — flattens objects to JSON  
- metadata_loader.py     MetadataLoader — reconstructs the library from disk  
  
## 7.9 Serialization and Loading Round-Trip  
  
Metadata is persisted as per-type, human-readable JSON files (one file per  
bucket) rather than a single combined document. Each bucket lives under the  
project's `Metadata/data/` directory, and the same casing is used by the  
serializer, the loader, and any calling code so the round-trip behaves  
identically on case-sensitive (Linux/macOS) and case-insensitive (Windows)  
filesystems.  
  
Every persistent object is written and re-linked by its stable identifier  
(`get_id()`). Identifiers—not names—are the single source of truth for  
references across the entire metadata system, including advertisers, products,  
campaigns, franchises, series, seasons, networks, and studios.  
  
Serialization (MetadataSerializer):  
- `to_dictionary()` produces the in-memory dictionary of all buckets.  
- `save_to_directory(directory)` writes each bucket to its own JSON file.  
- `_object_to_dictionary()` copies an object's public attributes.  
- `_media_to_dictionary()` flattens a media item, replacing every nested  
  reference object with its identifier (`get_id()`) so `json.dump` can  
  serialize it. This includes the commercial chain (advertiser, product,  
  campaign), the television chain (season, series, franchise), and the shared  
  vocabulary/library references (network, studio, country, languages, genres,  
  tags, themes).  
  
Loading (MetadataLoader):  
- `load(metadata_path)` constructs a MetadataLibrary and runs the load stages in  
  order: vocabulary, library (networks/studios), people, series, seasons,  
  media, then relationship resolution.  
- Each stage reads its JSON file, reconstructs objects, and adds them to the  
  library. Flattened identifier references are held on a temporary `_pending`  
  payload until relationships are resolved.  
- `_resolve_relationships()` re-links every flattened identifier back to its  
  loaded object instance—Episode → Season, Season → Series, Season → Franchise,  
  Appearance → Person, Commercial → Advertiser/Product/Campaign, and each media  
  item → network/studio/country/languages/genres/tags/themes—then clears the  
  temporary `_pending` payload.  
  
Because references are stored and restored by identifier, a populated library  
can be written to disk and reconstructed with every shared reference intact,  
giving a complete save → load round-trip with no duplicated entities.  
  
---

## 7.11 Media Acquisition and Source Resolution    
    
VISTOR separates a media item's existence from its local availability. The    
metadata library is the complete broadcast catalog regardless of what exists    
on disk, so acquisition is the runtime process that turns a catalogued    
MediaAsset into a verified local file. Because metadata is permanent and    
availability is a dynamic state, acquisition can run, fail, retry, and    
substitute without ever mutating the catalog.    
    
### Source Resolution    
    
Every MediaAsset carries a ranked list of remote `sources`, each a lightweight    
descriptor `{provider, reference, quality, date_posted}`. Order is preference:    
the resolver tries them top-down and advances on failure.    
    
`SourceResolver` (services/source_resolver.py) owns this logic. It marks the    
asset DOWNLOADING, walks the ranked sources, and on the first success marks it    
DOWNLOADED and verified. HTTP-style takedown statuses (403, 404, 410) are    
treated as "source gone" and cause it to advance to the next source rather    
than fail. If every source fails, it attempts a keyframe-fingerprint-based    
replacement before finally reporting failure.    
    
The network fetch itself is delegated to a pluggable "fetcher" object so the    
resolver stays fully testable without touching the network. A fetcher only    
needs to expose one method:    
    
    fetch(provider: str, reference: str) -> FetchResult    
    
`FetchResult` is a small value object with `success()` and `failure(status)`    
factory helpers. The smoke test supplies a canned `_FakeFetcher`; production    
supplies `RealFetcher`.    
    
### Fetchers Package    
    
The `services/fetchers/` package provides the production fetchers. All of them    
satisfy the resolver's fetcher contract, so `SourceResolver` itself is never    
modified:    
    
```  
services/fetchers/    
    __init__.py                    Exports the fetcher classes    
    base_fetcher.py                BaseFetcher — shared download lifecycle    
    metadata_probe.py              MetadataProbe — ffprobe/mutagen extraction    
    internet_archive_fetcher.py    InternetArchiveFetcher (rank 1)    
    youtube_fetcher.py             YouTubeFetcher (rank 2, yt-dlp)    
    generic_http_fetcher.py        GenericHttpFetcher (catch-all)    
    provider_registry.py           ProviderRegistry — provider -> fetcher    
    real_fetcher.py                RealFetcher — SourceResolver entry point    
```  
    
- RealFetcher is the object passed to `SourceResolver(fetcher=...)`. It routes    
  each `(provider, reference)` through the ProviderRegistry to the correct    
  fetcher and forwards the target MediaAsset so technical fields are populated    
  on success.    
- ProviderRegistry maps a source's `provider` string to a concrete fetcher.    
  Known providers are `internet_archive`, `youtube`, and `generic_http` /    
  `direct_url`; unknown providers fall back to GenericHttpFetcher, which treats    
  the reference as a direct URL so effectively any website is downloadable.    
- Providers are ranked by reliability. Internet Archive is preferred first    
  because its references are stable and dated; YouTube is second via yt-dlp;    
  arbitrary direct links are the catch-all.    
- BaseFetcher owns the shared lifecycle every provider reuses: download to    
  `Media/tmp/`, verify the file is present and non-empty, probe technical    
  metadata, fingerprint, then atomically move the file to the asset's final    
  path. Provider subclasses implement only `_download(reference, temp_path)`,    
  returning an HTTP-style status code, and map "gone/forbidden" outcomes to    
  403/404/410 so the resolver advances to the next source.    
    
### Automatic Metadata Extraction    
    
MetadataProbe fills the MediaAsset technical fields that already exist on the    
model (`runtime_seconds`, `video_codec`, `audio_codec`, `container`, `width`,    
`height`, `frame_rate`, `file_size`). It uses `ffprobe` when present on PATH    
for full stream information and degrades gracefully to file-size-only when it    
is not, so a missing tool never fails a download. Every successfully obtained    
asset is then fingerprinted from its keyframes before it can ever be evicted;    
the fingerprint is retained permanently even after the file is deleted, which    
is what allows a taken-down asset to be reverse-searched and reacquired later.    
    
### Dependencies    
    
Acquisition adds three third-party dependencies — `requests`, `yt-dlp`, and    
`mutagen`. All network imports are performed lazily inside the fetcher methods    
so the headless smoke test (Section 9) continues to run offline with no    
third-party packages installed.    
    
### Acquisition Flow    
    
```  
SourceResolver.resolve(asset)    
    RealFetcher.fetch(provider, reference)    
        ProviderRegistry.get(provider)    
            internet_archive -> InternetArchiveFetcher    
            youtube          -> YouTubeFetcher (yt-dlp)    
            generic_http     -> GenericHttpFetcher    
            direct_url       -> GenericHttpFetcher    
            <unknown>        -> GenericHttpFetcher (fallback)    
                BaseFetcher.fetch()    
                    1. temp-download to Media/tmp/    
                    2. verify (status 200, non-empty)    
                    3. MetadataProbe.populate()  -> runtime/codecs/res/size    
                    4. ensure_fingerprint()      -> keyframe fingerprint    
                    5. move temp -> asset final path    
                    6. FetchResult.success() / .failure(status)    
```  
    
Dependencies point downward: acquisition lives in the metadata `services`    
layer and depends only on `core` (Logger) and the metadata models, never on    
the scheduler or engine.

---

# 8. Subsystems  
  
The following subsystems are defined in VISTOR's architecture but are not  
yet implemented. Each has a reserved location in the source tree and a  
single, well-defined responsibility it will assume once built.  
  
## 8.1 Player  
  
**Status:** Not yet implemented.  
  
Will handle media playback, decoding, and transport control (play, pause,  
seek). Consumes the ProgrammingBlock selected by the Scheduler and reports  
playback position back to the runtime loop.  
  
## 8.2 Channel Manager  
  
**Status:** Not yet implemented.  
  
Will manage the set of available channels, channel selection, and the  
mapping between a channel and its active Schedule.  
  
## 8.3 OSD (On-Screen Display)  
  
**Status:** Not yet implemented.  
  
Will render on-screen overlays such as the channel bumper, clock, and  
now-playing information over the active video output.  
  
## 8.4 Weather  
  
**Status:** Not yet implemented.  
  
Will provide weather data for weather-themed channels and segments,  
integrating with the metadata WeatherSegment media type.  
  
## 8.5 Remote  
  
**Status:** Not yet implemented.  
  
Will translate physical or virtual remote input into commands (channel up  
or down, power, menu) dispatched to the runtime.  
  
## 8.6 Guide  
  
**Status:** Not yet implemented.  
  
Will present an electronic program guide built from the Scheduler's  
ProgrammingBlocks across channels.  
  
---  
  
# 9. Testing  
  
VISTOR currently uses a smoke-test script rather than a formal test  
framework.  
  
## 9.1 test_metadata.py  
  
Located at the repository root, test_metadata.py exercises the metadata  
layer end to end. It runs from the repo root with:  
  
    python test_metadata.py  
  
The script verifies, in order:  
  
- Metadata imports resolve across enums, vocabulary, library, media,  
  relationships, and services.  
- Core models construct correctly (Person, MediaItem, Appearance).  
- Collections and MediaLibrary catalog behavior.  
- MetadataLibrary bucket storage and retrieval.  
- MetadataSearch lookups.  
- MetadataSerializer.to_dictionary output shape.  
- MetadataValidator passes on populated data.  
- MetadataPopulation.build_library assembles movies, episodes, music  
  videos, and commercials with shared references intact.  
- A full serialization round-trip: a populated library is written to disk  
  with save_to_directory and reloaded with MetadataLoader, confirming the  
  reconstructed objects and their references match.  
  
A successful run ends with "All tests passed successfully."  
  
## 9.2 Testing Conventions  
  
- Tests should run without external services or network access.  
- Each new subsystem should add its own smoke test at the repository root  
  until a formal test framework is adopted.  
  
---  
  
# 10. Contribution Guidelines  
  
## 10.1 Branching and Commits  
  
- Keep commits focused and descriptive.  
- Ensure test_metadata.py passes before committing metadata changes.  
  
## 10.2 Code Style  
  
- Follow the formatting rules in Section 2 (Coding Standards).  
- Dependencies point downward through the architecture; higher-level  
  subsystems depend on lower-level ones, never the reverse.  
  
## 10.3 Documentation  
  
- Update this Developer Guide when a subsystem's implementation status  
  changes (for example, moving a component out of Section 8 once built).  
- Keep the Design Bible focused on vision and philosophy; implementation  
  detail belongs here.  
  
---  
  
# 11. Future Expansion  
  
Planned work, in rough order of development priority:  
  
- Implement the Player subsystem and wire it to the Scheduler output.  
- Implement the Channel Manager and channel selection.  
- Build the OSD overlay layer.  
- Add the Weather subsystem and connect it to WeatherSegment metadata.  
- Implement Remote input handling.  
- Build the Guide (electronic program guide).  
- Adopt a formal test framework as the codebase grows.  
  
---