# Jam — band practice chord charts

A static web viewer for displaying chord charts and lyrics during rehearsal.
Replaces a PowerPoint setlist (the original `Guest House.pptx`) with a
single-screen, fullscreen-friendly site.

**Live**: https://meldiner.github.io/jam/ (deploys from `main`, public repo)
**Local**: `python3 -m http.server 8765` from this folder, then http://localhost:8765/

---

## Why this exists

The band used to keep songs in a single PowerPoint deck. Drawbacks:
1. Two views were not possible per song. Some musicians want chord-only
   ("chart"); some want lyrics-with-chords.
2. PPTX requires scrolling for long songs — band members wanted everything
   on one screen.
3. Hard to reorder / hide / edit during practice.
4. No screen-saver suppression, no easy fullscreen.

Goal: a tool that I (Claude) can update *during* practice when the band wants
to add a new song or fix a chord — fast iteration, no deploy step gating.

## Hard requirements (from band discussion)

- **Single page, no scrolling** (Ronen) — fonts auto-shrink to fit any screen.
- **Top-to-bottom reading flow** (Ortal) — sections stack vertically; lyrics
  flow into balanced columns where each column reads top-to-bottom.
- **Reminders for opening cue, ending cue, and BPM** (Ortal) — surfaced in
  the song header along with key + time signature.
- **Form list visible at all times** — left sidebar, large bold font (32–64px,
  weight 800), numbered top-to-bottom.
- **Two views per song**:
  - **Chart**: chord-shape diagrams + section blocks with bar-by-bar
    progressions. No lyrics.
  - **Lyrics**: full lyrics with chord names above syllables, balanced into
    columns (sections never split across columns).
- **Fullscreen + screensaver suppression**: `F` toggles fullscreen; Wake Lock
  API requested when a song is open; `assets/keepawake.mp4` is a silent looped
  video as a wake-lock fallback for browsers without the API.
- **Live editable mid-practice**: paste me a chord-source URL/text, I add a
  song; press `R` to reload the current song's JSON.

## Setlist

Currently tracking **Show 5/29/26** — 13 songs from the Spotify playlist
[06p38NK6BWO8MjW6glhasN](https://open.spotify.com/playlist/06p38NK6BWO8MjW6glhasN).
Songs in the show are tagged with a `show: <position>` field in their JSON
and the index. The picker groups Show songs (with numbered badges and an
accent-color border) above all other songs.

When the playlist changes, update the `show: N` ordering in
`tools/build-songs.py` SONGS list (and rerun the builder).

## File layout

```
index.html              Shell. Loads chord-renderer.js then app.js.
app.js                  Picker + song views, hash routing, keyboard,
                        fullscreen + wake lock.
chord-renderer.js       Inline-SVG chord-diagram renderer + a library
                        of ~80 common chord shapes.
styles.css              All styles. Light/dark via prefers-color-scheme;
                        body.theme-light / body.theme-dark for override.
assets/keepawake.mp4    Silent looped video used as a wake-lock fallback.

songs/
  index.json            { setlist: "...", songs: [{slug,title,artist,...,show?}] }
  <slug>.json           Per-song data.

tools/
  build-songs.py        Reads pptx slide XML + applies overrides from
                        song-charts.py to write all songs/*.json.
  song-charts.py        Hand-curated chord chart data per song (chartChords,
                        chartSections, formSteps).
```

## Per-song JSON schema

```jsonc
{
  "title": "Song Title",
  "artist": "Artist",
  "key": "A major",
  "bpm": 124,
  "timeSig": "4/4",
  "opening": "Drums + bass groove",       // Ortal's opening cue
  "ending":  "End on A",                   // Ortal's ending cue
  "form": "Intro → Verse → Chorus → ...",  // legacy; superseded by formSteps
  "formSteps": ["Intro", "Verse 1", "Chorus", "..."],   // sidebar list
  "dir": "ltr" | "rtl",                    // text direction for Hebrew songs

  // Chord row in chart view — array of names looked up in ChordRenderer.lib.
  // (Legacy: object form { name: { frets, barre } } also supported, used
  //  by vampire.json which predates the library.)
  "chords": ["A", "E", "F#m", "D", ...],

  // Optional per-song chord-shape overrides.
  "chordShapes": { "F": { "frets": [...], "barre": {...} } },

  "sections": [
    {
      "name": "Verse",
      "reps": "8 bars",                    // optional repetition note
      "lines": [
        ["A", "E", "F#m", "D"],            // each entry = one bar
        ["A", "E", "F#m", "D7"]            // multi-chord per bar: "Cm Gm"
      ]
    }
  ],

  // Lyrics view. Each section's lines support two formats:
  //   - String:  "[A]used to be [E]spontaneous"  (chord markers inline)
  //   - Object:  { "chords": ["A","E","F#m"] }   (chord-only run)
  "lyrics": [
    {
      "section": "Verse 1",
      "dir": "rtl",                         // optional per-section override
      "lines": [
        "[A]used to be [E]spontaneous",
        { "chords": ["A","E"] }
      ]
    }
  ],

  "show": 1   // optional — position in the current setlist (1-indexed)
}
```

## Workflow

### Adding a new song

1. Add an entry to `SONGS` in `tools/build-songs.py` (slug, title, artist,
   key, bpm, time, opening cue, ending cue). Use `skipParse: True` for
   non-pptx songs.
2. If you have chord chart data (sections + chord row), add a `CHARTS`
   entry in `tools/song-charts.py` keyed by slug.
3. `python3 tools/build-songs.py`
4. Reload the picker (Esc from any song). The new card appears.

### Fixing a song mid-practice

- Edit `songs/<slug>.json` directly → press `R` in the browser.
- For changes that should survive rebuilds, also update
  `tools/song-charts.py` (or the SONGS list) and rerun the builder.

### Pushing changes to the public site

```
git add -A && git commit -m "..." && git push
```
Pages rebuilds in ~30s. Public URL: https://meldiner.github.io/jam/

## Keyboard shortcuts

| Key | Action |
|---|---|
| `F` | Toggle fullscreen |
| `L` / `C` | Switch to lyrics / chart view |
| `←` / `→` | Previous / next song (wraps) |
| `R` | Reload the current song's JSON from disk |
| `T` | Cycle theme (system → dark → light → system) |
| `S` / `Esc` | Back to picker |

## Routing

Hash-based, bookmarkable:
- `#`              → picker
- `#<slug>`        → song, chart view
- `#<slug>/lyrics` → song, lyrics view

## IP / copyright notes

The skill `band-practice-chord-chart.skill.md` (kept in this repo for
reference) has a hard "no lyrics" rule — every chart in that skill's intended
output is chord-only. This project deliberately overrides that rule for
**personal band rehearsal use** because the band wants the lyrics view.

The repo is **public** (required for free GitHub Pages). Lyrics in the
`songs/*.json` files are publicly indexable. If this becomes a concern,
options:
- Move to a private repo with paid GitHub Pages (Pro), or alternative free
  hosting that supports private repos (Cloudflare Pages, Netlify, Vercel).
- Strip lyrics from the public files and keep them in a separate
  `.gitignored` overlay loaded at runtime.
- Replace lyrics with the cue-sheet format from the skill (chord-only).

`Guest House.pptx` is intentionally `.gitignore`d — the JSON files are the
new source of truth.

## Songs without source material

These are title-only stubs in the original pptx (or new additions) and
have no chord chart yet. Paste me a chords URL or text and I'll fill them
in: `yehudim-kah-oti`, `ksheze-amok`, `ani-taluy`, `parperei-titua`,
`shir-hamakolet`, `yeled-mizdaken`, `mishehu`, `nitzotzot`,
`hamimut-holefet`, `hacheder-haintimi`, `or-hayareach`, `mehapes-tshuva`,
`one-way-or-another`, `smooth`, `valerie` (has stub).

## Things that are intentionally not done

- **Strumming patterns** — none of the existing source material had them.
- **Tab/notation** — out of scope. Slide 20 had a fingerpicking tab; that
  data is dropped.
- **Setlist editor in the UI** — for now, setlists are edited in
  `tools/build-songs.py` (the `show: N` field). UI editing would mean
  per-user state management.
- **Multi-setlist support** — only one current setlist (`SHOW_NAME`). When
  the band has another show, generalize `show` into `setlists: [{name,
  position}]`.
