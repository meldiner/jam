# X AIR OSC Protocol Notes

## Sources

- Music Tribe, [X AIR Mixer Series Remote Control Protocol](https://mediadl.musictribe.com/download/software/behringer/XAIR/X%20AIR%20Remote%20Control%20Protocol.pdf)
- Music Tribe, [X AIR user manual](https://mediadl.musictribe.com/media/sys_master/hff/hde/8849590714398.pdf)

## Transport

- Protocol: OSC-compatible messages with Music Tribe parameter-query and subscription extensions.
- Transport: UDP.
- Mixer receive port: `10024`.
- Replies: sent to the source IP and UDP port of the requester.
- Encoding: big-endian, 4-byte aligned OSC strings and values.
- Security: no protocol authentication or encryption; use only on a trusted LAN and do not port-forward it.

## Initial Verified Paths

| Purpose | OSC path | Type |
|---|---|---|
| Mixer identity | `/xinfo` | query; returns IP, name, model, firmware strings |
| Channel name | `/ch/01/config/name` | string, channels `01`–`16`, 12 characters max |
| Bus name | `/bus/1/config/name` | string, buses `1`–`6`, 12 characters max |
| Channel color | `/ch/01/config/color` | integer `0`–`7`, channels `01`–`16` |
| Bus color | `/bus/1/config/color` | integer `0`–`7`, buses `1`–`6` |

The standard color map is `0=off`, `1=red`, `2=green`, `3=yellow`,
`4=blue`, `5=magenta`, `6=cyan`, and `7=white`. X AIR Edit also shows
inverse display variants, but the helper intentionally exposes only the standard
set for predictable person/group identification.

A parameter query sends the address with no arguments. A set sends the same address with one typed value. The mixer normally echoes the parameter path and current value.

## Rehearsal Mixer Facts

Verified with a direct, read-only `/xinfo` request on 2026-07-30; confirm again before each control session:

- Address: `192.168.1.149`
- Console name: `Guest House Mixer`
- Model shown by X AIR Edit: `XR18V2`
- Firmware shown by X AIR Edit: `1.25`
- X AIR Edit version: `1.8.1`

Representative direct parameter reads also returned `Bass` for
`/ch/01/config/name` and `Desk L` for `/bus/1/config/name`.

## Current Input and Monitor Map

| Target | Intended label | Connection |
|---|---|---|
| Channel 1 | `Bass` | Bass |
| Channel 2 | blank | Empty |
| Channel 3 | `Drums` | Drums |
| Channel 4 | `Keys` | Keyboard |
| Channel 5 | `Guitar` | Guitar |
| Channels 6–8 | blank | Empty/unassigned |
| Channels 9–13 | `Mic 1`–`Mic 5` | Microphones |
| Bus 1 / Aux 1 | `Desk L` | Left desktop monitor |
| Bus 2 / Aux 2 | `Desk R` | Right desktop monitor |
| Bus 3 / Aux 3 | `Drum Mon` | Drums monitor |
| Bus 4 / Aux 4 | `Door Mon` | Sliding-door monitor |
| Bus 5 / Aux 5 | `Bass Amp` | Bass amp |

## Extension Rules

Before adding a new writable parameter:

1. Confirm the exact path, type, range, and unit against a trusted protocol map or a read from the real mixer.
2. Implement a dedicated subcommand; do not expose arbitrary raw writes.
3. Convert human units explicitly. X AIR commonly represents continuous values as normalized floats from `0.0` to `1.0`, not directly as dB or Hz.
4. Validate target indices and value bounds before opening the UDP socket.
5. Read the current value, preview the proposed change, and require an apply flag.
6. Query the same path afterward and fail if the returned value is outside the expected tolerance.
7. Test encoding and conversion locally before any live-mixer write.

Treat preamp gain, phantom power, routing, snapshot recall, initialization, and firmware operations as especially consequential.
