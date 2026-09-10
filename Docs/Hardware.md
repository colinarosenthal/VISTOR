# VISTOR Hardware Guide

VISTOR is designed to run as a self-contained "cable box" on a Raspberry Pi
wired to a CRT television. This document lists the reference hardware and
explains the role each part plays in the signal chain.

## Reference Build

| Component | Purpose |
|-----------|---------|
| Raspberry Pi 5 (8 GB) | Runs VISTOR; decodes and renders the watched channel while all others advance headlessly. |
| Official 27W USB-C PSU | Stable power for the Pi 5 under sustained video decode. |
| Official Active Cooler | Keeps the Pi 5 cool during continuous playback. |
| 32 GB A2 microSD card | Boot device and OS; A2 rating improves random I/O. |
| 1–2 TB external USB SSD | Media storage root (configurable via `Config.media_directory`). Keeps the media library off the SD card for speed and endurance. |
| Micro-HDMI to HDMI cable | Digital video/audio out from the Pi. |
| Active HDMI -> analog converter | Converts the Pi's HDMI to composite / S-Video for a CRT. Must be *active* (powered), not a passive adapter. |
| RCA / S-Video / SCART cable | Carries the analog signal into the CRT's input. |
| IR receiver + remote | Physical remote input, mapped by `RemoteController` to channel/volume/guide/settings actions. |

## Signal Chain

VISTOR outputs a modern digital signal and steps it down to what a CRT accepts:

Raspberry Pi 5 ──(micro-HDMI → HDMI)──▶ Active HDMI→Analog Converter ──(RCA / S-Video / SCART)──▶ CRT Television
│
├──(USB 3)──▶ External USB SSD (Media/ storage root)
│
└──(USB / GPIO)──▶ IR Receiver ◀──(infrared)── Handheld Remote

The Pi renders only the channel currently being watched; every other channel
advances headlessly so it stays at the correct live position. Digital HDMI
audio/video leaves the Pi and is converted to analog composite/S-Video by the
*active* (powered) converter — a passive adapter will not work because HDMI
carries no analog signal to passively tap. The converted signal then feeds the
CRT's RCA, S-Video, or SCART input.

Media lives on the external USB SSD rather than the microSD card for speed and
write endurance; the SSD path is set by `Config.media_directory`. Remote input
arrives through the IR receiver and is mapped to channel/volume/guide/settings
actions by `RemoteController`. During development a normal USB keyboard can
stand in for the IR remote.
