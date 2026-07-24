# VISTOR Design Bible

**Project Version:** 1.0

**Last Updated:** 7/23/2026

---

# 1. Project Vision

VISTOR is a software project designed to recreate the experience of watching cable television during the late 1990s and early 2000s.

Rather than functioning as a modern media player or streaming platform, VISTOR simulates a complete cable television ecosystem. Channels continuously broadcast scheduled programming, commercials, station identifications, promotional material, and special events. Every channel exists independently and continues playing regardless of whether it is currently being viewed.

---

# 1.1 Project Motivation

VISTOR is not intended to reject modern streaming. It exists to preserve and reintroduce the unique cultural experience of scheduled broadcast television—an experience built on anticipation, discovery, and shared moments that cannot be replicated by on-demand media.

---

# 1.2 The Name "VISTOR"

Choosing a name for the project became part of the design process itself.

Early in development, the working title *RetroTV* accurately communicated the project's purpose, but they lacked a distinct identity. As the project's vision matured beyond recreating old television and toward preserving an entire broadcast experience, it became clear that the project required a name that could stand on its own rather than simply describe its function.

The search for that identity drew inspiration from the naming conventions of classic consumer electronics manufacturers from the latter half of the twentieth century. Companies such as Sony, Aiwa, Denon, Pioneer, Grundig, Zenith, and Marantz became recognizable not because their names described televisions or audio equipment, but because decades of engineering excellence gave those names meaning.

Many of these names are short, memorable, and phonetically distinctive. They feel familiar without being descriptive, allowing the company's reputation—not the literal meaning of its name—to define its identity.

Rather than referencing nostalgia directly, the name is intended to feel like the name of a real electronics manufacturer that might have produced televisions, cable receivers, or professional broadcast equipment during the 1980s and 1990s. The goal was not to invent a fictional company for the sake of world-building, but to create a brand identity that naturally belongs within the era VISTOR seeks to preserve.

Throughout the project, VISTOR is treated as though it were an established manufacturer whose products quietly became part of millions of homes. The software is presented as a modern continuation of that legacy—a contemporary broadcast receiver built around the same philosophy of reliability, simplicity, and respect for the television experience.

In this way, the name VISTOR represents more than the software itself. It reflects the project's broader objective: preserving not only the content of broadcast television, but the feeling of interacting with the hardware, branding, and engineering culture that once surrounded it.

# 1.3 Broadcast Simulation Philosophy

## Core Principle

VISTOR does not simulate media playback.

VISTOR simulates television broadcasting.

The goal is not simply to play episodes, movies, or commercials. The goal is to recreate the behavior of a real television network, where programming is continuously scheduled, interrupted, resumed, and transitioned exactly as it would be on a broadcast station.

Every subsystem should be designed with this philosophy in mind.

---

## Broadcast Events

Programs are never interrupted directly by the player.

Instead, interruptions are represented as **Broadcast Events**.

Examples include:

- Commercial Blocks
- Station Identification
- Network Promos
- Local Affiliate Promos
- Weather Bulletins
- Emergency Alert System (EAS)
- Breaking News Interruptions
- Holiday Bumpers
- Rating Screens
- "We'll Be Right Back" Screens
- Countdown Timers
- Future Broadcast Types

Every interruption is treated as the same type of object within the broadcast pipeline.

---

## Broadcast Pipeline

The playback pipeline should remain separated into independent responsibilities.

```
Engine
    │
    ▼
Scheduler
    │
    ▼
Broadcast Controller
    │
    ▼
Playback Queue
    │
    ▼
Player
```

Responsibilities:

- **Engine** controls application runtime.
- **Scheduler** determines what should be airing.
- **Broadcast Controller** determines when interruptions occur.
- **Playback Queue** manages the ordered sequence of media.
- **Player** only plays the next queued media item.

The Player should never make scheduling decisions.

---

## Broadcast Modes

Version 1.0 will support multiple broadcast behaviors.

### Off

No interruptions.

```
Episode
Episode
Movie
```

---

### Between Programs

Commercial blocks occur only between completed programs.

```
Episode
Commercial Block
Episode
Commercial Block
Movie
```

---

### Mid-Program

Preferred broadcast mode.

Whenever broadcast metadata exists, commercial breaks should occur at their original broadcast timestamps.

Example:

```
Episode
    Break @ 09:14

Commercial Block

Resume Episode
```

If authentic breakpoint metadata is unavailable, VISTOR should generate breakpoints based on runtime.

---

## Future Expansion

The broadcast architecture should allow additional event types without redesigning the playback system.

Possible future broadcast events include:

- Local News Cut-Ins
- Severe Weather Interruptions
- Live Event Overrides
- Seasonal Network Branding
- Election Coverage
- Community-Created Broadcast Metadata
- Regional Affiliate Differences

The broadcast pipeline should remain flexible enough that any future event can be inserted without modifying the Player itself.

---

## Design Rule

Scheduling determines **what** should happen.

Broadcast Controller determines **when** interruptions occur.

Player determines **how** media is played.

Each subsystem should have a single responsibility and should not assume the responsibilities of another subsystem.

# 2. Project Goals

VISTOR aims to recreate the atmosphere of television as it existed before on-demand streaming became the standard.

The software should emphasize authenticity, simplicity, and nostalgia over modern convenience.

Primary goals include:

- Persistent television channels.
- Authentic (end of episode) commercial breaks.
- Historically appropriate programming.
- Cable-box style user interface.
- Local-first media storage.
- Reliable Raspberry Pi deployment.
- Expandable architecture for future channels and features.

---

# 3. Core Philosophy

VISTOR follows several guiding principles.

## 3.1 Television, Not Streaming

VISTOR is designed to simulate television.

Users do not browse a library.

Users watch whatever is currently airing.

---

## 3.2 Channels Never Stop

Every channel always exists.

Every channel always has a schedule.

Changing channels never restarts playback.

If a user leaves a channel for ten minutes, that channel should progress ten minutes while unattended.

---

## 3.3 Media Exists Independently

Shows, movies, commercials, music videos, and other content exist independently of channels.

Channels reference media.

Media does not belong to channels.

A single episode may appear on multiple channels without duplication.

---

## 3.4 Local First

Whenever possible, all media should be stored locally.

Internet access should be optional.

The only planned exception is live weather data used by the Weather Channel.

---

## 3.5 Relative Paths

No file paths should ever be hardcoded.

Every component of VISTOR should function correctly regardless of where the VISTOR project folder is stored.

---

## 3.6 Raspberry Pi Production Target

Development will occur primarily on Windows.

The final production system will operate on a Raspberry Pi connected to a CRT television.

The Raspberry Pi becomes the dedicated cable box.

---

## 3.7 Planned Channel Types

VISTOR is designed to support a wide variety of cable television channels inspired by the late 1990s and early 2000s.

Planned channel categories include:

- Cartoon channels
- Movie channels
- Music video channels
- Sports channels
- News channels
- Documentary channels
- Children's programming
- Classic television
- Late-night infomercial channels
- Aquarium channels
- Fireplace and ambient channels
- Public access style channels
- The Weather Channel
- Seasonal and holiday channels
- Experimental or custom channels

Each channel should maintain its own identity through programming, commercial selection, promotional material, station branding, and scheduling.

---

## 3.8 Cable Box Experience

VISTOR should behave like a dedicated cable box rather than a computer application.

The viewer should primarily interact with the system using a standard infrared television remote.

Planned remote functionality includes:

- Channel Up
- Channel Down
- Numeric channel entry
- Previous Channel (Last)
- Volume adjustment
- Mute
- Program Information
- Television Guide

On-screen overlays should closely resemble cable boxes from the late 1990s and early 2000s.

Typical overlays include:

- Channel number
- Channel name
- Current program
- Volume indicator
- Mute indicator
- Clock
- Program information banner

---

## 3.9 Authentic Scheduling

Programming should follow realistic broadcast schedules rather than random playback.

Examples include:

- Scheduled programming blocks
- Commercial breaks
- Station identifications
- Network promotions
- "Coming Up Next" bumpers
- Holiday programming
- Weekend marathons
- Late-night programming
- Seasonal events

The scheduler should create the illusion of an active television network operating continuously.

---

## 3.10 Weather Channel

VISTOR includes a dedicated Weather Channel inspired by the presentation style of The Weather Channel during the late 1990s and early 2000s.

Unlike other channels, this channel may retrieve live weather information from the internet.

The presentation should remain period appropriate while displaying:

- Current conditions
- Local forecast
- Extended forecast
- Radar imagery
- Weather maps
- Local time
- Characteristic background music
- Classic broadcast graphics

Internet connectivity should enhance this channel without becoming a requirement for the remainder of the system.

---

## 3.11 Portability

VISTOR should function as a completely portable project.

The project directory should be movable without requiring configuration changes.

Supported storage locations include:

- Internal SSD
- External USB SSD
- Windows development computer
- Raspberry Pi storage

Every component of the project should determine its location relative to the VISTOR project root.

Hardcoded paths should never be used.

---

## 3.12 Media Organization

Media should be organized according to its broadcast purpose rather than the television channel on which it appears.

For example, a television series may appear on multiple channels without requiring duplicate copies of the media.

Commercials, movies, music videos, ambient programming, and television shows should each exist independently within the media library.

Channels reference this content through configuration rather than ownership.

This approach minimizes duplication while allowing maximum scheduling flexibility.

---

## 3.13 Seasonal and Special Event Programming

VISTOR should support dynamic programming based on the time of year.

Rather than remaining static throughout the calendar year, channels should be capable of temporarily adjusting their schedules to recreate the seasonal programming commonly found on cable television.

Examples include:

### Halloween

- Horror movie marathons
- Halloween television episodes
- Spooky cartoon specials
- Halloween-themed commercials
- Seasonal station bumpers
- Halloween music videos
- Special event graphics

---

### Thanksgiving

- Family movies
- Charlie Brown specials
- Thanksgiving-themed television episodes
- Holiday commercials

---

### Christmas

- Twenty-four hour Christmas movie marathons
- Classic Christmas specials
- Holiday music channels
- Christmas commercials
- Seasonal station branding
- Fireplace channels
- Snow ambience channels

---

### New Year's

- Countdown specials
- Music celebrations
- Fireworks programming
- Year-end retrospectives

---

### Summer

- Summer movie events
- Beach programming
- Vacation-themed commercials

---

### Sporting Events

VISTOR may also support temporary programming associated with major sporting events including:

- Super Bowl weekend
- Olympics
- NCAA tournaments
- World Series
- Stanley Cup Finals

---

Seasonal programming should feel like a real cable provider modifying existing schedules rather than creating entirely separate television systems.

Whenever possible, existing channels should temporarily adopt seasonal programming blocks while maintaining their original identity.

## 3.14 Metadata System

VISTOR separates media from its descriptive information.

Metadata should be stored independently of the media files themselves.

Metadata may include:

- Title
- Episode
- Season
- Original network
- Original air date
- Runtime
- Genre
- Tags
- Preferred channels
- Commercial preferences
- Scheduling information

The metadata system should allow the scheduler to build realistic television lineups without depending on folder structure.

---

# 5. Planned System Architecture

VISTOR is divided into several independent components.

Each component is responsible for a specific aspect of the cable television experience.

## Channel Engine

Responsible for:

- Channel schedules
- Playback timing
- Program progression
- Commercial insertion
- Schedule generation

---

## Player

Responsible for:

- Media playback
- Switching channels
- Audio output
- Maintaining playback state

Changing channels should never restart programming.

---

## Remote Handler

Responsible for:

- Infrared receiver input
- Keyboard controls during development
- Mapping remote buttons to VISTOR functions

---

## OSD Manager

Responsible for displaying temporary overlays including:

- Channel number
- Channel name
- Program title
- Volume
- Mute
- Clock
- Guide information

The OSD should resemble period-correct cable television equipment.

---

## Metadata Engine

Responsible for:

- Reading metadata
- Organizing programming
- Providing information to the scheduler
- Tracking shows, movies, commercials, and promotions

---

# 6. Inspiration

VISTOR is an original software project.

The initial inspiration came from the open-source project FieldStation42, which demonstrated the concept of continuously broadcasting television channels that remain synchronized regardless of whether they are actively being viewed.

VISTOR adopts this broadcast philosophy as one of its core design principles.

Beyond this concept, VISTOR is designed as an independent system with its own architecture, goals, and implementation.

Major systems unique to VISTOR include:

- Modular software architecture
- Metadata-driven media organization
- Cable-box style on-screen display
- Infrared remote integration
- Raspberry Pi appliance deployment
- Live Weather Channel generation
- Seasonal broadcast events
- Dynamic commercial scheduling
- Television guide
- Relative-path project structure
- Expandable channel framework

While FieldStation42 helped inspire the original idea, VISTOR is not intended to be a modification, fork, or reimplementation of that project.

Instead, it is an original project that shares the underlying philosophy of persistent television broadcasting while pursuing its own vision of recreating the complete cable television experience.

---

# 8. Project Scope

VISTOR is intended to faithfully recreate the experience of watching American cable television during the late 1990s and early 2000s.

Historical authenticity should always take priority over adding modern conveniences or unnecessary features.

Whenever multiple design decisions are possible, preference should be given to the option that better recreates the atmosphere and behavior of period-correct cable television.

The project is intended to simulate an entire cable television ecosystem rather than simply providing access to a collection of media files.

---

# 9. Non-Goals

VISTOR is intentionally not designed to become a modern media platform.

The project is **not** intended to function as:

- A streaming service
- A Plex replacement
- A DVR
- A media server
- A smart television interface
- A movie library browser
- A video editor
- A home theater management system

The objective is to recreate the experience of cable television rather than improve upon it with modern conveniences.

---

# 10. Broadcast Standards

Every broadcast should appear intentional.

Programming should feel professionally scheduled rather than randomly assembled.

Whenever possible:

- Episodes should air in logical order.
- Commercial breaks should occur naturally.
- Station IDs should appear periodically.
- Network promotions should advertise upcoming programming.
- Time-of-day scheduling should resemble real television.
- Weekends and holidays should feel different from weekdays.

The viewer should believe that every channel has been programmed by an actual television network.

---

# 11. Channel Standards

Every television channel should maintain its own identity.

Each channel configuration should eventually define:

- Channel number
- Channel name
- Channel logo
- Primary genre
- Target audience
- Programming sources
- Commercial pools
- Promotional material
- Broadcast schedule
- Station identification graphics
- Network branding

No two channels should feel identical.

Each should recreate the personality of a real cable network.

---

# 12. Commercial Philosophy

Commercials are considered an essential part of the VISTOR experience.

Rather than interrupting programming, commercials help establish the illusion of authentic television broadcasting.

Commercial selection should consider:

- Television network
- Program genre
- Intended audience
- Time of day
- Season
- Year
- Holiday events

Commercials should complement the surrounding programming whenever possible.

Late-night programming should naturally transition toward infomercials and direct-response advertising.

---

# 13. Audio Philosophy

VISTOR should preserve the original character of archived media whenever practical.

Minor imperfections contribute to authenticity.

Whenever possible:

- Preserve original stereo or mono mixes.
- Avoid unnecessary audio processing.
- Preserve original broadcast dynamics.
- Avoid excessive loudness normalization.
- Maintain consistent listening levels without sacrificing authenticity.

The objective is to recreate the sound of television rather than modern digital media.

---

# 14. Visual Philosophy

Visual presentation should remain faithful to the era being recreated.

Whenever practical:

- Preserve original aspect ratios.
- Avoid stretching 4:3 programming.
- Preserve original broadcast logos.
- Avoid unnecessary AI enhancement.
- Maintain period-appropriate graphics.
- Design VISTOR graphics to complement CRT displays.

Modern visual effects should only be used when they improve authenticity.

---

# 15. Metadata Standards

VISTOR separates media files from descriptive information.

Every media item should have corresponding metadata whenever practical.

Metadata may include:

- Title
- Episode
- Season
- Runtime
- Original network
- Original air date
- Genre
- Tags
- Preferred channels
- Commercial preferences
- Scheduling information

Folder structure should never determine scheduling behavior.

Metadata should remain human-readable and easily editable.

---

# 16. Configuration Philosophy

Configuration should always be preferred over hardcoded values.

Whenever practical:

- Channels should be created through configuration files.
- Schedules should be generated from configuration.
- Settings should remain editable without modifying source code.
- Future expansion should require minimal programming changes.

The project should remain flexible and maintainable as it grows.

---

# 17. Performance Goals

VISTOR is intended to operate as a dedicated appliance.

Target hardware includes:

- Raspberry Pi 5
- 8 GB RAM
- SSD storage
- CRT television

Performance objectives include:

- Automatic startup after boot.
- Stable long-term operation.
- Low CPU utilization.
- Efficient memory usage.
- Responsive channel changes.
- Reliable continuous playback.

The finished system should require little or no maintenance during normal operation.

---

# 18. Development Milestones

The project will be developed in incremental phases.

Major milestones currently include:

- Project foundation
- Media library organization
- Metadata system
- Channel scheduler
- Playback engine
- On-screen display
- Remote control integration
- Television guide
- Weather Channel
- Seasonal broadcast events
- Raspberry Pi deployment
- Version 1.0 release

Future milestones will be added as the project evolves.

---

# 19. Version History

The Design Bible should maintain a record of significant project changes.

Major architectural decisions should be documented here to preserve the project's history and reasoning.

---

# 20. Future Ideas

Ideas that fall outside the current development roadmap should be recorded rather than forgotten.

Possible future additions include:

- Emergency Alert System simulations
- Public access channels
- Cable outage simulations
- VHS tracking effects
- Static between channels
- Local bulletin board channel
- Interactive TV listings
- Multiple cable provider presets
- Regional station packages
- Alternate era presets

Recording future ideas helps maintain long-term direction without interrupting current development.

---

# 21. Cable Provider Philosophy

VISTOR should be approached as though it were an actual cable television provider rather than a software application.

Every design decision should reinforce the illusion that the viewer is connected to a professionally operated cable network.

Questions considered during development should include:

- Which channels does the provider carry?
- What channel numbers are assigned?
- How are premium channels organized?
- What station branding is used?
- What promotional material is broadcast?
- How are seasonal marathons scheduled?
- How do channels evolve throughout the year?
- What does the television guide display?

Thinking from the perspective of operating a cable provider helps ensure that every feature contributes toward a consistent and believable television experience.

---

# 22. Guiding Principle

Whenever uncertainty exists during development, one question should always be asked:

> **"Would this make the viewer believe they are watching real cable television?"**

If the answer is **yes**, the feature likely belongs in VISTOR.

If the answer is **no**, the design should be reconsidered.

This principle takes precedence over convenience, modern expectations, or technical simplicity.

VISTOR is not intended to imitate a media player.

VISTOR is intended to recreate the experience of television.

---

# 23. Media Sources and Rights

VISTOR is designed to work with media that the user has the legal right to use.

Potential media sources may include:

- Public domain works
- Internet Archive collections
- Personally created recordings
- Personal VHS or DVD backups where legally permitted
- Home videos
- Other legally obtained media

Internet Archive serves as one of the primary resources for locating historically significant television broadcasts, commercials, station identifications, and promotional material preserved by the community.

VISTOR itself does not distribute copyrighted media.

The project provides software for organizing and presenting media supplied by the user.

Users are responsible for ensuring that any media added to their VISTOR installation complies with the copyright laws applicable in their jurisdiction.

Whenever possible, original creators, preservation groups, and archival projects should be respected and credited.

The VISTOR project encourages responsible media preservation and supports organizations dedicated to preserving television history for future generations.

# Acknowledgements

VISTOR would not be possible without the efforts of countless individuals and organizations dedicated to preserving television history.

Special recognition is given to:

- The Internet Archive, for preserving historically significant broadcasts and media.
- Home media preservation communities.
- VHS preservation projects.
- Broadcast history enthusiasts.
- Open-source software contributors whose work has inspired ideas incorporated into VISTOR.

Their efforts help preserve a part of television history that might otherwise be lost.

---

# 24. Development Standards

## Naming Conventions

To maintain consistency throughout the VISTOR codebase, the following naming conventions shall be used unless a specific exception is documented.

### Directories

- Lowercase only
- Use `snake_case` when multiple words are required

Examples:

```text
src/
channel_configs/
game_shows/
```

### Python Modules

- `snake_case.py`

Examples:

```text
channel_manager.py
media_library.py
schedule_generator.py
weather_service.py
```

### Classes

- `PascalCase`

Examples:

```text
Application
ChannelManager
MediaLibrary
WeatherService
```

### Functions & Methods

- `snake_case`

Examples:

```text
load_configuration()
initialize_engine()
generate_schedule()
```

### Variables

- `snake_case`

Examples:

```text
current_channel
weather_data
media_library
```

### Constants

- `UPPER_CASE`

Examples:

```text
APP_NAME
VERSION
DEFAULT_CHANNEL
```

### Assets

Media assets should use lowercase filenames with underscores.

Examples:

```text
channel_logo.png
rain_window.mp4
startup_chime.wav
```

### Configuration Files

Configuration files should use lowercase names.

Examples:

```text
settings.json
channels.yaml
weather.json
```

## Component Lifecycle

Components should implement only the lifecycle methods they require.

When implemented, lifecycle methods should always appear in the following order:

1. initialize()
2. start()
3. stop()
4. shutdown()

Each method has a distinct responsibility:

- initialize() prepares the component.
- start() begins active operation.
- stop() halts active operation while preserving state.
- shutdown() releases resources and performs cleanup.