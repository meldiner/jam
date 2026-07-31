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
| Channel main fader | `/ch/01/mix/fader` | normalized float; channels `01`–`16` |
| Bus master fader | `/bus/1/mix/fader` | normalized float; buses `1`–`6` |
| Main LR master fader | `/lr/mix/fader` | normalized float |
| Analog input gain | `/headamp/01/gain` | normalized float; inputs `01`–`16` |
| Channel send to bus | `/ch/01/mix/01/level` | normalized float; channels `01`–`16`, buses `01`–`06` |
| Aux/FX return Main fader | `/rtn/aux/mix/fader`, `/rtn/1/mix/fader` | normalized float; Aux plus FX returns `1`–`4` |
| Aux/FX return send to bus | `/rtn/aux/mix/01/level`, `/rtn/1/mix/01/level` | normalized float; buses `01`–`06` |

The standard color map is `0=off`, `1=red`, `2=green`, `3=yellow`,
`4=blue`, `5=magenta`, `6=cyan`, and `7=white`. X AIR Edit also shows
inverse display variants, but the helper intentionally exposes only the standard
set for predictable person/group identification.

A parameter query sends the address with no arguments. A set sends the same address with one typed value. The mixer normally echoes the parameter path and current value.

For the narrow reset workflow, fader `0.0` is the slider minimum (`-inf`)
and fader `0.75` is unity (`0 dB`). These points were verified against X AIR
Edit and direct reads on 2026-07-30. Analog headamp gain uses a linear
normalized scale from `-12 dB` at `0.0` to `+60 dB` at `1.0`; therefore
`0 dB` is `1/6` (`0.166666...`). Current readings of `0.375` and
`0.444444...` matched the app's `+15 dB` and `+20 dB` displays.

The XR18V2 quantizes normalized fader writes: requesting unity `0.75` reads
back as `0.7497556209564209`. Float verification therefore uses a `0.0005`
tolerance, just over the observed difference and approximately half of one
`1/1023` hardware step.

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
| Channel 14 | numeric/default | Mic 6, reserved for Moria |
| Bus 1 / Aux 1 | `Desk L` | Left desktop monitor |
| Bus 2 / Aux 2 | `Desk R` | Right desktop monitor |
| Bus 3 / Aux 3 | `Drum Mon` | Drums monitor |
| Bus 4 / Aux 4 | `Door Mon` | Sliding-door monitor |
| Bus 5 / Aux 5 | `Bass Amp` | Bass amp |
| Bus 6 / Aux 6 | numeric/default | Future monitor for Moria |

## Person Color Map

Verified on the rehearsal mixer on 2026-07-30. Each person's instrument,
vocal mic, and monitor share one standard scribble-strip color.

| Person | Color | Targets |
|---|---|---|
| Ortal | red (`1`) | Channel 1 Bass, Channel 9 Mic 1, Bus 5 Bass Amp |
| Ron | blue (`4`) | Channel 5 Guitar, Channel 10 Mic 2, Bus 1 Desk L |
| Ronen | green (`2`) | Channel 4 Keys, Channel 11 Mic 3, Bus 2 Desk R |
| Nadav | yellow (`3`) | Channel 3 Drums, Channel 12 Mic 4, Bus 3 Drum Mon |
| Vardit | magenta (`5`) | Channel 13 Mic 5, Bus 4 Door Mon |
| Moria | cyan (`6`) | Channel 14 Mic 6, Bus 6 future monitor |

## Current Baseline Levels

Applied and independently read back on 2026-07-30:

- Channel main faders 1, 3, 4, 5, and 9–14: unity (`0 dB`).
- Unused channel main faders 2, 6–8, 15, and 16: minimum (`-inf`).
- In every Bus 1–6, channel sends 1, 3, 4, 5, and 9–14: unity (`0 dB`).
- In every Bus 1–6, unused channel sends 2, 6–8, 15, and 16: minimum
  (`-inf`).
- Aux input and FX returns 1–4: minimum (`-inf`) in Main LR and every Bus
  1–6.
- Bus masters 1–6 and Main LR master: unity (`0 dB`).
- Analog headamp gains 1–16: `0 dB`.
- FX-send masters, mutes, EQ, and routing were deliberately left unchanged.

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
