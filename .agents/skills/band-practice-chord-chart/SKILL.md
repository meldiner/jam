---
name: band-practice-chord-chart
description: Add, fix, or regenerate songs for the Jam static band-practice chord chart viewer. Use when the user pastes a chord source URL/text, asks to add a song, correct chords, update the show order, rebuild song JSON, or prepare rehearsal-friendly chart/lyrics data for this repo.
---

# Band-Practice Chord Chart

Use this skill for work in the Jam repo: a static, fullscreen-friendly chord
chart and lyrics viewer used during band rehearsal.

## Core Model

- Runtime data lives in `songs/*.json` and `songs/index.json`.
- Durable generated data comes from `tools/build-songs.py` and
  `tools/song-charts.py`.
- `songs-local/` is gitignored and may contain local-only overlays such as
  lyrics or slide images that should not be published.
- The app is plain HTML/CSS/JS. There is no build step for the viewer.

## Local Workflow

Run from the repo root:

```bash
python3 -m http.server 8765
```

Then open `http://localhost:8765/`.

After editing song source data, rebuild generated JSON with:

```bash
python3 tools/build-songs.py
```

In the browser, press `R` while viewing a song to reload the current song JSON.
Press `Esc` or `S` to return to the picker.

## Adding A Song

1. Add the song metadata to `SONGS` in `tools/build-songs.py`.
2. Use `skipParse: True` for songs that are not backed by the original PPTX
   slide XML.
3. Add chart data in `tools/song-charts.py` under `CHARTS[slug]`:
   `chartChords`, `chartSections`, and `formSteps`.
4. Run `python3 tools/build-songs.py`.
5. Inspect the generated `songs/<slug>.json` and `songs/index.json`.
6. Verify in the browser when layout or display behavior changed.

## Fixing A Song

- For fast practice-time fixes, edit `songs/<slug>.json` directly and press
  `R` in the browser.
- For fixes that must survive regeneration, update `tools/song-charts.py` or
  the song's entry in `tools/build-songs.py`, then rerun the builder.
- If a chord shape is missing from the chart view, add a common reusable shape
  to `chord-renderer.js` or a song-specific override in `chordShapes`.

## Chart Data Conventions

- `chartChords` controls the chord diagram row.
- `chartSections` is a list of section blocks. Each `lines` entry is a row of
  bars, and each bar is a string such as `"Am"`, `"C G"`, or `"N.C."`.
- `formSteps` controls the always-visible left sidebar. Keep labels short and
  performance-oriented.
- Use musically consistent enharmonic spelling within a song. Prefer spelling
  that fits the key or the source chart.

## Lyrics Data

This repo intentionally supports a lyrics view for personal rehearsal use.
Lyrics in tracked `songs/*.json` files are public because the repo deploys via
public GitHub Pages. If that matters for a song, keep sensitive or local-only
lyrics in `songs-local/<slug>.json` instead of tracked files.

Lyrics lines support inline chord markers:

```json
"[A]used to be [E]spontaneous"
```

Chord-only lyric runs use:

```json
{ "chords": ["A", "E"] }
```

## Layout Requirements

- Single screen, no scrolling during song display.
- Chart and lyrics views must shrink to fit the viewport.
- Song sections should read top-to-bottom.
- Lyrics columns should be balanced without splitting sections across columns.
- The form list must remain visible in the left sidebar.
- The song header should surface key, BPM, time signature, opening cue, and
  ending cue when available.

## Current Show Order

The active setlist is controlled by `show: N` values in `tools/build-songs.py`
and reflected into `songs/index.json`. When the show order changes, update the
`SONGS` list and rerun `python3 tools/build-songs.py`.

## Verification

For data-only edits, at minimum run:

```bash
python3 tools/build-songs.py
```

For UI, layout, routing, keyboard shortcut, fullscreen, or fitting changes,
serve the site locally and inspect both chart and lyrics views at desktop and
mobile-ish widths.
