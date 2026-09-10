# Technical Notes

This document serves as the engineering notebook for VISTOR.

Unlike the Design Bible, which describes what VISTOR should become, this document records technical knowledge, implementation decisions, development techniques, and lessons learned during the creation of the project.

Topics may include:

- Programming concepts
- PowerShell
- Python
- Git
- Raspberry Pi
- MPV
- Metadata
- JSON
- Performance
- Architecture

The purpose of this document is to explain not only how VISTOR works, but why specific technical decisions were made.

---

# Relative Project Paths

## Concept

Software should never assume it will always be installed in the same location.

VISTOR is designed to function correctly regardless of where the project folder is stored, including:

- Internal SSD
- External USB SSD
- Windows computer
- Raspberry Pi

This allows the project to remain portable and avoids failures caused by hardcoded file paths.

## PowerShell

PowerShell provides the automatic variable:

```powershell
$ProjectRoot = $PSScriptRoot
```

`$PSScriptRoot` contains the directory where the currently running PowerShell script is located.

Instead of referencing a specific path such as:

```powershell
C:\VISTOR
```

the installer can use:

```powershell
$ProjectRoot = $PSScriptRoot
```

All folders and files are then created relative to the script's location.

## Why This Matters

Using `$PSScriptRoot` allows the same installer to function correctly regardless of where it is executed.

Examples include:

- `C:\VISTOR`
- `D:\Projects\VISTOR`
- `E:\Portable\VISTOR`
- `/home/pi/VISTOR` *(when the project is transferred to the Raspberry Pi)*

No changes to the installer are required when moving the project between systems.

## VISTOR Design Principle

VISTOR follows a "Relative Paths" philosophy.

All project components should determine their location dynamically rather than relying on hardcoded paths.

This improves portability, simplifies installation, and supports the project's goal of operating identically on Windows development machines and the final Raspberry Pi hardware.

## Key Takeaway

Whenever possible:

- Determine the project location automatically.
- Build paths relative to the project root.
- Never hardcode installation directories.
- Design every component to be portable.

### Applied In VISTOR

- `setup.ps1` uses `$PSScriptRoot` to locate the project root.
- Future Python modules will use `pathlib.Path` to achieve the same portability.
- This approach ensures VISTOR can be copied between Windows PCs, external drives, and Raspberry Pi systems without requiring configuration changes.

---

# Bootstrap Installers

## Concept

A bootstrap installer is a script whose purpose is to create the initial structure required for a software project.

Rather than containing the application itself, a bootstrap installer prepares the environment so development or execution can begin.

For VISTOR, this installer is `setup.ps1`.

## Single Responsibility

A well-designed bootstrap installer should have one clearly defined responsibility.

For VISTOR, the responsibility of `setup.ps1` is:

> Transform an empty directory into a correctly structured VISTOR project without modifying or overwriting existing work.

This means the installer creates the project's folder structure and foundational files while leaving all implementation details to the development process.

## Idempotency

A bootstrap installer should be **idempotent**.

An idempotent program can be run multiple times without causing unintended side effects.

For VISTOR, this means:

- Existing folders are left unchanged.
- Existing files are never overwritten.
- Missing folders are created.
- Missing foundational files are created.
- User data is preserved.

Running the installer multiple times should safely repair or complete the project structure without damaging existing work.

## Portability

The installer should never assume VISTOR is installed in a specific location.

Instead, it should determine the project directory automatically using relative paths.

For PowerShell, this is accomplished using:

```powershell
$ProjectRoot = $PSScriptRoot
```

This allows the same installer to function correctly whether VISTOR is stored on:

- Internal SSD
- External USB SSD
- Windows computer
- Raspberry Pi

No changes to the installer are required when the project is moved.

## Scope

A bootstrap installer should only perform setup tasks.

For VISTOR, `setup.ps1` should:

- Create the project folder structure.
- Create foundational project files.
- Create `.gitkeep` files where appropriate.
- Display setup progress and a completion summary.

The installer should **not**:

- Generate application source code.
- Create placeholder Python modules.
- Generate schedules.
- Create metadata.
- Download media.
- Install third-party software.

These tasks belong to the development process or dedicated utility scripts.

## Why This Matters

Keeping the installer focused on a single responsibility makes it:

- Easier to maintain.
- Safe to rerun.
- Portable across systems.
- Less likely to become outdated as the project evolves.

As VISTOR grows, the application code may change significantly, but the installer's responsibility should remain simple and stable.

## Applied In VISTOR

- `setup.ps1` serves as the official bootstrap installer for the project.
- It creates the VISTOR project skeleton while preserving existing work.
- The installer uses relative paths to support Windows development and Raspberry Pi deployment.
- Future setup tasks beyond project initialization will be implemented as separate utility scripts rather than expanding the responsibilities of `setup.ps1`.

---

# Configuration Through Data

## Concept

Rather than hardcoding repeated actions throughout a program, it is often better to store the information in a collection and process it automatically.

Instead of writing dozens of individual commands to create folders, VISTOR stores every required directory in a single list.

The installer then loops through that list and performs the same action for each item.

## Benefits

- Easier to read.
- Easier to maintain.
- Adding a new folder only requires editing one list.
- Reduces duplicate code.
- Makes the installer scalable as the project grows.

## Applied In VISTOR

The VISTOR installer stores:

- Project folders
- Root files
- `.gitkeep` directories

as separate collections. Future additions require updating only these lists rather than modifying the installation logic itself.

---

# Building File Paths

## Concept

Programs frequently need to construct file paths from smaller pieces.

Rather than manually combining text, PowerShell provides the `Join-Path` command.

This ensures paths are created correctly and improves portability.

---

## Why This Matters

Joining paths manually is error-prone and may not work consistently across operating systems.

Using `Join-Path` makes code safer and easier to read.

---

## Applied In VISTOR

The installer builds every project path using `Join-Path`, including the automatic creation of `.gitkeep` files inside selected directories.

---

# Enumerations vs. Constants

## Concept

Not every predefined value in VISTOR should be represented the same way.

Some values define the architecture of the software and are expected to remain stable throughout the lifetime of the project.

Other values exist only to describe media and are expected to evolve as the media library expands.

Choosing the appropriate representation improves both reliability and flexibility.

## Enumerations

Enumerations (Enums) are used when a value must be selected from a fixed set of valid options.

Examples include:

- MediaType
- Audience
- ContentRating

Enums provide several advantages:

- Prevent typographical errors.
- Provide IDE auto-completion.
- Restrict values to a predefined set.
- Clearly communicate architectural concepts.

Because these values directly affect how VISTOR operates, they are considered part of the application's architecture rather than user-editable metadata.

## Constants

Some classifications benefit from a standardized vocabulary but are expected to expand over time.

Rather than using Enums, these values are represented as predefined string constants.

Examples include:

- Genres
- Themes

This provides consistency throughout the project while allowing additional classifications to be introduced without significantly affecting the underlying architecture.

## Tags

Tags are intentionally unstructured.

Unlike Genres or Media Types, Tags are expected to evolve continuously throughout the lifetime of a media library.

Examples include:

- Halloween
- Christmas
- Cult Classic
- Viewer Favorite
- Marathon Eligible

Tags are stored as ordinary strings rather than predefined constants or Enums.

This allows metadata to remain flexible without requiring changes to the application's source code.

## Why This Matters

Using the appropriate representation for each type of metadata improves both software quality and long-term maintainability.

Stable architectural concepts benefit from strict validation and type safety.

Descriptive metadata benefits from flexibility and the ability to evolve alongside the media library.

Separating these responsibilities prevents unnecessary code changes while preserving consistency throughout the project.

## Applied In VISTOR

VISTOR uses Enums for architectural concepts that are expected to remain stable, including:

- MediaType
- Audience

VISTOR uses standardized vocabulary for descriptive metadata that may expand over time, including:

- Genres
- Themes
- Languages
- Content Ratings

Content Ratings are vocabulary rather than an Enum because rating systems vary by country and organization, and each rating preserves its original authority, country, and value.

User-defined Tags remain free-form strings to support unlimited media classification without requiring changes to the application's architecture.

---

# Metadata Classification Philosophy

## Concept

Not every piece of metadata represents the same kind of information.

Some values define the architecture of VISTOR and are expected to remain stable throughout the lifetime of the project.

Other values exist to describe media and are expected to evolve as the media library expands.

To keep the system organized, VISTOR separates metadata into three categories:

- Enums
- Vocabulary
- Models

Each category serves a different purpose within the metadata system.

## Enums

Enums define architectural concepts.

These represent fixed classifications that should rarely change and are used throughout the application's logic.

Examples include:

- MediaType
- PresentationType
- Audience
- ContentRating

Because these values are part of the software architecture, they benefit from strict validation, IDE auto-completion, and compile-time consistency.

## Vocabulary

Vocabulary files define standardized descriptive values.

Unlike Enums, these collections are expected to expand over time as the media library grows.

Examples include:

- Genres
- Music Genres
- Themes
- Networks
- Countries

Using standardized vocabulary prevents inconsistent naming while allowing the library to evolve without affecting the application's architecture.

Tags are intentionally excluded from this category because they are designed to remain completely free-form.

## Models

Models represent the structure of the media library itself.

Rather than describing classifications, models describe relationships between media objects.

Examples include:

- MediaLibrary
- Series
- Season
- Episode
- MediaAsset
- Person

These models define how media is organized within VISTOR and form the foundation upon which scheduling, metadata, and playback systems operate.

## Why This Matters

Separating metadata into architectural concepts, descriptive vocabulary, and data models keeps responsibilities clearly defined.

Architectural concepts remain stable and strongly typed.

Vocabulary remains standardized while allowing the media library to expand naturally.

Models describe relationships between media rather than individual classifications.

This separation improves maintainability, reduces duplication, and provides a scalable foundation for future features.

## Applied In VISTOR

The metadata package is organized into six sub-packages:

```text
metadata/
├── enums/          architectural concepts (audience, content_rating, media_type, presentation_type)
├── vocabulary/     controlled descriptive terms (genre, music_genre, network, country, theme, tag)
├── library/        library-level container models
├── media/          media item models (movies, episodes, music videos, commercials, ...)
├── relationships/  relationship models (people, studios, franchises, series, seasons, ...)
└── services/       acquisition, enrichment, scoring, caching, serialization, ingestion
```

This organization reflects the philosophy that architectural concepts,
descriptive vocabulary, media models, and their relationships should remain
independent systems while working together to describe every piece of media
within VISTOR. The `services/` layer holds the behavior — acquisition,
enrichment, scoring, caching, serialization, and ingestion — that operates over
those models.
