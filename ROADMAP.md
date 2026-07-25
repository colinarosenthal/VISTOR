# VISTOR Roadmap

**Project Status:** Pre-Alpha

**Current Version:** 0.2.0

**Last Updated:** July 24, 2026

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

**Phase 3 — Core Software**

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

# Phase 2 — Media Library

## Media Organization

- [ ] Finalize media folder structure
- [ ] Organize existing media library

---

## Media Acquisition

Programming

- [ ] Television Shows
- [ ] Movies
- [ ] Sports
- [ ] News
- [ ] Documentaries
- [ ] Game Shows
- [ ] Talk Shows

Supporting Content

- [ ] Commercials
- [ ] Station IDs
- [ ] Network Promos
- [ ] Music Videos
- [ ] Infomercials
- [ ] Ambient Loops

---

## Metadata

- [ ] Design metadata format
- [ ] Build metadata templates
- [ ] Create first metadata entries
- [ ] Build metadata validator

---

## Milestone

VISTOR has a usable media library and organized metadata system.

---

# Phase 3 — Core Software

## Foundation Modules

- [ ] Configuration Loader
- [ ] Logging System
- [ ] Relative Path Manager
- [ ] Utility Library

---

## Metadata Engine

- [ ] Media Scanner
- [ ] Metadata Parser
- [ ] Metadata Validator

---

## Scheduler

### Foundation

- [x] Implement Clock subsystem
- [x] Implement calendar detection
- [x] Implement weekday/weekend detection
- [x] Implement holiday detection
- [x] Implement ScheduleType
- [x] Implement ProgrammingBlock
- [x] Implement Schedule
- [x] Implement Scheduler

### Schedule Management

- [ ] Implement ScheduleLoader
- [ ] Populate schedule library
- [ ] Connect ScheduleLoader to Scheduler
- [ ] Automatic weekday schedule selection
- [ ] Automatic weekend schedule selection
- [ ] Automatic holiday schedule selection

### Broadcast Scheduling

- [ ] Daily Schedule Generator
- [ ] Weekly Schedule Generator
- [ ] Commercial Scheduler
- [ ] Persistent Playback Engine

---

## Milestone

VISTOR can determine what every channel should currently be broadcasting.

---

# Phase 4 — Playback System

## Player

- [ ] Video Playback
- [ ] Playlist Management
- [ ] Channel Switching
- [ ] Resume Playback After Channel Changes
- [ ] Persistent Playback
- [ ] Keyboard Controls

---

## Channel Management

- [ ] Channel Definitions
- [ ] Channel Manager
- [ ] Previous Channel Support
- [ ] Numeric Channel Entry

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

## Future Entries

Record each significant development session, milestone, or architectural decision here as the project progresses.