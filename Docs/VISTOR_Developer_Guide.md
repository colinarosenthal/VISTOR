# VISTOR Developer Guide

**Version:** 0.2.0

**Last Updated:** July 24, 2026

---

# Purpose

The VISTOR Developer Guide serves as the primary technical reference for contributors.

Unlike the Design Bible, which defines the vision and philosophy of VISTOR, the Developer Guide explains how the software is organized, how its systems interact, and how new functionality should be implemented.

This document is intended to ensure that every contributor develops VISTOR consistently while preserving the project's architecture.

---

# Intended Audience

This guide is intended for:

- Core developers
- Contributors
- Future maintainers
- Anyone wishing to understand VISTOR's internal architecture

---

# Development Philosophy

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

# Coding Standards

## Formatting

- Follow PEP 8.
- Use descriptive variable names.
- Avoid unnecessary abbreviations.
- Keep methods focused on a single responsibility.

---

## Documentation

Every public class and method should contain a docstring.

Complex logic should include comments explaining *why* something is being done rather than *what* the code is doing.

---

## Architecture

Subsystems should communicate through exposed methods.

Avoid directly modifying another subsystem's internal state.

When possible:

```
Subsystem A
        ↓
Public Interface
        ↓
Subsystem B
```

instead of

```
Subsystem A
        ↓
Internal Variables
        ↓
Subsystem B
```

---

## Dependencies

Dependencies should always point downward through the architecture.

For example:

```
Engine
    ↓
Scheduler
    ↓
Schedule
    ↓
Programming Block
```

Not:

```
Programming Block
        ↓
Engine
```

Lower-level systems should never depend upon higher-level systems.

---

# Project Architecture

The following sections describe every folder, subsystem, and major source file within VISTOR.

As development continues, this section will expand into a complete architectural reference.

---

# Source Tree

```
src/

core/
engine/
scheduler/
metadata/
player/
channel/
remote/
osd/
weather/
guide/
utilities/
```

---

# Core

The Core package contains systems required by every other subsystem.

Nothing inside Core should depend upon higher-level components.

## application.py

### Purpose

Coordinates application startup and shutdown.

### Responsibilities

- Initialize subsystems
- Start the engine
- Shutdown gracefully

---

## clock.py

### Purpose

Provides all runtime date and time information.

### Responsibilities

- Maintain current time
- Detect weekdays/weekends
- Detect holidays
- Determine schedule type

Clock is the authoritative source for all time-based behavior.

---

## config.py

### Purpose

Loads application configuration.

---

## logger.py

### Purpose

Provides centralized application logging.

---

## paths.py

### Purpose

Maintains project-relative filesystem paths.

---

## version.py

### Purpose

Stores application version information.

---

# Engine

The Engine coordinates runtime execution.

Every runtime subsystem is owned by the Engine.

Future responsibilities include:

- Clock
- Scheduler
- Metadata Engine
- Channel Manager
- Player
- OSD
- Weather
- Remote Input

The Engine should coordinate systems rather than perform subsystem logic itself.

---

# Scheduler

The Scheduler determines what programming should currently be broadcasting.

Responsibilities include:

- Selecting schedules
- Selecting programming blocks
- Providing broadcast timing information

The Scheduler never controls playback.

---

## scheduler.py

Coordinates schedule selection.

---

## schedule_loader.py

Loads available schedules.

---

## schedule.py

Represents one broadcast schedule.

---

## programming_block.py

Represents one scheduled time block.

---

## schedule_type.py

Defines all supported schedule types.

---

# Metadata

The Metadata subsystem determines what media exists.

Responsibilities include:

- Loading metadata
- Organizing media
- Providing searchable media information

The Metadata subsystem should never determine *when* media is played.

That responsibility belongs exclusively to the Scheduler.

---

# Player

The Player controls media playback.

Responsibilities include:

- Starting playback
- Stopping playback
- Resuming playback
- Channel switching

The Player should never determine scheduling.

---

# Channel Manager

Maintains all television channels.

Responsibilities include:

- Channel definitions
- Channel numbering
- Previous channel
- Active channel

---

# OSD

Responsible for all temporary on-screen overlays.

Examples include:

- Channel banner
- Program information
- Volume indicator
- Clock
- TV Guide

---

# Weather

Responsible for weather retrieval and forecast generation.

This subsystem should remain independent of the Scheduler.

---

# Remote

Processes remote-control input.

Responsibilities include:

- IR input
- Keyboard input during development
- Button mapping

---

# Guide

Provides television guide information.

The Guide consumes scheduling information but never creates schedules.

---

# Dependency Overview

The intended architecture is:

```
Application
        ↓
Engine
        ↓
Clock
Scheduler
Metadata
Player
Channel Manager
Guide
Weather
OSD
Remote
```

Example scheduling flow:

```
Clock
        ↓
Scheduler
        ↓
Schedule
        ↓
Programming Block
        ↓
Player
```

Example media flow:

```
Metadata Engine
        ↓
Media Library
        ↓
Schedule Loader
        ↓
Scheduler
```

---

# Contribution Guidelines

Before implementing new functionality:

1. Determine which subsystem owns the responsibility.
2. Avoid crossing subsystem boundaries.
3. Preserve modularity.
4. Update documentation when architecture changes.
5. Test the subsystem independently before integration.

---

# Future Expansion

This guide will eventually include:

- Complete file reference
- Class reference
- Module reference
- Data flow diagrams
- Lifecycle diagrams
- Initialization sequence
- Runtime sequence
- Metadata format specification
- Schedule format specification
- Coding examples
- Testing procedures
- Release workflow

# 4. Metadata Architecture

## Purpose

The metadata package defines the data model used throughout VISTOR.

Rather than storing metadata as unrelated JSON documents, VISTOR models every broadcast asset as a structured object with clearly defined relationships.

The metadata system is intentionally divided into four independent layers:

- Enums
- Vocabulary
- Models
- Metadata Services

This separation minimizes duplication, improves maintainability, and allows the metadata library to grow without requiring architectural changes.

---

## Package Structure

```text
metadata/
│
├── __init__.py
│
├── enums/
│   ├── audience.py
│   ├── commercial_type.py
│   ├── content_rating.py
│   ├── media_type.py
│   ├── presentation_type.py
│   └── role_type.py
│
├── vocabulary/
│   ├── country.py
│   ├── genre.py
│   ├── music_genre.py
│   ├── network.py
│   ├── tag.py
│   └── theme.py
│
├── models/
│   ├── media_item.py
│   ├── media_asset.py
│   ├── person.py
│   ├── appearance.py
│   ├── franchise.py
│   ├── series.py
│   ├── season.py
│   ├── episode.py
│   ├── movie.py
│   ├── commercial.py
│   ├── advertiser.py
│   ├── campaign.py
│   ├── product.py
│   ├── music_video.py
│   ├── sports_event.py
│   ├── news_segment.py
│   ├── weather_segment.py
│   ├── documentary.py
│   ├── station_id.py
│   ├── promo.py
│   ├── ambient.py
│   └── media_library.py
│
├── metadata_loader.py
├── metadata_library.py
├── metadata_search.py
├── metadata_serializer.py
└── metadata_validator.py
```

---

## Enums

Enums define architectural concepts.

These represent fixed classifications used throughout the application.

Because these values define application behavior rather than descriptive metadata, they should remain relatively stable over the lifetime of the project.

Examples include:

- Media Type
- Presentation Type
- Audience
- Content Rating
- Commercial Type
- Role Type

---

## Vocabulary

Vocabulary contains standardized descriptive values.

Unlike Enums, vocabulary collections are expected to expand as additional media is added to the library.

Examples include:

- Genres
- Music Genres
- Themes
- Networks
- Countries
- Tags

Using standardized vocabulary prevents inconsistent metadata while allowing the media library to continue growing.

---

## Models

Models describe media and the relationships between media.

Every broadcast asset is built upon a common Media Item model.

Specialized media models extend Media Item and provide only the metadata unique to that media type.

Supporting models eliminate duplication by representing shared entities such as:

- Series
- Seasons
- Advertisers
- Campaigns
- Products
- People
- Franchises

Relationships between people and media are represented through the Appearance model, allowing a single person to participate in any type of media while performing different roles.

---

## Metadata Services

Metadata Services provide the functionality required to operate the metadata system.

These services are responsible for:

- Loading metadata
- Validating metadata
- Searching metadata
- Managing the metadata library
- Serializing metadata

Keeping these responsibilities separate from the metadata models allows the metadata engine to evolve independently of the data itself.

---

## Design Philosophy

Every broadcast asset should be treated uniformly before being treated uniquely.

All media share a common metadata foundation through Media Item.

Individual media types extend this shared foundation only where necessary.

This minimizes duplicated code while allowing VISTOR to support television episodes, movies, commercials, music videos, sports broadcasts, news programming, station IDs, promos, documentaries, weather programming, and future media types using a single consistent architecture.