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