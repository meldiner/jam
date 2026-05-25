# Fender Tone App Map

This file is updated from empirical ADB exploration on the dedicated Android phone.

## Device

- Serial: `R58M70C8J9Y`
- Model: `SM-A105F`
- Android: `10`
- Screen: `720x1520`
- Package: `com.fender.tone`
- Activity: `com.fender.tone/.MainActivity`
- App version: `5.1.2.110891`

## Current Status

- ADB control verified: `adb devices -l`, `getprop`, `screencap`, `uiautomator dump`, and `KEYCODE_HOME`.
- Unlock helper verified using local `.env`.
- Fender Tone UI is mostly not exposed through `uiautomator`; use screenshots and coordinates.
- Fender Tone launched to `My Presets`, with slot `01 Charlie` selected.
- Signal-chain editor and block detail views mapped below.
- Force-stop/relaunch discarded exploration state and returned to `Connect to Device` scanning, then preset `01 Empty`.

## Safety Notes

- Do not tap `Save` unless the user explicitly confirms the target preset/slot.
- Opening Add Block and selecting an insertion point can turn the preset badge red / enable `Save` even before confirming a new effect. Back out and force-stop/relaunch to avoid saving accidental state.
- Fender Tone may reconnect to the amp and show the currently active amp slot, which can differ from the previously visible `My Presets` list.

## Stable Commands

```bash
adb shell monkey -p com.fender.tone -c android.intent.category.LAUNCHER 1
adb exec-out screencap -p > /tmp/codex-android/fender-tone.png
adb shell uiautomator dump /sdcard/window.xml
adb pull /sdcard/window.xml /tmp/codex-android/window.xml
adb shell input keyevent KEYCODE_BACK
adb shell input keyevent KEYCODE_HOME
```

## Screens To Map

- Launch/onboarding/account screen: not yet seen.
- Amp connect / Bluetooth scan screen: title `Connect to Device`, spinner, bottom `SCANNING...`; app auto-advanced after several seconds.
- My Presets list: mapped.
- Preset detail: list row itself did not open detail; edit/pencil icon opens signal chain.
- Signal chain: mapped.
- Add effect drawer/menu: insertion and category picker mapped.
- Amp model selection: not mapped.
- Save/rename preset flow: not mapped.
- Settings / My Amps / Wi-Fi / Backup-Restore: not mapped.

## Coordinate Map at 720x1520

### My Presets

Seen screen: `/tmp/codex-android/fender-tone-unlocked.png`

- Top back: `(48,92)`
- Favorite star: `(146,92)`
- Preset number badge: `(226,92)`
- Save: `(594,92)`
- Settings gear: `(678,92)`
- Section collapse `MY PRESETS`: `(66,173)`
- Search: `(506,174)`
- Add new preset: `(637,174)`
- Current row `01 Charlie`: bounds roughly `x=7..700, y=219..316`
- Current row overflow/menu dots: `(506,268)`
- Current row edit/signal-chain pencil: `(635,268)`
- Bottom tabs:
  - My Presets: `(135,1410)`
  - Favorites: `(285,1410)`
  - Setlists: `(435,1410)`
  - Cloud: `(585,1410)`

### Signal Chain

Seen screen: `/tmp/codex-android/charlie-edit-or-detail.png`

- Chain shown for `01 Charlie`: Overdrive -> Simple Comp -> `'65 Twin` amp -> `'65 Spring Reverb`.
- Overdrive block center: `(292,370)`
- Simple Comp block center: `(426,370)`
- Amp block center: `(360,765)`
- Reverb block center: `(360,1160)`
- Add Block control: `(350,1440)`
- Tempo/BPM control: `(600,1440)`, displayed `120 BPM`
- Back to preset list: `(48,92)`

### Amp Block Detail

Seen screen: `/tmp/codex-android/charlie-amp-block.png`

- Amp model: `'65 Twin`; cabinet: `'65 Twin`.
- Visible knobs:
  - Gain: `(80,810)`, observed value after tap: `5.8`
  - Volume: `(220,810)`
  - Treble: `(360,810)`
  - Middle: `(500,810)`
  - Bass: `(640,810)`
- Bottom `Amp Settings`: `(80,1440)`
- Bottom `Replace`: `(640,1440)`
- Tapping a knob opens a right-side parameter drawer.

### Parameter Drawer

Seen screen: `/tmp/codex-android/charlie-gain-control.png`

- Drawer opens from right side.
- Example: `GAIN 5.8`
- Minus control: `(306,1440)`
- Plus control: `(640,1440)`
- Use `KEYCODE_BACK` to close without editing.

### Add Block Flow

Seen screens:

- `/tmp/codex-android/add-block-picker-2.png`
- `/tmp/codex-android/add-block-category.png`

Process:

1. From signal chain, tap Add Block `(350,1440)`.
2. App shows `Select Node To Add` and plus insertion points.
3. Example insertion points:
   - Before Overdrive: `(222,370)`
   - Between Overdrive/Simple Comp: `(360,370)`
   - After Simple Comp: `(498,370)`
   - Around amp/reverb sections also expose plus points.
4. After selecting insertion point, app shows `Add` with category tabs:
   - STOMP
   - MOD
   - DELAY
   - REVERB
   - DYN + EQ
   - FILT + PITCH
5. Example selected stomp model: `Ranger Boost`.
6. `Confirm` is at top right `(632,92)`. Do not tap unless user asked to add this block.
