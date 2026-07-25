# VISTOR Developer Guide

**Version:** 0.2.0

**Last Updated:** July 24, 2026

---

# Purpose

The VISTOR Developer Guide serves as the primary technical reference for contributors.

Unlike the Design Bible, which defines the vision and philosophy of VISTOR, the Developer Guide explains how the software is organized, how its systems interact, and how new functionality should be implemented.

This document is intended to ensure that every contributor develops VISTOR consistently while preserving the project's architecture.

---

1. Introduction
    1.1 Purpose
    1.2 Intended Audience
    1.3 Development Philosophy

2. Coding Standards
    2.1 Formatting
    2.2 Documentation
    2.3 Architecture
    2.4 Dependencies

3. Core Architecture
    3.1 Source Tree
    3.2 Core
    3.3 Engine
    3.4 Scheduler
    3.5 Metadata
    3.6 Player
    3.7 Channel Manager
    3.8 OSD
    3.9 Weather
    3.10 Remote
    3.11 Guide

4. Metadata Architecture
    4.1 Purpose
    4.2 Package Structure
    4.3 Metadata Categories
        4.3.1 Enums
        4.3.2 Vocabulary
        4.3.3 Library Models
        4.3.4 Relationship Models
        4.3.5 Media Models
        4.3.6 Metadata Services

    4.4 Organization Models
    4.5 Programming Hierarchy
    4.6 Playable Media Hierarchy
    4.7 Metadata Relationships

    4.8 Design Philosophy
        4.8.1 Organizational Metadata vs Playable Media
        4.8.2 Strongly Typed Metadata
        4.8.3 Appearance Philosophy
        4.8.4 Franchise Philosophy
        4.8.5 Organization Philosophy
        4.8.6 Media Item Philosophy
        4.8.7 Episode Philosophy
        4.8.8 Folder Placement Philosophy
        4.8.9 Commercial Hierarchy

    4.9 Metadata Class Reference
        4.9.1 MediaItem
        4.9.2 Movie
        4.9.3 Episode
        4.9.4 Commercial
        4.9.5 Promo
        4.9.6 Station ID
        4.9.7 Documentary
        4.9.8 Music Video
        4.9.9 News Segment
        4.9.10 Weather Segment
        4.9.11 Sports Event
        4.9.12 Ambient
        4.9.13 Infomercial

5. Scheduler Architecture

6. Playback Architecture

7. Channel Architecture

8. Weather Architecture

9. Runtime Lifecycle

10. Data Flow

11. Testing

12. Contribution Guidelines

13. Future Expansion

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

The metadata package defines the complete data model used throughout VISTOR.

Rather than treating media as unrelated JSON documents, VISTOR models every broadcast asset as a structured object with clearly defined relationships.

Every object within the metadata package belongs to one of six architectural categories:

- Enums
- Vocabulary
- Library Models
- Relationship Models
- Media Models
- Metadata Services

Each category has a single responsibility, minimizing duplication while allowing the metadata library to grow without requiring architectural redesign.

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
├── catalog/
│   ├── media_library.py
│   ├── franchise.py
│   ├── series.py
│   ├── season.py
│   ├── advertiser.py
│   ├── product.py
│   └── campaign.py
│
├── relationships/
│   ├── appearance.py
│   ├── media_asset.py
│   └── person.py
│
├── media/
│   ├── media_item.py
│   ├── ambient.py
│   ├── commercial.py
│   ├── documentary.py
│   ├── episode.py
│   ├── infomercial.py
│   ├── movie.py
│   ├── music_video.py
│   ├── news_segment.py
│   ├── promo.py
│   ├── sports_event.py
│   ├── station_id.py
│   └── weather_segment.py
│
├── metadata_loader.py
├── metadata_library.py
├── metadata_search.py
├── metadata_serializer.py
└── metadata_validator.py
```

---

## Metadata Architecture

Metadata
│
├── Enums
│
├── Vocabulary
│
├── Library Models
│
├── Relationship Models
│
├── Media Models
│
└── Metadata Services

---

# Metadata Categories

## Enums

Enums define fixed architectural concepts.

These values describe application behavior rather than descriptive metadata and therefore change very infrequently.

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
- Countries
- Languages
- Tags

Using standardized vocabulary prevents inconsistent metadata while allowing the media library to continue growing.

---

## Content Ratings and Regional Classification Systems

Content ratings are treated as vocabulary metadata rather than fixed application enums.

Although ratings influence scheduling decisions, official rating systems vary significantly between countries, organizations, and media formats.

Examples include:

- MPAA ratings in the United States
- TV Parental Guidelines in the United States
- BBFC ratings in the United Kingdom
- Eirin ratings in Japan
- FSK ratings in Germany

Because these systems are not universal fixed values, they should not be represented as a single enum.

VISTOR separates audience classification from official content ratings.

### Audience

Audience describes the intended target viewer.

Examples:

- Children
- Family
- Teen
- Young Adult
- Adult
- General

Audience is used primarily for scheduling decisions and determining appropriate programming groups.

---

### Content Rating

Content Rating represents an official classification assigned by a recognized rating authority.

Examples:

- MPAA → PG-13
- TV Parental Guidelines → TV-14
- BBFC → 15
- Eirin → PG12

Content ratings should preserve the original rating system rather than converting everything into a universal classification.

Future implementations should associate ratings with:

- Rating authority
- Country
- Rating value
- Description

## Example: International Media and Multiple Classification Systems

A single media item may have different metadata depending on region, language, and presentation.

For example, an English dubbed release of a Japanese animated series may contain:

Media:
    Ghost Stories

Country of Origin:
    Japan

Original Language:
    Japanese

Presentation:
    English Dub

Audience:
    Teen

Content Ratings:

    Japan:
        Rating Authority:
            Eirin

        Rating:
            PG-12

    United States:
        Rating Authority:
            TV Parental Guidelines

        Rating:
            TV-14

These fields represent different concepts. The country does not determine the audience. The language does not determine the rating. The rating does not determine the audience.

A media item should preserve its original cultural and broadcast context while allowing VISTOR to make scheduling decisions appropriate for the selected channel and region.

This separation allows VISTOR to support:

- International programming
- Alternate language releases
- Dubbed and subtitled versions
- Regional broadcast standards
- Different cable provider packages

### Design Philosophy

VISTOR preserves both the original metadata and the generalized information required for scheduling.

A media item may contain:

- Audience:
    - FAMILY

- Content Rating:
    - MPAA PG

These fields answer different questions.

Audience answers:

> "Who is this content intended for?"

Content Rating answers:

> "What official classification was assigned to this content?"

Keeping these concepts separate allows VISTOR to support international media libraries without redesigning the metadata architecture.

## Library Models

Library Models organize the media library.

They provide structure but are never scheduled or played directly.

Examples include:

- Media Library
- Franchise
- Series
- Season
- Person
- Studio
- Network
- Advertiser
- Product
- Campaign

Library Models describe how media is grouped rather than the media itself.

## Programming Hierarchy

Media Library
│
├── Franchises
│
├── Series
│     └── Seasons
│            └── Episodes
│
├── Organizations
│     ├── Studios
│     ├── Networks
│     └── Advertisers
│
└── Standalone Media
      ├── Movies
      ├── Commercials
      ├── Music Videos
      ├── Documentaries
      ├── Promos
      ├── Station IDs
      ├── Sports Events
      ├── News Segments
      ├── Weather Segments
      ├── Ambient
      └── Infomercials

---

## Organization Models

Organization Models represent real-world organizations that participate in the creation, distribution, promotion, or broadcast of media.

Unlike Vocabulary objects, Organization Models possess their own metadata and identity.

Examples include:

- Advertiser
- Network
- Studio

Organization Models are reusable across many media items and are referenced rather than duplicated.

For example:

Movie
→ Production Studio
→ Distributor

Episode
→ Production Studio
→ Original Network

Commercial
→ Advertiser

Separating organizations into dedicated models allows VISTOR to support scheduling and searching based on organizations themselves, such as:

- Studio Ghibli marathon
- Disney Channel programming
- Cartoon Network originals
- Warner Bros. Animation collection

Organizations represent entities.

Vocabulary represents descriptions.

## Relationship Models

Relationship Models connect metadata objects together.

Rather than storing duplicated information throughout the library, shared entities are represented once and referenced wherever needed.

Examples include:

- Person
- Appearance
- Media Asset

Relationship models describe participation, ownership, or storage, but are never directly broadcast.

---

## Media Models

Media Models represent playable broadcast assets.

Every playable object inherits from Media Item.

Examples include:

- Episode
- Movie
- Commercial
- Music Video
- Documentary
- Sports Event
- News Segment
- Weather Segment
- Promo
- Station ID
- Ambient
- Infomercial

Only Media Models may be selected by the scheduler for broadcast.

## Playable Media Hierarchy

MediaItem
│
├── Episode
├── Special
├── Movie
├── Documentary
├── Commercial
├── Promo
├── Station ID
├── Music Video
├── Concert
├── Live Performance
├── Sports Event
├── News Segment
├── Weather Segment
├── Ambient
└── Infomercial

---

## Metadata Services

Metadata Services operate on the metadata library.

They provide functionality rather than representing metadata themselves.

Responsibilities include:

- Loading metadata
- Validating metadata
- Searching metadata
- Managing the metadata library
- Serializing metadata

Keeping these services separate from the metadata models allows the metadata engine to evolve independently of the data itself.

---

# Design Philosophy

Every broadcast asset should be treated uniformly before being treated uniquely.

All playable media inherit from a common Media Item foundation.

Specialized media models extend this foundation only where additional metadata is required.

Supporting metadata is intentionally separated into Library Models, Relationship Models, Vocabulary, and Enums.

This minimizes duplicated information while allowing VISTOR to support television episodes, movies, commercials, music videos, sports broadcasts, documentaries, station IDs, promos, weather programming, ambient programming, infomercials, and future media types using a single consistent architecture.

---

# Organizational Models vs Playable Media

VISTOR distinguishes between organizational metadata and playable media.

Organizational models exist solely to organize related content.

Examples include:

- Franchise
- Series
- Season
- Advertiser
- Product
- Campaign

These models are never scheduled or broadcast.

Playable media inherits from Media Item.

Examples include:

- Episode
- Movie
- Commercial
- Documentary
- Music Video
- Promo
- Station ID

Only playable media contains Media Assets and may be selected by the scheduler.

This separation mirrors the structure of real broadcast television while maintaining a clean metadata hierarchy.

---

# Strongly Typed Metadata

VISTOR favors explicit metadata models over primitive values whenever possible.

Rather than storing arbitrary strings throughout the metadata library, dedicated models and enumerations are used.

Examples include:

- Genre
- Theme
- Tag
- Network
- Country
- Audience
- Content Rating

Collections are strongly typed.

For example:

```python
self.genres: list[Genre] = []
self.tags: list[Tag] = []
self.themes: list[Theme] = []
```

Likewise, relationships are represented using dedicated models rather than duplicated data.

Examples include:

- Media Asset
- Appearance
- Franchise
- Campaign

Strong typing provides several benefits:

- Prevents inconsistent metadata.
- Improves IDE autocompletion.
- Simplifies validation.
- Reduces programming errors.
- Creates a consistent architecture throughout the metadata system.

To avoid circular imports while preserving strong typing, VISTOR uses forward references where appropriate.

```python
from __future__ import annotations
from typing import TYPE_CHECKING
```

Relationship models are imported only during static type checking, allowing strict typing without introducing runtime dependency issues.

---

# Appearance Model Philosophy

A Person represents an individual.

An Appearance represents that person's participation within a specific piece of media.

VISTOR intentionally separates these concepts because a single individual may participate in many different media while performing different roles.

For example, the same person may appear as:

- An actor in a movie
- A spokesperson in a commercial
- A guest on a talk show
- An athlete in a sporting event
- A narrator in a documentary

Rather than storing role-specific information inside the Person model, all participation-specific information is stored inside Appearance.

This includes:

- Role
- Character name
- Display name
- Organization
- Billing order
- Credit status
- Notes

This design prevents duplicated person information while allowing VISTOR to answer complex queries without duplicating metadata.

## People Relationships

Media Item
     │
     ├───────────────┐
     │               │
 Appearance      Appearance
     │               │
     │               │
 Person         Person

---

# Franchise Model Philosophy

A Franchise represents shared intellectual property rather than a collection.

Multiple media items may belong to the same franchise regardless of their format.

Examples include:

- Television series
- Movies
- Commercials
- Promos
- Music Videos
- Station IDs

Media items store a reference to their franchise.

The Franchise model does not maintain lists of associated media.

Instead, the Media Library is responsible for locating every media item that references a given franchise.

This ensures there is only one source of truth within the metadata system.

## Franchise Relationships

Franchise
     │
     ├── Series
     │       └── Episodes
     │
     ├── Movies
     │
     ├── Commercials
     │
     ├── Promos
     │
     ├── Station IDs
     │
     └── Music Videos
     
---

# Commercial Metadata Hierarchy

Commercial metadata is organized using a hierarchical relationship model.

Advertiser
→ Product
→ Campaign
→ Commercial

Each level represents a reusable real-world entity.

- An Advertiser may promote many Products.
- A Product may have many Campaigns.
- A Campaign may contain many Commercials.

Commercials reference these models rather than duplicating advertiser information.

This reduces redundancy while improving search capabilities.

## Commercial Relationships

Advertiser
      │
      ▼
   Product
      │
      ▼
   Campaign
      │
      ▼
  Commercial

---

# Media Item Philosophy

Media Item serves as the common foundation for every playable broadcast asset.

Rather than storing every possible field directly, Media Item references specialized relationship models such as:

- Media Asset
- Appearance
- Franchise
- Campaign

and maintains reusable metadata collections including:

- Genres
- Tags
- Themes

Every playable media type inherits from Media Item.

Specialized media models extend the foundation only where additional metadata is required.

This creates a flexible metadata architecture capable of supporting complex scheduling, searching, and broadcast automation without duplicating information.

---

# Organization Philosophy

VISTOR distinguishes between organizations and people.

A Person participates in media through an Appearance.

An Organization participates through ownership, production, distribution, promotion, or broadcast.

Examples include:

- Studio
- Network
- Advertiser

Unlike people, organizations are never represented by Appearance objects.

Instead, media references organizations directly through dedicated metadata fields.

Examples:

Movie
→ Production Studio
→ Distributor

Episode
→ Network

Commercial
→ Advertiser

Separating organizations from people prevents unrelated concepts from being merged while allowing VISTOR to schedule and search by both independently.

---

## Strongly Typed Metadata Collections

VISTOR uses strongly typed metadata collections rather than generic Python objects.

For example, instead of storing genres as arbitrary strings:

```python
self.genres = []
```

VISTOR stores collections of dedicated metadata objects:

```python
self.genres: list[Genre] = []
self.tags: list[Tag] = []
self.themes: list[Theme] = []
```

The same philosophy applies throughout the metadata system:

- `MediaAsset`
- `Appearance`
- `Franchise`
- `Campaign`
- `Network`
- `Country`
- `ContentRating`
- `Audience`

Each field references a dedicated model or enumeration rather than using primitive values whenever possible.

### Benefits

Using strongly typed metadata provides several advantages:

- Prevents invalid data from entering the metadata library.
- Improves IDE autocompletion and code navigation.
- Makes future validation significantly easier.
- Reduces programming errors caused by inconsistent strings.
- Creates a consistent architecture across every metadata model.
- Makes the metadata system easier to expand without breaking existing code.

### Forward References

As the metadata system grows, some models reference each other.

To avoid circular imports while preserving strong typing, VISTOR uses Python's forward reference system:

```python
from __future__ import annotations
from typing import TYPE_CHECKING
```

Relationship models are imported only during static type checking:

```python
if TYPE_CHECKING:
    from metadata.models.relationships.person import Person
```

This allows VISTOR to maintain strict type safety without creating runtime dependency issues.

### Design Philosophy

VISTOR favors explicit metadata models over generic values.

Rather than asking:

> "Is this string supposed to represent a genre?"

the architecture asks:

> "Is this a Genre object?"

This philosophy makes the metadata library more predictable, easier to maintain, and better suited for long-term expansion as additional broadcast media types are introduced.

## Organizational Models vs Playable Media

VISTOR distinguishes between organizational metadata and playable media.

Organizational models exist solely to group related content.

Examples include:

- Franchise
- Series
- Season

These models are never scheduled or played directly.

Instead, they provide structure for the metadata library.

Playable media inherits from MediaItem.

Examples include:

- Episode
- Movie
- Commercial
- Documentary
- Music Video
- Promo
- Station ID

Only playable media contains MediaAssets and can be selected by the scheduler.

Separating organizational models from playable media keeps the metadata hierarchy clean and accurately reflects how broadcast television is structured.

## Programming Hierarchy

VISTOR models episodic programming using a hierarchical structure.

Series
→ Season
→ Episode

Each level serves a distinct purpose.

A Series represents the overall television program.

A Season groups episodes released together.

An Episode represents an individual broadcast and is the first level that inherits from MediaItem.

Unlike relationship models such as Franchise, Seasons maintain direct references to their Episodes because episodes cannot exist independently of a season.

This hierarchy mirrors both television production and how viewers naturally organize episodic content.

## Metadata Package Organization

The metadata package is organized by architectural responsibility rather than by inheritance or implementation details.

Each subpackage answers a specific question about the metadata system.

### Enums

Fixed values that define immutable classifications.

Examples include:

- MediaType
- Audience
- ContentRating

### Vocabulary

Reusable descriptive objects shared across media.

Examples include:

- Genre
- Theme
- Network
- Country

### Catalog

Objects that organize the media library.

Examples include:

- Franchise
- Series
- Season
- Advertiser
- Product
- Campaign

Library Models are never scheduled or played directly.

### Relationships

Objects that connect metadata together.

Examples include:

- Person
- Appearance
- MediaAsset

These models describe relationships rather than playable media.

### Media

Playable broadcast objects.

Every class in this package inherits from `MediaItem`.

Examples include:

- Episode
- Movie
- Commercial
- Promo
- Documentary

Only Media objects may be scheduled by the VISTOR scheduler.

### Managers

Service classes responsible for operating on the metadata system.

Examples include:

- MetadataLoader
- MetadataLibrary
- MetadataSearch
- MetadataSerializer
- MetadataValidator

Managers manipulate metadata but are not themselves metadata objects.

## Complete Metadata Object Model

                 Media Library
                      │
         ┌────────────┴────────────┐
         │                         │
    Organizational            Standalone
        Media                   Media
         │                         │
     Franchise                 Movie
         │                         │
       Series                 Commercial
         │                         │
       Season                Documentary
         │
      Episode
         │
         ▼
     Media Item
         │
         ├──────────────┐
         │              │
    Media Assets    Appearances
                          │
                          ▼
                       Person

Media Item also references:

• Genres
• Tags
• Themes
• Network
• Country
• Audience
• Content Rating
• Campaign

## Episode Model Philosophy

Episode is the primary playable television object within VISTOR.

Unlike Series and Season, Episode inherits from MediaItem and may therefore be scheduled for broadcast.

An Episode belongs to exactly one Season.

Through its parent Season, an Episode automatically belongs to:

- Series
- Franchise

This relationship eliminates duplicated metadata while preserving the complete programming hierarchy.

Episode stores only metadata unique to an individual broadcast, including:

- Episode Number
- Absolute Episode Number
- Production Code
- Original Air Date
- Runtime

All common metadata—including appearances, genres, tags, themes, media assets, and broadcast classifications—is inherited from MediaItem.

This separation keeps Episode lightweight while allowing the scheduler to treat every episode as a fully featured broadcast asset.

## Folder Placement Philosophy

Metadata is organized by architectural responsibility rather than by implementation details or inheritance.

When introducing a new metadata class, its location should be determined by its primary responsibility.

Use the following questions to determine the correct package:

- Is it a fixed application value? → Enums
- Is it standardized descriptive metadata? → Vocabulary
- Does it organize the media library? → Library Models
- Does it connect other metadata objects? → Relationship Models
- Can it be scheduled and broadcast? → Media Models
- Does it operate on metadata? → Metadata Services

Every metadata object should belong to exactly one architectural category.

This organization prioritizes long-term maintainability by grouping objects according to their purpose rather than their implementation.

## Organizational Metadata vs Playable Media

VISTOR intentionally separates objects that organize media from objects that represent broadcast media.

Library Models exist solely to organize and describe the media library.

Media Models represent assets that can actually be scheduled for broadcast.

For example:

Series
→ organizes Episodes

Season
→ organizes Episodes

Campaign
→ organizes Commercials

None of these objects can be played directly.

Conversely:

- Episode
- Movie
- Commercial
- Promo
- Documentary

all inherit from Media Item and represent playable broadcast assets.

This separation mirrors the structure of real broadcast television while preventing organizational metadata from being treated as media.