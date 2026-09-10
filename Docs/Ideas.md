## Long-Term Feature Concepts

The following ideas are intentionally exploratory. They are not part of the current development roadmap but represent directions VISTOR may evolve toward as the project matures.

### Preset Channel Bundles

Rather than requiring every user to build an entire cable lineup from scratch, VISTOR could ship with several curated channel presets. During installation, users could choose which channels they would like to include, while still retaining the ability to create custom channels later.

Each preset could automatically download and organize the media required for that channel, dramatically simplifying setup for new users.

---

### Adjustable Media Library Size

To accommodate different storage capacities, channels could offer configurable media library sizes.

For example:

- Minimum
- Medium
- Maximum

Smaller libraries would reuse programming more frequently while requiring significantly less disk space. Larger libraries would maximize variety and reduce repetition.

---

### Dynamic Episode Management

Rather than permanently storing every episode of every television series, VISTOR could maintain only the episodes necessary for upcoming broadcasts.

After an episode airs, it could eventually be removed and replaced by the next scheduled episode, allowing enormous television libraries to exist while keeping storage requirements relatively small.

This concept would require intelligent download scheduling, caching, and offline safeguards, making it a long-term research item.

---

### Seasonal Programming

Programming should evolve throughout the year.

Examples include:

- Halloween horror marathons
- Christmas movie blocks
- Thanksgiving specials
- Summer movie events
- Back-to-school programming
- Valentine's Day romantic films

Seasonal changes should feel natural rather than manually selected.

---

### Recurring Television Events

Certain recurring television traditions could automatically appear on the schedule.

Examples:

- Saturday Morning Cartoons
- Sunday movie presentations
- Shark Week
- Holiday marathons
- Network anniversary specials
- Sweeps Week promotional events

These recurring blocks help reinforce the feeling of living inside a functioning television ecosystem.

---

### Historic Broadcast Events

Major real-world broadcasts could automatically appear when appropriate.

Examples include:

- Presidential debates
- Election night coverage
- New Year's Eve ball drops
- Olympic opening ceremonies
- Space shuttle launches
- Significant breaking news coverage

These events would only appear within eras in which they originally occurred.

---

### Context-Aware Ambient Channels

Certain channels could respond to both the calendar and the user's real-world environment.

Examples:

- Rain on a window during local rainfall
- Fireplace channels during winter holidays
- Snow ambience during snowstorms
- Ocean ambience during summer
- Seasonal music programming

The goal is to make VISTOR feel connected to the viewer's surroundings without becoming a modern streaming service.

---

### Localized Content

Future versions could optionally incorporate the viewer's approximate location.

Possible applications include:

- Local news archives
- Regional weather broadcasts
- Local station identifications
- Area-specific commercials
- Regional sports coverage

This feature would require careful consideration of content availability and privacy.

---

### Philosophy

The long-term vision of VISTOR is not simply to organize media into playlists, but to recreate the experience of living with television as an ever-present part of everyday life. Every season, holiday, major event, weather pattern, and cultural moment should influence what appears on-screen, allowing the system to feel alive rather than static.

## Era-Based Television Experiences

Although VISTOR is currently focused on recreating the late 1990s and early 2000s cable television experience, the underlying architecture could eventually support complete television ecosystems from other periods in history.

Rather than simply changing the programming lineup, an era would redefine the entire viewing experience. Channel schedules, commercials, station identifications, network branding, local news, election coverage, weather graphics, promotional material, seasonal events, and television presentation would all reflect the selected period.

For example, choosing the year 1987 would produce a dramatically different experience than choosing 2003. Likewise, major historical events such as presidential elections, Olympic Games, natural disasters, or significant cultural moments could automatically appear within the programming at the appropriate points in the calendar, preserving the feeling of living through that era rather than simply watching isolated media from it.

This concept significantly expands the scope of VISTOR and introduces challenges regarding content availability, licensing, storage requirements, and historical accuracy. For these reasons it is considered a long-term vision rather than an immediate development goal.

One possible future implementation could involve downloadable "era packs" containing curated media libraries, schedules, branding assets, and interface themes representing specific time periods. Different VISTOR distributions or hardware editions could even ship preconfigured around a particular decade, allowing users to experience television as it existed during that era.

# Intelligent Content Management

## Overview

Rather than permanently storing every piece of media on the local system, VISTOR should eventually support an intelligent content management system capable of automatically downloading, caching, and removing media based on scheduling needs and available storage.

This would allow VISTOR to operate efficiently on systems with limited storage or internet bandwidth while maintaining the illusion of a complete broadcast library.

---

## Metadata vs Availability

VISTOR should distinguish between:

- The complete metadata library
- Media currently available on the local machine

Every media item may exist within the metadata library, even if its associated media file has not yet been downloaded.

Availability should therefore become a runtime state rather than permanent metadata.

---

## Sequential Episode Downloads

Rather than downloading entire television series, VISTOR should maintain only a small rolling window of upcoming episodes.

Example:

Downloaded:

- Episode 5
- Episode 6
- Episode 7

After Episode 5 airs:

- Delete Episode 5
- Download Episode 8

Result:

- Episode 6
- Episode 7
- Episode 8

This dramatically reduces storage requirements while preserving continuous weekly scheduling.

---

## Seasonal Content

Holiday programming should only occupy storage when it is likely to air.

Examples:

October

- Halloween Specials
- Halloween Commercials

November

- Thanksgiving Programming

December

- Christmas Specials
- Christmas Commercials

After each season ends, these assets may be automatically removed until needed again.

---

## Commercial Rotation

Commercial campaigns should follow the same download strategy.

Examples:

- Christmas advertising
- Summer promotions
- Back-to-school campaigns

Only active campaigns should remain locally stored.

---

## Intelligent Download Priorities

Every media item should eventually receive a scheduling priority score that determines whether it should remain downloaded.

Possible factors include:

- Broadcast frequency
- Seasonal relevance
- IMDb or community rating
- User preferences
- Storage limitations
- Historical usage
- Upcoming schedule requirements

Rather than relying solely on ratings, VISTOR should prioritize content based upon how likely it is to appear in future broadcasts.

---

## Long-Term Goal

The objective is for VISTOR to feel like it owns an enormous television library while only storing the content most relevant to upcoming broadcasts.

This allows VISTOR to scale efficiently to thousands of media items without requiring enterprise-level storage.

## Future Idea: Dynamic Broadcast Interruptions

VISTOR may eventually support dynamic broadcast interruptions that simulate how real television networks could override scheduled programming for major events.

These interruptions should not be treated as changes to the currently airing program. Instead, they should exist as independent Broadcast Events that temporarily override normal playback and allow the original programming to resume afterward.

Possible broadcast interruptions include:

- Breaking News
- Emergency Alert System (EAS)
- Severe Weather Alerts
- Presidential Addresses
- Live Event Overrides
- Special Announcements

Example behavior:

Scheduled Programming

Episode

↓

Broadcast Interruption:

Breaking News Segment

↓

Resume Original Programming


The scheduler should maintain the original state of the channel while the Broadcast Controller temporarily inserts the interruption.

The currently airing program should not restart after an interruption. Playback should resume from the correct position as if the viewer had been watching a real television broadcast.


## User Configuration

Because some viewers may prefer uninterrupted playback, VISTOR should provide settings that control broadcast interruptions.

Possible settings:

Broadcast Settings

Enable Breaking News:
On / Off

Enable Emergency Alerts:
On / Off

Enable Weather Interruptions:
On / Off

Enable Special Broadcast Events:
On / Off


## Interruption Modes

Future versions may support different interruption behaviors.


### Historical Mode

Uses preserved historical broadcast interruptions when available.

Example:

CNN

Normal Programming

↓

Historical Breaking News Coverage

↓

Resume Programming


### Generated Mode

Creates simulated broadcast interruptions based on configurable events.

Example:

Breaking News:

Severe Weather Warning


### Disabled Mode

No broadcast interruptions occur.

Channels continue normal scheduling without overrides.


## Architectural Consideration

Broadcast interruptions should be implemented as Broadcast Events rather than as media categories.

A Breaking News event is not a replacement for a News Segment. A News Segment represents a piece of content, while a Broadcast Event represents the decision to interrupt programming and insert content into an active channel.

This approach allows VISTOR to support:

- Authentic television behavior
- Historical broadcast recreation
- Optional interruptions
- Future emergency systems
- Live event overrides

without requiring changes to the playback engine.


This follows the core broadcast architecture:

Scheduling determines what should happen.

Broadcast Controller determines when interruptions occur.

Player determines how media is played.

## Resilient Acquisition and Replacement

Media availability on public archives is not guaranteed. An upload that
satisfies a scheduled program today may be removed tomorrow. VISTOR must
therefore treat every remote source as unreliable and be able to recover
from a takedown automatically rather than failing the broadcast.

### Multi-Archive Sources

Each media asset should carry a ranked list of remote sources rather than
a single origin. A source is a lightweight descriptor (provider, remote
identifier / URL). When a file is missing locally, VISTOR walks the ranked
sources in order and downloads from the first that responds. A removed page
simply returns an error (e.g. 404 / 403); the resolver treats that as
"source unavailable" and advances to the next source instead of crashing.

### Keyframe Fingerprints

Every asset VISTOR successfully obtains is fingerprinted from its keyframes
before it can ever be evicted. The fingerprint is small and is retained
permanently even after the underlying file is deleted. When all known
sources for an asset fail, VISTOR uses the stored fingerprint to search
across multiple archives for a matching re-upload of the same content, so a
takedown does not permanently lose the ability to reacquire the file.

### Relevant-Media Substitution

If no acceptable match can be found for a specific missing item (for example
the next episode of a series is genuinely unavailable from every source),
VISTOR does not leave a gap. Instead it substitutes a different piece of
relevant media so the broadcast continues uninterrupted, and re-queues the
missing item for a later acquisition attempt. There is no low-quality
"cold storage" copy of the file; only the permanent fingerprint and metadata
are kept, which is enough to find and restore a full-quality replacement.

### Two Independent Scores

VISTOR maintains two deliberately separate scores per media item:

1. Broadcast Score — how likely the item is to air. Driven by repurposability
   (applicable to more channels scores higher), non-seasonal content sitting
   in a higher bracket than seasonal, and overall appeal. This score alone
   drives broadcast frequency / selection for streaming.

2. Retention Score — whether the file should stay on disk. This is a combined
   score derived from the Broadcast Score, the "at-risk" fragility of the
   item's sources (scarce or unreliable sources raise retention priority),
   and the storage footprint the file occupies (larger files are more
   expensive to keep). This score alone drives disk eviction decisions.

The scores are kept separate because a frequently-aired item on a rock-solid,
widely-mirrored source may not need aggressive on-disk pinning, while a
medium-frequency item that survives on a single fragile upload should be
pinned. Collapsing them into one number would lose this distinction.

### Deleted-Content Metadata Retention

Deleting a file never deletes its metadata or its fingerprint. The metadata
library remains the complete catalog regardless of what exists on disk, so a
previously-evicted item can always be reverse-searched (via fingerprint and
metadata) and reacquired when the schedule needs it again.

### Catalogue Expansion (Future)

The discovery service described above operates over the *known* metadata
catalog: it can only select and acquire items VISTOR already knows about.
A true "find a show I have never catalogued" capability is a separate,
later feature that requires a metadata-ingest step first: querying an
external source, parsing series/episode metadata, and inserting new
MediaItems into the Library before any acquisition can target them.

This is intentionally deferred until the core program is complete. The
buildable, testable core today is: (1) a provider-agnostic fetcher that
can pull from any backend (Internet Archive, YouTube, Smithsonian, etc.),
(2) a rolling acquisition loop that keeps the window filled and evicts
aired content, and (3) channel-spec discovery over the existing catalog.
Catalogue expansion layers on top of these once metadata ingest exists.

## Recommended Media (Automatic Catalogue Expansion)

VISTOR should eventually be able to grow its own catalogue rather than
relying entirely on manual ingest through the drag-and-drop web UI. When
enabled, VISTOR would use an existing catalogued item as a seed, ask an
authoritative source (TMDB "recommendations"/"similar", IMDb) for related
titles, and surface them as suggestions for new programming.

This builds directly on the existing RecordBuilder -> TMDBSource ->
MediaIngestor seam and is the concrete first slice of the "Catalogue
Expansion (Future)" item already noted at the end of this document.

### Pipeline

1. Seed selection - pick a catalogued MediaItem (or a whole channel spec)
   to base recommendations on.
2. Suggestion - query TMDB/IMDb for similar/recommended titles and build
   provisional metadata records (no asset yet).
3. Source discovery - for each accepted suggestion, search public archives
   (YouTube, Internet Archive, etc.) for a suitable URL, reusing the ranked
   multi-archive source model.
4. Acquisition - download, probe, and fingerprint via the normal ingest
   pipeline, then commit into media.json.

### Autonomy Levels

Because fully-automatic URL discovery is risky, the feature should ship in
graduated modes:

- Suggest Only - recommendations appear in a queue; nothing is downloaded
  until a human confirms (same confirm step as the web UI today).
- Assisted - VISTOR finds candidate URLs automatically but still waits for
  confirmation before committing.
- Automatic - VISTOR discovers a URL, ingests, and commits with no
  interaction, feeding new similar shows straight into broadcasts.

### Possible Settings

Recommended Media:
On / Off

Recommendation Mode:
Suggest Only / Assisted / Automatic

Seed Source:
Whole Library / Per Channel / Specific Titles

Max Auto-Additions Per Week:
(numeric limit)

### Relationship to the Management Website and TV Settings Menu

These toggles are part of a larger planned management surface. Two distinct
front-ends are envisioned:

- Management Website - a full system console (separate from add_media_web)
  for editing every setting, including commercial-playback rules from the
  Design Bible and the Recommended Media toggles above.
- TV Settings Menu - the same settings viewable/toggleable on the
  television itself, mapped to a dedicated remote button, so the operator
  never needs a keyboard. A future USB mode could let the TV ingest media
  directly from a plugged-in drive of supported file types.

The ingest/authoring surfaces remain separate from the TV-viewing runtime,
consistent with how src/ingest is already documented as "NOT part of the
TV-viewing runtime."

### Deferral Note

Full automation depends on reliable source discovery and a real settings/
config persistence layer (the current Config.load() is a placeholder). The
first buildable slice is Suggest Only over the known TMDB "recommendations"
endpoint, with a persisted `recommended_media` toggle.

---

## Coexisting with Jellyfin (Streaming Mode Alongside Cable Mode)

VISTOR and a media server such as Jellyfin could run side-by-side on the same
Raspberry Pi, pointed at the same downloaded media, giving the operator two
front-ends over the same bytes: traditional "always airing" cable television
through VISTOR, and on-demand "streaming mode" browsing through Jellyfin.

Both would run as separate processes with no shared runtime - just a shared
folder. Jellyfin would be pointed at the same `Media/` tree that VISTOR
resolves through `Paths.get_media_directory()` (`src/core/paths.py`). There is
no code-level conflict in two processes *reading* the same files; every
friction below comes from VISTOR *writing and deleting* within that tree.

### Problem 1 - Retention-driven eviction deletes files out from under Jellyfin

VISTOR's rolling cache (`evict_to_budget` in
`src/metadata/services/rolling_cache.py`) intentionally keeps only a small
resident window of upcoming episodes and evicts already-aired ones to stay
within the storage budget. Jellyfin assumes a stable, always-present library,
so any evicted episode would simply show as missing/unavailable there.
Eviction is non-destructive to *metadata* - it flips `download_status` to
MISSING and preserves the sidecar/fingerprint for re-fetch - but the playable
file Jellyfin needs is gone.

Solution: either set the storage budget to `0` (unbounded) so window-based
eviction never fires - at the cost of the #1/#2 disk-management behavior - or
accept that Jellyfin only reliably sees VISTOR's currently-resident window
rather than the full catalog.

### Problem 2 - File naming is VISTOR-shaped, not Jellyfin-shaped

Files are named by internal media id via `RecordBuilder._path_for`
(`src/metadata/services/record_builder.py`), e.g. `Media/<folder>/<media_id>.mkv`,
rather than Jellyfin's expected `Show Name/Season 01/Show Name - S01E02`
convention. Jellyfin's scanner and metadata agents rely on filename/folder
conventions to identify content, so pointing it at VISTOR's tree yields a
poorly-identified library. VISTOR's own `<file>.vistor.json` sidecars
(`src/metadata/services/asset_sidecar.py`) are a VISTOR-specific format that
Jellyfin cannot read.

Solution: treat the tree as a "mixed / home videos" library in Jellyfin, or add
an `.nfo`-generation bridge step that translates VISTOR metadata into a format
Jellyfin's agents understand.

### Problem 3 - Conceptually opposite models

VISTOR is a broadcast simulator ("watch what's airing"); Jellyfin is a library
browser ("browse and pick"), which is an explicit VISTOR non-goal. This is not
a technical conflict but a UX one: the two front-ends behave differently over
the same media, which is exactly the point of this setup.

Solution / guardrails: decide who owns deletion (VISTOR's eviction vs. a stable
Jellyfin library), and consider pointing Jellyfin at a curated subset rather
than the whole `Media/` tree so VISTOR's `Raw/`, `tmp/`, and sidecar files do
not clutter the Jellyfin library.

### Deferral Note

This is an optional deployment/integration idea, not a core roadmap item. It
becomes cleanly viable once the storage-budget setting (#2) is respected
everywhere and a naming/`.nfo` bridge exists; until then the safest
configuration is an unbounded budget plus a curated Jellyfin library subset.
