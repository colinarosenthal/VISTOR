# VISTOR User Manual

**Version:** 0.8.1

---

## Quick Start

VISTOR emulates a broadcast cable TV box. You don't select individual programs:
when it's running, a channel is already playing, and you change channels to see
what each one is currently airing. Channels run in real time, so if you switch
away and come back, the program has continued in your absence — nothing pauses
or waits for you.

### Starting up

Power on the device. Once it boots, a channel begins playing automatically.
There is no login and no program-selection menu.

### Changing channels

- **Channel up / down** moves to the next or previous channel.
- **Number buttons** let you enter a channel directly. Type the number, then
  press "Enter"/"OK" to jump to it.
- **Previous** (or "Last") returns you to the channel you were watching before.

Each channel change briefly displays a corner banner with the channel number
and name, which then fades out on its own.

### Volume and mute

- **Volume up / down** adjusts the level, and a volume bar appears while you do.
- **Mute** silences audio; press it again to restore sound.

### The on-screen guide

Press **Guide** to display all channels and what each is currently airing. Use
up/down to scroll the list, and close it to return to viewing.

### Settings

Press **Settings** to open the on-screen menu, navigated with the arrow
buttons. The key setting is **broadcast mode**, which controls how commercials
air:

- **Off** — no commercials; programs play back to back.
- **Between Programs** — commercials air only in the gap between one program
  ending and the next beginning.
- **Mid-Program** — commercials interrupt a program partway through, as on
  traditional broadcast TV, after which the program resumes.

Close the settings menu to save your selection.

### The clock

Press **Clock** to briefly display the current time. It fades out after a few
seconds.

---

## Common Questions

**Can I rewind or pause?**
No. VISTOR is designed to behave like live TV — whatever is airing is airing now.

**Why did the channel keep going while I was away?**
By design. Each channel runs on its own real-time schedule, exactly like
broadcast television.

**Nothing is playing on a channel.**
That channel may not have programming loaded yet. Switch to another channel.

---

## Remote Buttons at a Glance

| Button          | What it does                                  |
|-----------------|-----------------------------------------------|
| Channel Up/Down | Next / previous channel                       |
| Number + Enter  | Jump directly to a channel number             |
| Previous / Last | Return to the channel you were just watching  |
| Volume Up/Down  | Adjust loudness                               |
| Mute            | Silence / un-silence                          |
| Guide           | Open the on-screen channel guide              |
| Settings        | Open the on-screen settings menu              |
| Clock           | Briefly show the current time                 |

---

# Full Reference

The section above covers everyday use. The rest of this manual explains how
VISTOR is set up, how to add your own media, and how the system works
internally.

## 1. What VISTOR Is (In More Detail)

VISTOR is not a streaming app and not a media library. It recreates *broadcast
television* the way it worked before on-demand streaming: a set of channels
that are always "on the air." Each channel runs its own continuous schedule of
shows, movies, commercials, station IDs, and promos. If you change the channel
and come back later, that channel has kept "broadcasting" the whole time — you
join it wherever it happens to be, not where you left it.

Only the channel you are watching is actually decoded and drawn on screen; all
the other channels advance silently in the background so they stay at the
correct live position. That is why switching channels resumes a program in the
middle instead of starting it over.

## 2. Installing

1. Install Python 3 and Git.
2. Clone the repository and run the bootstrap installer:
   - Windows: `./setup.ps1`
3. Install dependencies: `pip install -r requirements.txt`
4. (Optional) Install `ffmpeg`, `libmpv`, and `fpcalc` for real video output,
   YouTube merging, and music fingerprinting. VISTOR runs without them (it
   falls back to a headless/no-op mode), but you need them for on-screen video.

## 3. Adding Media

VISTOR builds a channel lineup from media you add. Two ways:

- **Web UI (easiest):** run `python Tools/add_media_web.py`. A page opens in
  your browser. Paste a link (YouTube / Internet Archive / direct URL) or drop
  a file. VISTOR scrapes the title/year/description, corrects it against an
  authoritative source, shows a preview card, and lets you pick the right match
  ("did you mean...?") before committing.
- **Command line:** `python Tools/add_media.py "<url>"` or
  `python Tools/add_media.py path/to/record.json`. Add `--no-download` to
  catalog without pulling the file, or `--type` / `--title` / `--year` /
  `--genres` to pin values that the authoritative source will never overwrite.

To rebuild your catalog from the metadata stored next to each media file, run
`python Tools/rebuild_media.py` (add `--no-download` to rebuild the catalog
only, without pulling the files back).

## 4. Using the Controls (Detailed)

Once running, VISTOR behaves like a cable box:

- **Channel up / down** and **numeric entry** (type a channel number, then
  press Enter/OK to commit it).
- **Previous channel** jumps back to the last channel you watched.
- **Volume up / down** and **mute**.
- **Guide** opens the on-screen program grid (current + upcoming programs per
  channel). Use up/down to move through it and close it to resume watching.
- **Settings** opens the on-screen settings menu (see below).
- **Clock** briefly flashes the current time.
- The **channel banner**, **program info**, and **clock** overlays fade in and
  out automatically.

Channels never stop. Switching channels resumes the destination channel at the
correct live position, not from the beginning.

## 5. How Channels and Schedules Work

- Channels are defined in `ChannelConfigs/channels.json` — you can add or edit
  channels with no code changes.
- Schedules live in `Schedules/` as authored JSON (`weekday.json`,
  `weekend.json`, `halloween.json`, ...). VISTOR picks the right schedule for
  the current day, including holidays; a holiday that falls on a weekend still
  selects its holiday lineup. If no schedule is authored it falls back to
  sensible in-code defaults so a channel always has something to air.
- "Broadcast mode" controls commercials: off, between programs, or mid-program
  (using commercial break points detected when the media was downloaded, or
  runtime-spaced breaks as a fallback).

## 6. The Settings Menu (Detailed)

The on-screen settings menu edits VISTOR's configuration and saves it to disk
when you close the menu. Use up/down to pick a row and left/right to change a
value. The available settings are:

| Setting            | What it controls                                                            |
|--------------------|-----------------------------------------------------------------------------|
| Storage Budget     | Maximum disk space VISTOR keeps for media before it evicts low-priority files (steps by 1 GB; "Unlimited" = off). |
| Commercials        | Broadcast mode: Off, Between Programs, or Mid-Program.                       |
| Captions           | Turns subtitles/captions on or off.                                         |
| OSD Enabled        | Turns the on-screen overlays (banners, clock, etc.) on or off.              |
| Weather Enabled    | Enables weather-themed features (reserved for the future Weather subsystem). |
| Recommended Media  | Lets VISTOR suggest (or, if configured, automatically acquire) new media.   |

---

## 7. For Newcomers — What Every File and Folder Is

If you've never worked on a software project, here's what each part of the
VISTOR folder is and why it exists. Many of these are *standard conventions*
used by almost all Python projects, noted where they apply.

### Top-level project files (standard conventions)

- **`README.md`** — the front page of the project. Standard in virtually every
  software repository; it's the first thing people read.
- **`CHANGELOG.md`** — a dated, versioned history of what changed in each
  release. Follows the widely used "Keep a Changelog" convention.
- **`ROADMAP.md`** — what's planned and what's done. Not universal, but common
  for long-running projects.
- **`requirements.txt`** — the list of third-party Python packages VISTOR
  needs. Standard in Python; `pip install -r requirements.txt` installs them.
- **`setup.ps1`** — a bootstrap installer script that creates the folder
  structure and environment. Project-specific.
- **`LICENSE`** — the legal terms for using the source code. Standard and
  expected for any open-source project.

### Source and tests

- **`src/`** — all of VISTOR's actual program code, split into subsystems
  (see below). Keeping code in a `src/` folder is a common Python layout.
- **`src/tests/`** — the test suite, split into one module per subsystem
  (`test_metadata.py`, `test_player.py`, `test_playback.py`, `test_engine.py`,
  `test_osd.py`, `test_icm.py`, `test_scheduling.py`, `test_acquisition.py`,
  `test_catalogue_expansion.py`), with `test_suite.py` as the runner that
  executes them all. Keeping tests together is a standard convention.
- **`Tools/`** — helper scripts you run by hand (`add_media.py`,
  `add_media_web.py`, `rebuild_media.py`, classifier tuner).
- **`Scripts/`** — one-off setup/seed scripts (e.g. seeding vocabulary).

Inside almost every code folder you'll find an **`__init__.py`** file. In
Python, this marks a folder as an importable "package." It's a standard
convention, not something specific to VISTOR.

### The subsystems inside `src/`

- **`core/`** — the foundation: app startup/shutdown, the `Clock`,
  configuration, logging, file paths, and the version number.
- **`engine/`** — the runtime loop that ties everything together each tick.
- **`scheduler/`** — decides what airs when (schedules, programming blocks,
  broadcast events and modes).
- **`metadata/`** — the "brain": describes every piece of media (movies,
  episodes, music videos, commercials), plus the services that acquire,
  enrich, score, cache, and store them.
- **`channel/`** — pairs a schedule + queue + player so each channel runs.
- **`player/`** — plays the current item and renders it to the screen (via mpv,
  or a headless no-op when there's no display).
- **`osd/`** — the on-screen overlays (channel banner, volume, clock, guide,
  settings).
- **`guide/`** — builds the electronic program guide grid.
- **`remote/`** — maps remote/keyboard buttons to actions.
- **`settings/`** — the on-screen settings menu.
- **`ingest/`** — the drag-and-drop web app for adding media.

### The data and media folders

- **`Media/`** — the actual video/audio files (kept on the external SSD in the
  finished build).
- **`Metadata/`** — the catalog: JSON files describing your media, people,
  studios, vocabulary, and configuration.
- **`ChannelConfigs/`** — channel definitions (`channels.json`).
- **`Schedules/`** — authored daily/seasonal schedules.
- **`Config/`, `Cache/`, `Logs/`, `Assets/`** — runtime configuration, cached
  data, log output, and static assets.
- **`Docs/`** — all the documentation you're reading now.
