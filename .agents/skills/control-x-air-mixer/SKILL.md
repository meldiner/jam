---
name: control-x-air-mixer
description: Inspect and safely control Behringer X AIR or Midas M AIR digital mixers directly over their OSC-compatible UDP protocol. Use when Codex needs to discover an XR18/X18/XR16/XR12/MR18/MR12, read mixer state, label channels or buses, build repeatable rehearsal mixer workflows, or extend direct control for faders, monitor sends, mute, EQ, routing, snapshots, gain, or phantom power.
---

# Control X AIR Mixer

Control the mixer directly over the local network instead of automating X AIR Edit. Use the bundled helper for deterministic OSC packet handling and verified writes.

## Guardrails

- Treat the mixer as a live audio system. Read the current value before every write and verify the value afterward.
- Do not write unless the user explicitly requested the exact change. A request to inspect, diagnose, or explain authorizes read-only operations only.
- Use only typed, validated write commands exposed by `scripts/xair_osc.py`. Do not improvise raw write packets during rehearsal.
- Treat faders, mute, sends, EQ, dynamics, gain, phantom power, routing, snapshot recall, initialization, and firmware operations as live-audio changes. Add a validated helper command before controlling any of them.
- Require an explicit target and value immediately before changing gain, phantom power, routing, snapshot state, or mixer initialization. Warn that these can create feedback, silence outputs, damage connected equipment, or overwrite working state.
- Never expose UDP port 10024 to the public Internet. Use it only on the trusted mixer LAN.
- X AIR Edit may remain open, but the console is authoritative. Re-read state after any app or direct-protocol change.

## Quick Start

Run from this skill directory. Override the default rehearsal-mixer address with `--host` or `XAIR_HOST`.

```bash
python3 scripts/xair_osc.py self-test
python3 scripts/xair_osc.py --host 192.168.1.149 probe
python3 scripts/xair_osc.py --host 192.168.1.149 get /ch/01/config/name
```

`probe` and `get` are read-only.

## Label Workflow

Always preview first. The preview reads the current name and emits a JSON plan without changing the mixer:

```bash
python3 scripts/xair_osc.py --host 192.168.1.149 label-channel 1 Bass
python3 scripts/xair_osc.py --host 192.168.1.149 label-bus 1 "Desk L"
```

After comparing `before` and `requested`, apply only with explicit user authorization:

```bash
python3 scripts/xair_osc.py --host 192.168.1.149 label-channel 1 Bass --apply
python3 scripts/xair_osc.py --host 192.168.1.149 label-bus 1 "Desk L" --apply
```

The helper refuses invalid channel/bus numbers and names longer than 12 characters. An applied write succeeds only after the mixer returns the requested value.

## Color Workflow

Channel and bus scribble strips support the standard colors `off`, `red`,
`green`, `yellow`, `blue`, `magenta`, `cyan`, and `white`. Preview first, then
apply only after explicit authorization:

```bash
python3 scripts/xair_osc.py --host 192.168.1.149 color-channel 1 red
python3 scripts/xair_osc.py --host 192.168.1.149 color-bus 5 red
python3 scripts/xair_osc.py --host 192.168.1.149 color-channel 1 red --apply
python3 scripts/xair_osc.py --host 192.168.1.149 color-bus 5 red --apply
```

Color commands read the current integer value first and verify the requested
value after every applied write.

## Fader And Gain Workflow

Fader commands intentionally expose only `unity` (`0 dB`) and `minimum`
(`-inf`) positions. Headamp gain accepts `-12` through `+60 dB` in `0.5 dB`
steps. Preview every target first:

```bash
python3 scripts/xair_osc.py --host 192.168.1.149 set-channel-fader 1 unity
python3 scripts/xair_osc.py --host 192.168.1.149 set-bus-fader 1 unity
python3 scripts/xair_osc.py --host 192.168.1.149 set-main-fader minimum
python3 scripts/xair_osc.py --host 192.168.1.149 set-headamp-gain 1 0
python3 scripts/xair_osc.py --host 192.168.1.149 set-channel-bus-send 1 1 unity
python3 scripts/xair_osc.py --host 192.168.1.149 set-return-fader aux minimum
python3 scripts/xair_osc.py --host 192.168.1.149 set-return-bus-send 1 1 minimum
```

Use `--apply` only after showing the exact targets and values to the user and
receiving explicit authorization. Raising faders to unity can create feedback
or a sudden loud output. Setting headamp gain to `0 dB` can silence low-level
microphones until gain is rebuilt during soundcheck.

## Operating Workflow

1. Run `self-test` after changing the helper.
2. Run `probe` and verify mixer name, model, firmware, and IP before a session.
3. Read every target path before planning a change.
4. Show the user the exact target paths, current values, and proposed values for live-audio changes.
5. Apply only the authorized operations.
6. Re-read and report the verified final values.
7. Stop on timeout, model/IP mismatch, an unexpected current value, or failed verification. Do not retry writes blindly.

## Extending Control

Read `references/protocol.md` before adding commands or paths. Add narrow subcommands with:

- strict target/range validation;
- dry-run as the default for writes;
- read-before-write and post-write verification;
- JSON output suitable for audit and comparison;
- no third-party runtime dependency unless the standard library is insufficient.

Do not add a general-purpose raw `set` command. Prefer a dedicated command such as `set-channel-fader` whose value conversion and safety behavior can be tested.

## Maintenance

Keep protocol details and observed mixer facts in `references/protocol.md`. Keep this file focused on safe operating procedure. Run the skill validator after meaningful edits.
