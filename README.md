## VISTOR

*Preserving the broadcast television experience of the late 1990s and early 2000s.*

---

## Overview

VISTOR is a preservation project designed to recreate the experience of cable television before the era of on-demand streaming.

Rather than functioning as a traditional media player, VISTOR simulates a complete broadcast ecosystem. Every channel operates independently on a continuous schedule, complete with television programming, commercials, station identifications, and network promotions. Channels continue broadcasting whether or not they are currently being watched, recreating the spontaneity, anticipation, and shared cultural experience of broadcast television.

Built with a local-first philosophy, VISTOR is designed to run on dedicated hardware such as a Raspberry Pi connected to a CRT television, transforming modern hardware into a self-contained cable box that faithfully recreates the atmosphere of late-1990s and early-2000s television.

---

## Vision

VISTOR is designed around one simple idea:

**Television, not streaming.**

Users do not browse a media library.

Users watch whatever is currently airing.

If a viewer changes channels and later returns, programming has continued exactly as if a real cable network had been broadcasting the entire time.

---

## Planned Features

### Persistent Channels

- Channels continuously broadcast in real time.
- Playback never resets when changing channels.
- Every channel maintains its own schedule independently.

### Authentic Programming

- Television series
- Movies
- Sports
- Music videos
- News broadcasts
- Infomercials
- Ambient channels
- Classic Weather Channel

### Commercial Breaks

Commercials are inserted naturally between programs using configurable scheduling rules.

Commercials, network promotions, and station identifications are selected according to the active channel, time of day, and season.

### Cable Box Interface

VISTOR recreates the appearance of a classic digital cable box.

Planned interface features include:

- Channel banner
- Program information
- Volume indicator
- Mute indicator
- Clock
- Television Guide
- Numeric channel entry
- Previous channel support

### Seasonal Programming

VISTOR supports automatic seasonal schedule changes.

Examples include:

- Halloween movie marathons
- Christmas specials
- Thanksgiving programming
- Summer programming
- Weekend events

### Raspberry Pi Deployment

The final production system is intended to operate as a dedicated cable box using:

- Raspberry Pi 5
- USB SSD
- CRT television
- Infrared remote control

---

## Project Structure

```
VISTOR/

Assets/
Cache/
ChannelConfigs/
src/
Config/
Docs/
Logs/
Media/
Metadata/
Schedules/

README.md
ROADMAP.md
CHANGELOG.md
requirements.txt
setup.ps1
```

---

## Project Documentation  
  
Additional documentation is located inside the **Docs** directory.  
  
- Design Bible (`VISTOR_Design_Bible.md`)  
- Developer Guide (`VISTOR_Developer_Guide.md`)  
- User Manual (`VISTOR_User_Manual.md`)  
- Technical Notes (`Technical_Notes.md`)  
- Hardware Guide (`Hardware.md`)  
- Ideas (`Ideas.md`)  
  
The roadmap and version history live at the repository root in `ROADMAP.md`  
and `CHANGELOG.md`.

---

## Development Status  
  
**Status:** Alpha — Version 0.8.1  
  
Phases 1 through 7 are implemented and exercised by the test suite (metadata  
engine, playback runtime, cable-box UI, intelligent content management, and the  
media acquisition/ingestion pipeline). Phase 8 (Broadcast Programming) is in  
progress. Weather remains the only reserved, unimplemented subsystem.

---

## Project Goals

- Authentic cable television experience
- Local-first media storage
- Modular architecture
- Portable installation
- Raspberry Pi compatibility
- Expandable channel system
- Long-term maintainability

---

## Media

VISTOR is designed to operate primarily using locally stored media.

Programming, commercials, movies, music videos, station IDs, and promotional material are intended to be organized independently of individual channels. Channels reference media through configuration and metadata rather than folder structure.

This allows the same content to appear on multiple channels without duplication.

---

## Licensing

VISTOR itself is an original open-source software project.

Users are responsible for obtaining and using media in accordance with applicable copyright laws and licensing agreements.

VISTOR does not distribute copyrighted television programming, commercials, movies, music videos, or other protected media.

---

## Inspiration

The scheduling philosophy behind VISTOR is inspired by projects such as **FieldStation42**, which demonstrated the appeal of continuously broadcasting television channels.

VISTOR is an original implementation with its own architecture, media organization, scheduling system, user interface, and long-term design goals.

---

## Contributing

Contributions, ideas, bug reports, and feature suggestions are welcome as the project matures.

Documentation, testing, and code improvements are all appreciated.

---

## Current Roadmap

The current development roadmap can be found in:

`ROADMAP.md`

---

## License  
  
VISTOR's source code is released under the terms in the `LICENSE` file at the  
repository root. VISTOR does not distribute copyrighted television programming,  
commercials, films, or music; users are responsible for obtaining and using  
media in accordance with applicable copyright law.

---

## Why VISTOR?

VISTOR is not intended to replace Plex, Jellyfin, Kodi, or other media center software.

Instead, it recreates the experience of traditional broadcast television.

Rather than choosing what to watch from a library, viewers experience continuously running channels complete with scheduled programming, commercial breaks, seasonal events, and classic cable-box interactions.

The emphasis is on recreating the atmosphere and unpredictability of television before the widespread adoption of on-demand streaming.