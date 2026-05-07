---
name: band-practice-chord-chart
description: Generate single-page HTML chord charts for band practice from a song's chord-and-lyrics source. Use when the user wants a chart they can display on a TV/laptop/iPad during rehearsal without scrolling, or asks to convert a chords page (Ultimate Guitar, GuitarTuna, e-chords, etc.) into a single readable slide. Output is a fullscreen-friendly HTML file with chord-shape diagrams across the top and section-by-section progression blocks below — never lyrics.
---

# Band-Practice Chord Chart

A skill for turning chord/lyrics song sources into a single-page HTML chart optimized for band rehearsal: visible from across the room, no scrolling, no lyrics.

## When to use

- User pastes or links to a chords-with-lyrics page and wants it "on one screen for band practice"
- User asks for a "chord chart," "cheat sheet," or "single-page" version of a song
- Goal is rehearsal use (TV, laptop, iPad on a stand) — not learning the song from scratch

## When NOT to use

- User wants chords-with-lyrics formatting → that's a copyright issue; offer this skill as the alternative
- User wants tablature, sheet music, or note-by-note notation → different deliverable
- User wants a chord progression for analysis only → just answer in chat

## Hard rule: no lyrics

Never reproduce lyrics in the output, not even fragments above chord changes. The chart shows:
1. Chord-shape diagrams (a row of SVG fretboards)
2. Section names with bar-by-bar chord progressions in `| Cm | Gm | Fm | Bb |` notation
3. A one-line song form at the bottom (Intro → Verse → Chorus → …)

If the user asks to add lyrics, decline and remind them why — paraphrasing or restructuring lyrics around chords is still reproduction.

## Output structure

A single self-contained HTML file at `/mnt/user-data/outputs/{song-slug}-chord-chart.html`:

- **Header**: Song title + artist, key, BPM, time signature
- **Chord row(s)**: SVG diagrams for every unique chord in the song. Up to ~7-8 chords fits one row; beyond that, split into two rows grouped semantically (e.g., "verse/chorus core" + "bridge accidentals")
- **Sections grid**: 2×2 grid of section blocks (Intro, Verse, Chorus, Bridge, etc.) with bar-line notation
- **Form line**: A single horizontal strip at the bottom showing the song's order of sections

## Layout sizing

Use viewport units (`vh`/`vw`) and `clamp()` so the layout fills any screen when fullscreened (F11 / ⌃⌘F). Reference values that have worked:

```css
.title { font-size: clamp(22px, 3.2vw, 40px); }
.bars  { font-size: clamp(18px, 2.4vw, 32px); }
.tag   { font-size: clamp(13px, 1.3vw, 18px); }
```

Body should be `display: flex; flex-direction: column` with `height: 100%` so sections grow to fill vertical space. Mobile fallback: `@media (max-width: 700px)` collapses sections grid to one column and chord row to fewer columns.

## Chord diagram rendering

Self-contained inline SVG, no external library. The data structure:

```js
const chordData = {
  Cm: { frets: ['x',3,5,5,4,3], barre: { fret: 3, from: 1, to: 5 } },
  Gm: { frets: [3,5,5,3,3,3],   barre: { fret: 3, from: 0, to: 5 } },
  C:  { frets: ['x',3,2,0,1,0] },  // open chord, no barre
  // ...
};
```

- `frets` array is low-E → high-E (6 entries). Use `'x'` for muted, `0` for open, integer for fretted.
- `barre` is optional. `from`/`to` are string indices (0 = low E, 5 = high E).
- Renderer auto-decides whether to show the nut or shift up the neck (with a `Nfr` label) based on the lowest played fret and presence of open strings.
- Diagrams that need shifting (e.g., Eb at 6th fret) render correctly without manual intervention.

The render function (see existing artifacts for full code) takes a chord name and data object and returns an SVG string. Append to `.chords-row` containers via JS at page load.

## Theme tokens

Both light and dark modes via `prefers-color-scheme`. Token names map to the visualizer system but inlined as CSS custom properties so the file works standalone:

```css
:root {
  --bg:#fafaf7; --surface:#ffffff; --surface-2:#f1efe8;
  --text:#2c2c2a; --text-2:#5f5e5a; --text-3:#888780;
  --border:rgba(0,0,0,0.12);
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg:#1c1c1b; --surface:#262624; --surface-2:#2c2c2a;
    --text:#f1efe8; --text-2:#b4b2a9; --text-3:#888780;
    --border:rgba(255,255,255,0.15);
  }
}
```

## Bar notation conventions

- `| Cm | Gm | Fm | Bb |` — pipes separate bars, one chord per bar by default
- Two chords in a bar: `| Cm Gm |` (space-separated, same bar)
- Repeated 4-bar phrase: write once, label `×2` in the section tag's right side
- Section tag right side also fits "4 bars", "10 bars", etc. for clarity

## Workflow

1. Parse the user's source (pasted text or URL fetch). If URL fetch fails (UG returns 403), search for the song's structure across e-chords, chords-and-tabs, hooktheory, etc., and reconcile.
2. **Verify the key against music-theory plausibility**. If a source lists `Bm` in F major, suspect it's `Bbm` (borrowed iv) and confirm with the user. The vampire chart caught exactly this — every Bm was actually Bbm.
3. **Respect the user's key choice**. If they link a transposed version, ask before transposing. Default to original recording key unless told otherwise.
4. Build the widget version inline first (`visualize:show_widget`) for quick preview.
5. Then write the standalone HTML file to `/mnt/user-data/outputs/` and call `present_files`.
6. Note any simplifications in the response (collapsed repeated phrases, dropped duplicate verse lines, etc.) so the user can flag corrections.

## Style for the response

Brief. Lead with the chart. Follow with a short bulleted list of design decisions worth flagging (key, repeated sections, anything the user might want to override). Offer 2-3 concrete next-step modifications: transpose, add strumming pattern, expand specific sections, simplify chord row.

## Songs done so far

- **vampire (Olivia Rodrigo)** — F major, 7 chords. User caught Bm→Bbm error; correction was harmonically obvious (borrowed iv from F minor). Final: F, A, Bb, Bbm, Gm, C7, C.
- **Don't Speak (No Doubt)** — C minor verse modulating to F minor chorus, 12 chords across two rows. Pre-chorus is the last 3 bars of verse 3 (`Eb Bb C` lift). Solo reuses verse loop ×3, no separate block. Original key, not transposed.

## Known pitfalls

- **Copyright via "summary" loophole**: Don't paraphrase lyrics tightly above chords either. The chart format exists specifically to avoid this.
- **Barre chord shapes for `Bb` vs `Bbm`**: differ only in the high-G string fret (3 vs 2). Easy to mistype.
- **`Db` and `C#` are enharmonically equivalent**; some sources mix them within the same chart. Pick one spelling per chart for readability — usually whatever fits the key signature (Db in F minor, C# in A major).
- **Ultimate Guitar fetches return 403**. Fallback: web_search the song, cross-reference 2-3 sources.
- **Don't end on the chord row**. Always include the form line at the bottom — band members orient by section order more than by chord shapes during practice.

## Future enhancements to consider

- Strumming pattern row per section (eighth-note grids)
- Capo position note in the header
- Per-section tempo markings if song has tempo changes
- Print stylesheet (`@media print`) sized to letter/A4 landscape
- Multi-song setlist view: each song as a tab or page-break-separated chart
