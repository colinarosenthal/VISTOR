# Metadata

The metadata package defines the complete broadcast data model used throughout VISTOR.

Metadata is organized by architectural responsibility rather than by implementation details.

## Package Layout

- Enums — Fixed application values.
- Vocabulary — Standardized descriptive metadata.
- Library — Organizes the media library.
- Relationships — Connects metadata objects together.
- Media — Playable broadcast assets.
- Services — Operate on metadata.

## Choosing the Correct Folder

Ask one question:

- Is it a fixed classification? → Enums
- Is it descriptive? → Vocabulary
- Does it organize media? → Library
- Does it connect objects? → Relationships
- Is it playable content? → Media
- Does it perform an operation? → Services

Every new metadata object should belong to exactly one of these categories.
