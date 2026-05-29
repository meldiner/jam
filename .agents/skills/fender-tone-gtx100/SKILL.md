---
name: fender-tone-gtx100
description: Control and configure a Fender Mustang GTX100 through the Fender Tone Android app on a USB-connected dedicated Android device. Use when the user wants Codex to pair/connect Fender Tone, inspect presets, select or edit amp/effect signal chains, save presets, troubleshoot Bluetooth/app connection issues, or prepare repeatable GTX100 setup workflows.
---

# Fender Tone GTX100

Use this skill to operate the Fender Tone Android app on a dedicated phone connected by USB/ADB, with the phone handling Bluetooth to the Mustang GTX100.

## Guardrails

- Treat the phone UI as the source of truth. Use screenshots and UI dumps before tapping.
- Do not bypass device security. If the phone is locked, ask the user to unlock it.
- Avoid destructive preset edits until the user has named the exact preset/slot and confirmed the save target.
- Before any significant preset edits, verify there is a recent Fender Tone/GTX backup. If none is visible or the backup age is uncertain, create one in Fender Tone before editing.
- Create a new backup periodically during long editing sessions, especially before changing multiple presets, adding/removing blocks, changing footswitch assignments, or saving over show presets 1-15.
- Before editing, capture a screenshot and UI XML into `/tmp/codex-android/`.
- Run `python3 scripts/tone_adb.py audit-snapshot --label <short-label>` before and after meaningful changes to preserve local evidence of the app state.
- Prefer ADB controls over macOS mouse clicks. Use `scrcpy` only as a monitor/manual override.

## Verified Local Facts

- ADB device serial observed: `R58M70C8J9Y`
- Device model observed: `SM-A105F`
- Android version observed: `10`
- Screen size observed: `720x1520`
- Fender Tone package: `com.fender.tone`
- Launch activity: `com.fender.tone/.MainActivity`
- Fender Tone version observed: `5.1.2.110891`
- Granted permissions observed: Bluetooth, Bluetooth Admin, Fine Location, Coarse Location, Internet.

## Quick Start

Run the helper from this skill directory:

```bash
python3 scripts/tone_adb.py status
python3 scripts/tone_adb.py unlock
python3 scripts/tone_adb.py stay-awake
python3 scripts/tone_adb.py launch
python3 scripts/tone_adb.py monitor --background
python3 scripts/tone_adb.py snapshot
python3 scripts/tone_adb.py ui-text
python3 scripts/tone_adb.py audit-snapshot --label before-edit
```

If `status` shows no device, run:

```bash
adb devices -l
```

If the device is visible to macOS but not ADB, ask the user to enable USB debugging, choose File Transfer / Android Auto, and accept the USB debugging prompt.

## Operating Model

Fender Tone controls Mustang GTX100 over Bluetooth from the Android app. Codex controls the Android phone over USB/ADB:

1. `adb shell monkey -p com.fender.tone -c android.intent.category.LAUNCHER 1`
2. `adb exec-out screencap -p > /tmp/codex-android/screen.png`
3. `adb shell uiautomator dump /sdcard/window.xml`
4. `adb pull /sdcard/window.xml /tmp/codex-android/window.xml`
5. Inspect visible text, content descriptions, and bounds.
6. Tap only after identifying the target from screenshot/UI XML.

## Fast Practice Mode

Use this when the goal is responsive control during rehearsal:

1. Run `python3 scripts/tone_adb.py monitor --background` to open a live `scrcpy` view.
2. Use the `scrcpy` window as the visual source of truth while sending actions through ADB.
3. Prefer helper commands such as `tap`, `swipe`, and `key` for mapped controls.
4. Run `snapshot` only when entering an unmapped screen or when the live view is ambiguous.
5. Run `audit-snapshot --label <label>` before and after meaningful preset edits, backup creation, and any confirmed save.

Keep macOS mouse clicks in the `scrcpy` window as a manual override only. ADB coordinates remain the repeatable control surface, and the coordinate map assumes the phone's native `720x1520` screen.

## Fender Workflow Facts

Load `references/fender-tone-gtx100.md` when planning connection, preset selection, effect editing, or troubleshooting. Core points:

- GTX100 is supported by Fender Tone on iOS/Android via Bluetooth.
- Tone Desktop does not support GTX/GT/Rumble Stage/Studio amps.
- Android 6+ needs location permission enabled for Bluetooth discovery.
- Preset detail view should update the amp in real time.
- Preset detail supports vertical swipes to cycle presets and left swipe to enter the signal chain.
- Effects are added from preset detail/chain item with the lower-left `+`, then Pre-FX or Post-FX, then effect selection and Save.
- Knob/parameter edits are made by selecting a chain item, tapping the knob, and dragging vertically; smaller movement gives finer adjustment.

## App Exploration Protocol

When exploring a new app state:

1. Capture `snapshot`.
2. Read UI text with `ui-text`.
3. If UI XML is sparse, use screenshot inspection and coordinate taps.
4. Record stable labels, content descriptions, and coordinates in `references/app-map.md`.
5. Prefer navigation by labels when `uiautomator` exposes text; otherwise use coordinate taps with screen-size assumptions and recapture after every tap.
6. If the preset badge turns red or Save becomes enabled after exploration, do not tap Save. Force-stop/relaunch Fender Tone to discard unsaved app state unless the user asked to save.

## Backup Protocol

Use this before editing presets on the real amp:

1. Confirm Fender Tone is connected to the intended amp, usually `Mustang GTX #2`.
2. Navigate to the Fender Tone backup/restore area and verify there is a recent backup from the current rehearsal/editing session.
3. If there is no recent backup, create one before making changes.
4. Run `python3 scripts/tone_adb.py audit-snapshot --label backup-verified` to capture local evidence of the connected app state.
5. During long sessions, create another backup after each coherent batch of changes, such as after finishing volume alignment, after adding all solo boosts, or before experimenting with larger tone redesigns.

If backup creation shows `Creating Backup` for more than a few minutes, do not edit presets in that app state. Capture a screenshot, back out or force-stop/relaunch Fender Tone, and verify the amp reconnects before continuing. A failed/stuck backup attempt can leave the app disconnected from the amp.

The helper reads a local `.env` beside this file. Keep secrets there, not in SKILL.md:

```bash
ANDROID_PIN=...
```

## Common ADB Actions

```bash
adb shell input keyevent KEYCODE_HOME
adb shell input keyevent KEYCODE_BACK
adb shell input tap X Y
adb shell input swipe X1 Y1 X2 Y2 DURATION_MS
adb shell input text 'Preset%20Name'
python3 scripts/tone_adb.py monitor --background
python3 scripts/tone_adb.py tap X Y
python3 scripts/tone_adb.py swipe X1 Y1 X2 Y2 DURATION_MS
python3 scripts/tone_adb.py key KEYCODE_BACK
```

For Fender Tone, use `%s` or `%20` for spaces in `adb shell input text` depending on shell quoting behavior; verify the text field after entry.

## Skill Maintenance

Update `references/app-map.md` whenever a stable screen, button, or coordinate is verified on the actual phone. Keep this SKILL.md concise; put detailed UI maps and source notes in `references/`.
