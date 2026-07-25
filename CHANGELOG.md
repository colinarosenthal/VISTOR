# Changelog

All notable changes to VISTOR will be documented in this file.

The format is based on *Keep a Changelog*, adapted for the long-term development of VISTOR.

---

## [0.1.0] — Core Foundation

### Added

#### Project

- Initial project architecture
- Standardized project folder structure
- Bootstrap installer (`setup.ps1`)
- Relative path installation support
- Git repository
- GitHub repository
- Python virtual environment
- Project dependency management

#### Documentation

- Complete Design Bible
- README
- Roadmap
- Changelog
- Hardware documentation
- Ideas document
- Developer Guide
- User Manual
- Technical Notes

#### Core Application

- Application entry point
- Engine architecture
- Engine lifecycle
- Runtime loop foundation
- Startup sequence
- Shutdown sequence
- Project path management
- Configuration system foundation
- Logging system foundation

#### Scheduling Foundation

- Clock subsystem
- Calendar detection
- Weekday detection
- Weekend detection
- Holiday detection
- ScheduleType
- ProgrammingBlock
- Schedule
- Scheduler architecture

#### Architecture

- Relative Paths philosophy
- Bootstrap Installer philosophy
- Configuration Through Data philosophy
- Project portability architecture

### Milestone

VISTOR possesses a complete project foundation and application skeleton ready for subsystem development.

## [0.2.0] — Metadata Architecture

### Added

- Designed the complete metadata engine architecture.
- Established `MediaItem` as the common base model for every playable broadcast asset.
- Designed reusable library models:
  - Media Library
  - Franchise
  - Series
  - Season
  - Advertiser
  - Product
  - Campaign
- Designed relationship models:
  - Person
  - Appearance
  - Media Asset
- Designed specialized media models for:
  - Television
  - Film
  - Advertising
  - Music
  - Miscellaneous media
- Designed metadata service layer:
  - Metadata Loader
  - Metadata Library
  - Metadata Search
  - Metadata Serializer
  - Metadata Validator
- Added metadata package documentation (`README.md`).
- Expanded the Developer Guide with complete metadata architecture documentation.
- Documented:
  - Metadata architecture philosophy
  - MediaItem philosophy
  - Appearance relationship philosophy
  - Franchise philosophy
  - Commercial hierarchy philosophy
  - Folder organization philosophy
  - Organizational vs. playable media philosophy

### Changed

- Reorganized the metadata package around architectural responsibility rather than file type.
- Replaced the original metadata structure with six primary subsystems:
  - Enums
  - Vocabulary
  - Library
  - Relationships
  - Media
  - Services
- Reorganized media models into functional categories:
  - Advertising
  - Film
  - Music
  - Television
  - Miscellaneous
- Updated the project roadmap to establish the Metadata Engine as its own development phase.
- Refined the overall project architecture to support long-term scalability and reduce metadata duplication.