# VISTOR Roadmap

**Project Status:** Pre-Alpha

**Current Version:** 0.3.0

**Last Updated:** July 25, 2026

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

**Phase 3 — Media Library**

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

## Milestone

VISTOR has a complete project structure and is ready for software development.

---

# Phase 1.5 — Core Application Foundation

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

## Runtime Engine

## Runtime Engine

- [x] Implement engine update loop
- [x] Add engine state management
- [x] Add graceful runtime shutdown
- [ ] Build engine timing system
- [ ] Integrate channel manager
- [ ] Integrate media player
- [ ] Integrate scheduler
- [ ] Integrate weather service
- [ ] Integrate on-screen display (OSD)
- [ ] Integrate remote input system

## Core Infrastructure

- [ ] Create application configuration manager
- [ ] Implement centralized logging
- [ ] Create reusable path utilities
- [ ] Create basic exception handling framework

---

## Milestone

VISTOR successfully launches as an application and establishes the foundation upon which all future systems will be built.

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

- [ ] Channel Banner
- [ ] Program Information
- [ ] Volume Indicator
- [ ] Mute Indicator
- [ ] Clock
- [ ] Fade Animations

---

## TV Guide

- [ ] Guide Layout
- [ ] Current Program
- [ ] Upcoming Program
- [ ] Time Display
- [ ] Navigation

---

## Milestone

VISTOR provides an authentic cable television user interface.

---

# Phase 6 — Broadcast Experience
  
## Media Acquisition  
  
### Programming  
  
- [ ] Television Shows  
- [ ] Movies  
- [ ] Sports  
- [ ] News  
- [ ] Documentaries  
- [ ] Game Shows  
- [ ] Talk Shows  
  
### Supporting Content  
  
- [ ] Commercials  
- [ ] Station IDs  
- [ ] Network Promos  
- [ ] Music Videos  
- [ ] Infomercials  
- [ ] Ambient Loops  
  
---  

## Channels

- [ ] Cartoon Network
- [ ] Nickelodeon
- [ ] Movie Channel
- [ ] Music Video Channel
- [ ] Sports Channel
- [ ] News Channel
- [ ] Weather Channel
- [ ] Aquarium Channel
- [ ] Fireplace Channel
- [ ] Infomercial Channel

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

VISTOR delivers a believable television broadcast experience.

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

- Multiple fictional cable providers
- Additional regional channel lineups
- Premium movie packages
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

# Definition of Success

VISTOR Version 1.0 will be considered complete when:

- It operates as a dedicated cable box.
- Channels continue playing whether they are being watched or not.
- Programming schedules feel authentic.
- Commercials are inserted naturally.
- Seasonal programming behaves automatically.
- The system boots directly into VISTOR.
- Navigation is performed using a standard television remote.
- The experience faithfully recreates late-1990s and early-2000s cable television.

The objective is not simply to build software.

The objective is to recreate the feeling of sitting in front of a CRT television and watching cable television as it existed before the era of streaming.

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