# Amp Presets for Show 2026-05-29

Working notes for the Fender Mustang GTX 100 presets used for the 5/29/26
show. Presets 1-15 are intended to match the show song order.

These notes are based on:

- The show order in the Jam repo.
- Spotify setlist source:
  https://open.spotify.com/playlist/06p38NK6BWO8MjW6glhasN
- Ronen's stated guitar and parts.
- Visual review of Fender Tone over screen sharing.
- The earlier tone-design discussion.
- Rehearsal feedback from 2026-05-24 after starting volume alignment across
  the 15 show presets.

Some current setup details are inferred visually from Fender Tone icons. Exact
effect names/settings should be verified by opening each block in the app.

## Rig Context

- Amp: Fender Mustang GTX 100.
- Guitar: Fender American Professional II.
- App/device status seen in Fender Tone: connected to `Mustang GTX #2`.
- Global EQ seen in Fender Tone: `Bright Cut`.
- `Bright Cut` is a good global choice for the American Professional II because
  it helps keep Fender single-coil brightness from becoming sharp through the
  GTX speaker.

## Show Preset Map

| Preset | Song | Notes |
|---:|---|---|
| 1 | Charlie | Ronen has a solo. |
| 2 | Ah ah ah | Clean/pop rhythm target. |
| 3 | Ahava hadasha | Clean/chorus-friendly target. |
| 4 | Vampire | Needs B-flat and B changes reflected in chart later. |
| 5 | Boots | Needs chart/chord feedback later; not part of amp note. |
| 6 | Valerie | Clean compressed funk/soul target. |
| 7 | Parparim | Ronen only plays chorus/elevation, then ending solo with phaser. |
| 8 | Ha'Makolet | Clean/crunch rhythm target. |
| 9 | Mishu | Needs boost for the dramatic second part. |
| 10 | Blues Cnaani | Blues-rock target. |
| 11 | Kach Oti / Take Me | Dirty rhythm, solo 1 bigger, solo 2 wah screaming dirty solo. |
| 12 | All The Small Things | Marketplace Blink 182 sound used as baseline. |
| 13 | Ito Lanetzach / Kerach 9 | British rhythm crunch was the original target. |
| 14 | Nitzotzot | Ronen has a solo. |
| 15 | Ha'Perach | Wah pedal used for funky rhythm guitar. |

## General Design Principles

- Current broad direction after rehearsal: make the guitar sound bigger across
  the board, while still level-matching presets rather than simply making every
  patch louder.
- Do not make every preset louder or gainier than the previous one. Level-match
  across the set first, then add controlled boosts for leads.
- For solos, prefer a combination of mids, slight volume lift, sustain, and
  short delay over simply adding more gain.
- For the American Professional II, keep treble/presence under control. The
  global `Bright Cut` helps, but individual presets may still need less top end.
- Because the guitar can sound thin in this rig, it is acceptable to add
  body-shaping blocks such as EQ, compression, clean boost, or other pedals
  when they make the guitar feel larger and more stable in the band mix.
- For wah-heavy parts, avoid excessive pre-wah gain or sharp treble. The wah
  already adds strong resonant peaks.
- For pop-punk rhythm, tightness matters more than maximum distortion. Gate,
  lower gain, and small room ambience are usually more useful than huge reverb.

## Rehearsal Feedback 2026-05-24

- Volume alignment across presets 1-15 has started.
- The guitar needs to sound bigger across the board. Candidate fixes: more
  body/low-mid support, better ambience, controlled compression, and slightly
  wider/deeper post effects where appropriate, not just more output level.
- Boots has a guitar solo and needs a boost pedal/footswitchable lift.
- Mishehu Mipaam / Mishu boost is not powerful enough; make the second-part
  lift bigger, wider, and more dramatic in the band mix. This does not
  necessarily mean dirtier.
- All The Small Things sounds too dry; add reverb, room ambience, or another
  subtle post effect so it feels less flat without losing pop-punk tightness.
- A backup was created before these next changes. Future significant edits
  should verify/create a fresh backup first.

## Implemented Edits 2026-05-25

- Preset 05 `Boots`: added `Ranger Boost` before the amp for the solo. Set
  Ranger Boost Level to `7.0` and Gain to `4.0`, then saved back to slot 05.
- Preset 09 `Mishu`: raised `Tube OD` Level from `4.0` to `7.0` for a bigger
  second-part lift. Left Drive at `4.2` so the boost is more dramatic without
  simply becoming dirtier, then saved back to slot 09.
- Preset 12 `Blink 182 Tone`: added `Small Hall Reverb` after the amp and left
  its Level at the default observed value of `4.9`, then saved back to slot 12.
  This should make the sound less dry while preserving pop-punk tightness.
- Preset 08 `Ha'Makolet`: added `Simple Compressor` before the amp, then saved
  back to slot 08. This is a conservative body/stability change for a patch
  that was just amp plus `Small Hall Reverb`.
- Preset 13 `Kerach 9`: added `Simple Compressor` before the amp, then saved
  back to slot 13. This is the same body/stability treatment for a patch that
  was just amp plus spring reverb.
- No new backup was created during this batch because Ronen confirmed the amp
  was reconnected and explicitly said to proceed without creating a backup.

## Full Setup Audit 2026-05-25

- The stronger and less-thin architectures already tend to include front-end
  compression, EQ, boost, or drive: `01 Charlie`, `03 Ahava hadasha`,
  `06 Valerie`, `07 Parparim`, `09 Mishu`, `10 Blues Cnaani`, `11 Take Me`,
  and `14 Nitzotzot` based on visible/audited chain families.
- The patches most likely to sound small/thin are the ones built mostly as
  amp plus reverb: `08 Ha'Makolet`, `12 Blink 182 Tone`, and `13 Kerach 9`.
  `12` now has post-amp reverb for space; `08` and `13` now have front-end
  compression for body.
- `05 Boots` now has Ranger Boost for the solo, but still needs rehearsal
  validation for whether the base tone is twangy/full enough.
- For the next body pass, prefer adding or tuning EQ/compression/clean boost
  before changing amp gain. The goal is more dominance, body, and stability in
  the band mix, not just more distortion.

## Current Review Table

| # | Song / Preset | Initial Intuition | Current Setup Observed | Recommendation After Review | Song Notes / Improvements |
|---:|---|---|---|---|---|
| 1 | Charlie | Fender clean/blues base, light drive, slap or spring, solo boost. | Red drive/boost into blackface Fender-style combo, then post effect. | Keep the base. Make the red pedal a footswitchable solo lift with mids, small volume bump, and maybe short delay. | Ronen has a solo. Do not rely on gain alone for the solo; it needs to cut. |
| 2 | Ah ah ah | Clean Fender rhythm, light compression, possible trem or plate. | Looked very similar to preset 1: red pre effect into blackface Fender-style combo, then post effect. | Safe as a clean rhythm preset. Differentiate from Charlie with less gain, more clean headroom, or trem/plate if desired. | If it feels samey in rehearsal, make this the cleaner/lighter preset. |
| 3 | Ahava hadasha | Clean pop/funk base: Twin, Deluxe, or JC-120 style; compression; subtle chorus or delay. | Blue pre effect into `80s British` style amp, then green effect. | This is probably the biggest mismatch. Move toward a cleaner Twin/JC/Deluxe base unless a rockier interpretation is intentional. | Watch brightness and hard upper mids with the American Professional II. |
| 4 | Vampire | Edge-of-breakup Deluxe-style tone with optional gain lift for bigger sections. | Amp/head first, then red effect, then purple effect. No obvious pre-amp drive visible in the chain. | Verify whether the amp gain supplies the dirt. If not, add or move a light OD/boost before the amp. | Chart feedback from rehearsal says `Bb` and `B` are relevant later, but this note is for amp setup only. |
| 5 | Boots | Clean twang: Twin or Dual Showman, slapback delay, spring reverb, low gain. | Ranger Boost into amp/head, then Large Plate. Ranger Boost set to Level `7.0`, Gain `4.0`. | Rework cleaner and twangier if this is meant to feel like the record. The solo boost is now present; verify it lifts without harshness at rehearsal volume. Use slapback and spring, not heavy rock gain, if the base still needs to move closer to the record. | Rehearsal update: Ronen has a solo. Later chord-sheet feedback says chart needs correction; amp target remains clean/twang with a solo lift. |
| 6 | Valerie | Clean compressed funk/soul rhythm; low drive; tight bass. | Blue pre effect into tweed/Fender-style combo, then purple post effect. | Close to target. Keep drive low, bass tight, and compression controlled. | Should sit well if the blue block is compression or mild drive. |
| 7 | Parparim | Earlier intuition was medium British/art-rock crunch plus solo boost. | Blue plus green pre effects into higher-gain amp/head. | Current heavier setup makes sense because Ronen only enters for chorus/elevation. Add/assign phaser for the ending solo. | Ronen only plays chorus and brings rock/grit/elevation. Ending solo should use phaser. Use moderate phaser rate/depth so pick attack remains clear. |
| 8 | Ha'Makolet | Fender clean/crunch, light compression or low OD, spring/plate ambience. | Simple Compressor into tweed/Fender-style combo, then Small Hall Reverb. | Body pass applied. Verify that the compressor makes the guitar feel larger without flattening the groove. If still thin, use EQ/clean boost before adding dirt. | Keep it practical and level-matched. |
| 9 | Mishu / Mishehu Mipaam | Clean expressive base with dedicated dramatic boost for second part. | Tube OD into clean Fender-style combo, then post effect. Tube OD Level raised to `7.0`; Drive left at `4.2`. | Good architecture, and the boost is now larger without simply adding dirt. If it still needs more drama at rehearsal volume, add width with short delay/reverb lift or mids rather than more Drive first. | Ronen needs a bigger boost for the second dramatic part. Verify it cuts clearly at rehearsal volume without becoming harsh or over-gained. |
| 10 | Blues Cnaani | Bassman/blues-rock drive, tape/spring feel, optional boost. | Two front-end pedals into an amp head. | Good blues-rock layout. Use one pedal for always-on edge and the other for lift. Watch compression/noise. | Avoid over-compressing the rhythm part. |
| 11 | Kach Oti / Take Me | Original intuition was British/Jubilee/80s-style lead with boost/gate. | Drive pedal into clean Fender-style combo, then post effect. | Revised target: slightly dirty base with reverb and slight delay for most of the song. Solo 1 should add bigger sustain/presence. Solo 2 is wah-led, so keep patch dirty and vocal but not fizzy. | Ronen needs slightly dirty sound with reverb/slight delay for most of song. End has solo 1 bigger sound, then solo 2 with wah pedal for screaming dirty solo. |
| 12 | All The Small Things / Blink 182 Tone | Tight pop-punk: high-gain British/EVH-style amp, gate, tiny room. | Marketplace `Blink 182 Tone`; EVH-style high-gain amp block with `Small Hall Reverb` added post-amp, Level observed at `4.9`. | Keep marketplace preset as baseline. Reverb is now present; verify it removes dryness without softening palm-muted rhythm. If too wet, lower Level before changing the amp. Also check noise gate, gain not too high, and level matching. | This was intentionally picked from Fender online sounds marketplace. Do not over-customize; make it bigger/less dry without washing it out. |
| 13 | Ito Lanetzach / Kerach 9 | British rhythm crunch, low-gain OD, plate or mono delay. | Simple Compressor into clean Fender-style combo, then spring reverb. | Body pass applied. If this still feels too polite, add low-gain drive or EQ before switching amp families. | Verify whether this preset name maps exactly to Ito Lanetzach in the show notes. |
| 14 | Nitzotzot | Moderate drive with solo lift, delay/reverb; possibly subtle modulation. | Two drives before a tweed/Fender-style amp. One block looked like Tube OD. | Best lead-ready setup observed. Use one drive for rhythm edge and the second for mids/volume lift in the solo. | Ronen has a solo. Keep the solo boost about cut and sustain, not just more saturation. |
| 15 | Ha'Perach | Initially thought clean sustained ballad tone with compression/low OD, delay/hall. | Red drive/boost into blackface Fender-style combo. | Revised target: wah-friendly funky rhythm. Keep amp clean or edge-of-breakup, tight bass, controlled treble, optional compression. | Ronen uses wah pedal for funky rhythm guitar. Too much gain before wah can get harsh. |

## Priority Tuning List

1. Backup: verify the recent Fender Tone/GTX backup or create a fresh one
   before saving any preset changes.
2. Bigger across the board: review all 15 presets for body/ambience/low-mid
   support after the initial volume alignment.
3. Boots: add a footswitchable solo boost while keeping the base clean/twangy.
4. Mishu / Mishehu Mipaam: make the second-part boost much bigger and more
   dramatic in the band mix, not necessarily dirtier.
5. All The Small Things: add controlled room/reverb/ambience so it is less dry.
6. Ha'Makolet and Kerach 9: verify the newly added Simple Compressor blocks at
   rehearsal volume and decide whether either needs EQ or clean boost next.
7. Kach Oti: define base dirty rhythm, solo 1 bigger sound, solo 2 wah-ready
   screaming lead.
8. Parparim: preserve chorus grit and add/assign phaser for the ending solo.
9. Ha'Perach: make the preset wah-friendly for funky rhythm.
10. Ahava hadasha and Boots: likely biggest style mismatches based on visual
   review.

## Open Checks For Fender Tone

- Open each block to verify exact effect names and settings.
- Confirm whether GTX footswitch assignments map to the intended changes:
  rhythm/solo, boost, phaser, delay, and wah use.
- Confirm whether external wah is in front of the amp or in another part of the
  signal path. This affects how much gain/treble each wah song should use.
- Level-match every preset at rehearsal volume, not bedroom volume.
- Check that solo boosts are audible in the band mix without being painfully
  brighter than the rhythm tone.
