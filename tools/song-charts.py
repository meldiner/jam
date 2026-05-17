"""
Hand-curated chart data per song, derived from the original pptx slides.
Each entry maps a slug -> dict with optional fields:
  chartChords:   list of chord names for the chord row
  chartSections: list of {name, reps?, lines: [[bar, bar, ...], ...]}
  formSteps:     list of step names for the left-sidebar form list
                 (overrides the "form" string)

Each "bar" string is one bar; multiple chords in a bar are space-separated ("Am Em").
"""

CHARTS = {

    # -------- English songs from the pptx --------

    "dont-speak": {
        "chartChords": ["Bm", "F#m", "Em", "A"],
        "chartSections": [
            {"name": "Intro", "reps": "guitar, ×4 bars on Bm",
             "lines": [["Bm"]]},
            {"name": "Verse", "reps": "×2",
             "lines": [["Bm", "F#m", "Em", "A"], ["Bm"]]},
            {"name": "Chorus",
             "lines": [["Bm", "F#m", "Em", "A"], ["F#m", "Bm", "Em"]]},
            {"name": "Bridge / Solo",
             "lines": [["Bm", "F#m", "Em", "A"]]},
        ],
        "formSteps": [
            "Intro (gtr)", "Long Verse", "Chorus", "Short Verse", "Chorus",
            "Bridge + Solo", "Bridge (gtr+vox)", "Chorus", "Solo (outro)"
        ],
    },

    "rehab": {
        "chartChords": ["C", "G", "F", "Em", "Am", "Ab"],
        "chartSections": [
            {"name": "Chorus", "reps": "8 bars",
             "lines": [["C", "C", "G", "F"], ["C", "F", "C", "C"]]},
            {"name": "Verse", "reps": "×3",
             "lines": [["Em", "Am", "F", "Ab"], ["Em", "Am", "F", "Ab"], ["G", "F"]]},
        ],
        "formSteps": [
            "Chorus", "Verse 1", "Chorus", "Verse 2", "Chorus", "Verse 3", "Chorus"
        ],
    },

    "everybody-hurts": {
        "chartChords": ["D", "G", "Em", "A", "F#", "Bm", "C", "C/B", "Am", "D/A"],
        "chartSections": [
            {"name": "Verse",
             "lines": [["D", "G", "D", "G"], ["D", "G", "D", "G"]]},
            {"name": "Chorus",
             "lines": [["Em", "A", "Em", "A"], ["Em", "A"]]},
            {"name": "Bridge",
             "lines": [["F#", "Bm", "F#", "Bm"], ["F#", "Bm"], ["C", "G", "C", "C/B Am"]]},
            {"name": "Outro",
             "lines": [["D", "G", "D/A", "G"], ["D"]]},
        ],
        "formSteps": [
            "Verse 1", "Chorus", "Verse 2", "Chorus", "Bridge",
            "Verse 3", "Chorus", "Verse 4 / Outro (fade)"
        ],
    },

    "something": {
        "chartChords": ["F", "Eb", "G/D", "C", "Cmaj7", "C7", "Am", "Am7", "D7", "G", "D9",
                        "A", "C#m", "F#m7", "A/E"],
        "chartSections": [
            {"name": "Intro / Lick", "reps": "Lick 1",
             "lines": [["F", "Eb G/D"]]},
            {"name": "Verse",
             "lines": [["C", "Cmaj7"], ["C7", "F"], ["D7", "G G/A G7/B"], ["Am", "Am(maj7)"], ["Am7", "D9"]]},
            {"name": "Middle 8",
             "lines": [["A", "C#m/G#"], ["F#m7", "A/E"], ["D", "G", "A"]]},
            {"name": "Solo",
             "lines": [["C", "Cmaj7", "C7", "F"], ["D7", "G G/A G7/B"], ["Am Am(maj7)", "Am7 D9"]]},
            {"name": "Outro",
             "lines": [["F Eb G/D", "A"], ["F Eb G/D", "C"]]},
        ],
        "formSteps": [
            "Intro (Lick 1)", "Verse 1", "Verse 2", "Middle 8", "Solo",
            "Verse 4", "Outro (Lick 2 / Lick 1)"
        ],
    },

    "oh-darling": {
        "chartChords": ["G", "D", "Em", "C", "Am7", "D7", "G7", "D7#5", "D#7", "A7"],
        "chartSections": [
            {"name": "Verse",
             "lines": [["D7#5", "G", "D"], ["Em", "C"], ["Am7", "D7"], ["Am7 D7", "G C", "G", "D"]]},
            {"name": "Chorus",
             "lines": [["C", "D#7"], ["G"], ["A7"], ["D7", "D#7", "D7", "D7#5"]]},
            {"name": "Outro",
             "lines": [["Am7 D7", "G", "C", "G", "Ab7 G7"]]},
        ],
        "formSteps": [
            "Verse 1", "Verse 2", "Chorus", "Verse 3", "Chorus", "Verse 4 / Outro"
        ],
    },

    "under-the-bridge": {
        "chartChords": ["D", "F#", "E", "B", "C#m", "G#m", "A", "Emaj7", "F#m", "B/F#",
                        "Am7", "G6", "Fmaj7", "Am", "E7", "Gmaj7"],
        "chartSections": [
            {"name": "Intro", "reps": "×4",
             "lines": [["D", "F#"]]},
            {"name": "Verse",
             "lines": [["E", "B"], ["C#m G#m", "A"], ["E", "B"], ["C#m A", "Emaj7"]]},
            {"name": "Chorus",
             "lines": [["F#m", "E"], ["B/F#", "F#m"], ["E"], ["B/F#", "F#m"]]},
            {"name": "Interlude / Coda", "reps": "“under the bridge…”",
             "lines": [["A Am7", "G6 Fmaj7"], ["A Am7", "G6 Fmaj7"]]},
        ],
        "formSteps": [
            "Intro", "Verse 1", "Verse 2", "Chorus",
            "Interlude", "Verse 3", "Chorus", "Interlude (one time)", "Coda"
        ],
    },

    "whats-up": {
        "chartChords": ["G", "Am", "C", "Gsus2", "Gsus"],
        "chartSections": [
            {"name": "Intro / Verse / Pre-Chorus",
             "lines": [["G", "Am", "C", "Gsus2"]]},
            {"name": "Chorus",
             "lines": [["G", "Am"], ["C", "Gsus"]]},
        ],
        "formSteps": [
            "Intro (×2)", "Verse 1", "Pre-Chorus", "Chorus",
            "Interlude", "Verse 2", "Interlude",
            "Verse 3", "Pre-Chorus", "Chorus (×2)"
        ],
    },

    "feeling-good": {
        "chartChords": ["Gm", "Gm7/F", "D#7", "D7", "C", "D"],
        "chartSections": [
            {"name": "Verse",
             "lines": [["Gm", "Gm7/F", "D#7", "D7"]]},
            {"name": "Chorus",
             "lines": [["Gm", "Gm7/F"], ["D#7", "D7 C D"], ["Gm", "Gm7/F", "D#7", "D7"]]},
        ],
        "formSteps": [
            "Verse 1", "Chorus", "Verse 2", "Chorus",
            "Verse 3 (dragonfly)", "Chorus", "Verse (stars)", "Chorus"
        ],
    },

    "true-colors": {
        "chartChords": ["Am", "G", "G/B", "C", "F", "E", "Gsus4"],
        "chartSections": [
            {"name": "Verse",
             "lines": [["Am G/B", "C F"], ["Am", "G", "C", "F"], ["Am G", "F C"]]},
            {"name": "Pre-Chorus", "reps": "Am G C F",
             "lines": [["Am", "G", "C", "F"]]},
            {"name": "Chorus",
             "lines": [["F C", "G"], ["F C", "F G"], ["F C", "E Am"], ["F C", "Gsus4 G"], ["Am G", "C F"]]},
        ],
        "formSteps": [
            "Verse 1", "Pre-Chorus", "Chorus", "Verse 2", "Pre-Chorus", "Chorus", "Outro (Am G C F)"
        ],
    },

    "son-of-a-preacher-man": {
        "chartChords": ["E", "A", "B7", "B", "D", "E7", "D7"],
        "chartSections": [
            {"name": "Verse",
             "lines": [["E", "A E"], ["E", "B7"], ["A", "E"]]},
            {"name": "Chorus", "reps": "key of E",
             "lines": [["E", "A E"], ["E", "A E"], ["E", "B", "A"]]},
            {"name": "Bridge", "reps": "↑ key of A",
             "lines": [["D", "A"], ["B7"], ["E7"]]},
            {"name": "Chorus 2", "reps": "key of A",
             "lines": [["A", "D A"], ["A", "D A"], ["A", "E", "D7"]]},
        ],
        "formSteps": [
            "Verse 1", "Chorus", "Instrumental", "Verse 2", "Chorus",
            "Bridge", "Chorus 2 (in A)", "Coda (A E D A)"
        ],
    },

    "dreams": {
        "chartChords": ["E", "A", "B", "G"],
        "chartSections": [
            {"name": "Verse",
             "lines": [["E"], ["A"], ["B"], ["E"]]},
            {"name": "Bridge",
             "lines": [["G"], ["G"]]},
        ],
        "formSteps": [
            "Verse 1", "Bridge", "Verse 2", "Bridge", "Verse 3 (outro)"
        ],
    },

    "powerful": {
        "chartChords": ["Bm", "D", "A", "Em", "E", "E5"],
        "chartSections": [
            {"name": "Verse",
             "lines": [["Bm"], ["D", "A"], ["Bm"], ["D", "A"]]},
            {"name": "Pre-Chorus",
             "lines": [["Em", "Bm"], ["D", "A"], ["E Em", "Bm"], ["D", "A"]]},
            {"name": "Chorus", "reps": "×2",
             "lines": [["Em", "Bm"], ["D", "A"], ["Em", "Bm"], ["D", "A"]]},
            {"name": "Bridge", "reps": "tab riff",
             "lines": [["—"]]},
        ],
        "formSteps": [
            "Verse 1", "Pre-Chorus", "Chorus ×2", "Bridge",
            "Verse 2", "Chorus", "Bridge", "Pre-Chorus", "Chorus ×2", "Bridge (×2)"
        ],
    },

    "purple-rain": {
        "chartChords": ["Bbsus2", "Gm7", "F", "Eb", "Bb", "Gm", "Bbadd9/D", "Gm7add11"],
        "chartSections": [
            {"name": "Intro",
             "lines": [["Bbadd9/D", "Gm7add11", "F", "Eb"]]},
            {"name": "Verse",
             "lines": [["Bbsus2", "Gm7"], ["F", "Eb"], ["Bbsus2", "Gm7"], ["F", "Bbsus2"]]},
            {"name": "Chorus",
             "lines": [["Eb"], ["Eb", "Bbsus2"], ["Gm7", "F"], ["F", "Bbsus2"]]},
        ],
        "formSteps": [
            "Intro", "Verse 1", "Chorus", "Verse 2", "Chorus", "Verse 3", "Chorus (outro)"
        ],
    },

    "ziggy-stardust": {
        "chartChords": ["G", "D", "Cadd9", "G/B", "G/A", "Bm", "C", "B", "Em", "A",
                        "Am", "F", "Dsus2", "E"],
        "chartSections": [
            {"name": "Intro / Interlude", "reps": "×4 (×2 between verses)",
             "lines": [["G D", "Cadd9 G/B G/A"]]},
            {"name": "Verse",
             "lines": [["G"], ["Bm", "C"], ["B C D"], ["G"], ["Em"], ["A"], ["C"]]},
            {"name": "Chorus",
             "lines": [["Am G", "F G Am"], ["G", "F G Am"], ["G", "F"], ["D Dsus2"], ["D E"]]},
        ],
        "formSteps": [
            "Intro", "Verse 1", "Verse 2", "Chorus",
            "Interlude", "Verse 3", "Chorus 2", "Interlude", "Outro"
        ],
    },

    "take-me-out": {
        "chartChords": ["E", "Am", "D", "G", "Bm", "Em", "A", "F", "C"],
        "chartSections": [
            {"name": "Verse (slow)",
             "lines": [["E Am", "D"], ["G Bm", "Em"], ["Am", "D"], ["G Bm", "Em"]]},
            {"name": "Transition",
             "lines": [["G A", "Em"], ["G D", "F C Em"]]},
            {"name": "Chorus", "reps": "Em / Am Bm",
             "lines": [["Em"], ["Em"], ["Am", "Bm"]]},
            {"name": "Bridge",
             "lines": [["Am", "C", "D"], ["Am", "C", "D"], ["Am", "C", "D"], ["Am", "C", "D"]]},
        ],
        "formSteps": [
            "Verse (slow)", "Transition", "Chorus", "Bridge", "Chorus",
            "Instrumental", "Bridge", "Outro"
        ],
    },

    "give-it-away": {
        "chartChords": ["Am7", "Am", "C", "Em", "G", "D", "C#"],
        "chartSections": [
            {"name": "Intro / Verse",
             "lines": [["Am", "C"], ["Am", "C"], ["Am", "C"], ["Am", "C"]]},
            {"name": "Chorus",
             "lines": [["Am"], ["Am"], ["Am"], ["Am"]]},
            {"name": "Solo",
             "lines": [["Em", "G", "Em", "G", "Em", "G"]]},
            {"name": "Outro",
             "lines": [["Am C", "Am C"], ["Am D C# C", "Am D C# C"]]},
        ],
        "formSteps": [
            "Intro (Am7)", "Verse 1", "Chorus", "Verse 2", "Chorus",
            "Solo", "Verse 3", "Chorus", "Solo", "Verse 4", "Chorus", "Outro"
        ],
    },

    "ballad-of-a-thin-man": {
        "chartChords": ["Am", "Abaug", "C/G", "D9", "F", "Dm", "C", "Em", "G"],
        "chartSections": [
            {"name": "Intro / Interlude", "reps": "| Am | %",
             "lines": [["Am"]]},
            {"name": "Verse",
             "lines": [["Am"], ["Abaug"], ["C/G", "D9"], ["F", "Dm"], ["C Em", "Am"]]},
            {"name": "Chorus",
             "lines": [["C", "Em"], ["Am", "C/G"], ["F", "Am"]]},
            {"name": "Middle 8",
             "lines": [["Am", "C", "F"], ["Am"], ["Am", "C"], ["F", "Dm G G7"]]},
        ],
        "formSteps": [
            "Intro", "Verse 1", "Chorus", "Interlude",
            "Verse 2", "Chorus", "Verse 3", "Chorus",
            "Middle 8", "Verse 4", "Chorus",
            "Verse 5", "Chorus", "Verse 6", "Chorus", "Verse 7", "Chorus", "Outro (fade)"
        ],
    },

    "after-midnight": {
        "chartChords": ["D", "F", "G", "A", "G/D"],
        "chartSections": [
            {"name": "Intro", "reps": "×4",
             "lines": [["D", "G/D", "D"]]},
            {"name": "Verse",
             "lines": [["D", "F", "G", "D G/D D G/D D"]]},
            {"name": "Chorus",
             "lines": [["D"], ["F"], ["G", "A"], ["D", "F", "G", "D G/D D G/D D"]]},
            {"name": "Solo", "reps": "×2",
             "lines": [["D F", "G D G/D D G/D D"]]},
        ],
        "formSteps": [
            "Intro", "Verse 1", "Chorus", "Verse 2", "Chorus", "Solo", "Outro / Chorus (fade)"
        ],
    },

    "seven-nation-army": {
        "chartChords": ["Em", "G", "C", "B", "A"],
        "chartSections": [
            {"name": "Verse / Chorus",
             "lines": [["Em", "G C B"], ["Em", "G C B"], ["Em", "G C B"], ["Em", "G C B"]]},
            {"name": "Lift",
             "lines": [["G", "A"]]},
            {"name": "Instrumental Chorus",
             "lines": [["Em", "G", "C", "B"], ["Em", "G", "C", "B"]]},
        ],
        "formSteps": [
            "Verse 1", "Inst. Chorus (×4)", "Interlude (×4)",
            "Verse 2", "Solo (×8)", "Interlude (×4)",
            "Verse 3", "Inst. Chorus", "Outro on Em"
        ],
    },

    "i-put-a-spell-on-you": {
        "chartChords": ["Dm", "Gm", "D", "A", "Bb"],
        "chartSections": [
            {"name": "Intro", "reps": "Dm",
             "lines": [["Dm"]]},
            {"name": "Verse",
             "lines": [["Dm", "Gm"], ["Dm", "D"], ["Gm"], ["A"]]},
            {"name": "Bridge", "reps": "< Bass",
             "lines": [["Dm"], ["D"], ["Gm"], ["Bb"]]},
            {"name": "Solo",
             "lines": [["Dm Gm", "Dm D"], ["Gm", "A"]]},
        ],
        "formSteps": [
            "Intro", "Verse 1", "Bridge", "Verse 2",
            "Solo", "Verse 3 (long)", "Bridge", "Verse 4", "Outro"
        ],
    },

    # -------- Hebrew songs --------

    "blues-cnaani": {
        "chartChords": ["Am", "Em", "Fmaj7", "G", "D9", "D5+", "D/F", "D/E", "D/C"],
        "chartSections": [
            {"name": "פתיחה (Intro)", "reps": "ריף גיטרה",
             "lines": [["D5+", "D9"], ["D/F D/E", "D9 D/C"], ["D9"]]},
            {"name": "בית (Verse)",
             "lines": [["Am", "Em"], ["Fmaj7", "G"], ["Am", "Em"], ["Fmaj7", "G"], ["Am", "Em"]]},
            {"name": "פזמון (Chorus)",
             "lines": [["Am", "Em"], ["Fmaj7", "G"]]},
            {"name": "סיום (Outro)", "reps": "D9 ×8",
             "lines": [["D9"]]},
        ],
        "formSteps": [
            "פתיחה", "בית", "פזמון", "פתיחה",
            "בית", "פזמון", "מעבר (כמו פתיחה)",
            "בית", "פזמון", "מעבר",
            "בית", "פזמון", "מעבר",
            "חצי בית → סיום"
        ],
    },

    "ah-ah-ah": {
        "chartChords": ["C", "F", "Em", "Am", "Dm", "G", "G/F", "G/E", "Eb", "Bb"],
        "chartSections": [
            {"name": "פתיחה (Intro)", "reps": "לפני הבית",
             "lines": [["C", "C"]]},
            {"name": "בית — תבנית (Verse pattern)",
             "lines": [
                 ["C", "F"],
                 ["Em", "Am", "F", "Dm"],
                 ["G G/F", "G/E", "C"],
             ]},
            {"name": "סיומות בית (Verse voltas)",
             "lines": [
                 ["1.", "C", "(→ ראש)"],
                 ["2,3.", "G G/F", "G/E", "F", "C"],
                 [" ", "G G/F", "G/E", "G", "G"],
                 ["4.", "G", "F", "C", "C"],
             ]},
            {"name": "פזמון — תבנית (Chorus pattern)",
             "lines": [["C", "Eb", "F", "Bb"]]},
            {"name": "סיומות פזמון (Chorus voltas)",
             "lines": [["1, 2.", "F", "F"]]},
        ],
        "formSteps": [
            "פתיחה",
            "בית (1)",
            "בית (2)",
            "פזמון",
            "בית (3) — תיבה ראשונה רק פסנתר",
            "פזמון",
            "מעבר — רק פסנתר (2 תיבות)",
            "בית (4) — חצי ראשון פסנתר + שירה + מחיאות כפיים",
            "פזמון × 4 (סיום בפעם הרביעית)",
            "סיום — רק פסנתר על C",
        ],
    },

    "kerach-9": {
        # קרח 9 — איתו לנצח. From slide 8 / images 12 + 13 + 17.
        # Key: Bb. BPM: 160.
        "chartChords": ["Bb", "F", "Eb", "Eb/E", "Gm", "D", "Ab", "Bb7", "A", "E"],
        "chartSections": [
            {"name": "פתיחה (Intro)", "reps": "×2",
             "lines": [["Bb F", "Bb F"]]},
            {"name": "בית (Verse)",
             "lines": [
                 ["F", "Bb", "F", "Bb"],
                 ["Bb F", "Bb", "Eb/E", "Eb"],
                 ["F", "Bb", "F", "Bb"],
                 ["Eb F", "Bb", "Eb/E", "Eb"],
             ]},
            {"name": "פזמון (Chorus)",
             "lines": [
                 ["Gm", "D", "Eb"],
                 ["Eb", "Ab"],
                 ["Eb Bb7 Bb", "Eb/E"],
                 ["Gm", "D", "Eb"],
                 ["Eb", "Ab"],
                 ["Bb", "F"],
             ]},
            {"name": "מעבר (Bridge)",
             "lines": [["Bb F", "Bb F", "Bb"]]},
            {"name": "סיום (Outro)", "reps": "modulation up",
             "lines": [["Bb F"], ["A E", "A E"]]},
        ],
        "formSteps": [
            "פתיחה (×2)",
            "בית 1",
            "פזמון",
            "פתיחה",
            "בית 2",
            "פזמון",
            "מעבר",
            "בית 3",
            "פזמון",
            "מעבר",
            "Outro (modulation A E)",
            "פזמון* (last chorus)",
        ],
    },

    "ahava-hadasha": {
        # Assaf Amdursky. From slide 12 / images 23 + 24 + 27. Key: Em.
        "chartChords": ["Em", "G", "F#", "Bm", "C", "F#m"],
        "chartSections": [
            {"name": "פתיחה — Bass",
             "lines": [["D & E", "E & G"], ["A & B", "A & C"]]},
            {"name": "פתיחה — Guitar",
             "lines": [["F# & G", "A & B"], ["C & B & F# & E"]]},
            {"name": "בית (Verse)",
             "lines": [
                 ["Em"],
                 ["G"],
                 ["F#", "Bm"],
             ]},
            {"name": "פזמון (Chorus)", "reps": "×2",
             "lines": [
                 ["Em"],
                 ["F#", "Bm", "G"],
                 ["Em"],
                 ["G"],
                 ["C", "Bm"],
                 ["C", "Em"],
             ]},
            {"name": "סיום (Outro)",
             "lines": [
                 ["Em"],
                 ["G"],
                 ["Bm"],
                 ["C"],
                 ["Em G F# Em", "(×4)"],
             ]},
        ],
        "formSteps": [
            "פתיחה (bass + guitar)",
            "בית 1",
            "פזמון (×2)",
            "בית 2",
            "פזמון (×2)",
            "מעבר",
            "פזמון",
            "סיום (Em G F# Em ×4)",
        ],
    },

    "pahei-show": {
        "chartSections": [],
        "formSteps": [
            "פתיחה", "בית", "בית", "פזמון", "מעבר",
            "בית", "פזמון", "סולו (על חצי בית)",
            "פזמון × 2", "סיום"
        ],
    },

    "hakaas": {
        "chartChords": ["E", "G#m", "A", "B"],
        "chartSections": [
            {"name": "סולו (chord run)",
             "lines": [["E", "G#m", "A", "B"]]},
        ],
        "formSteps": [
            "פתיחה (גיטרה ← בס ← תופים)", "בית", "פזמון",
            "מעבר קצר", "בית", "פזמון",
            "סולו (E ← G#m ← A ← B)", "פזמון", "פזמון", "סולו (סיום)"
        ],
    },

    "crazy": {
        "chartChords": ["Dm", "F", "Bb", "A"],
        "chartSections": [
            {"name": "Verse / Chorus",
             "lines": [["Dm", "F", "Bb", "A"]]},
        ],
        "formSteps": [
            "(loop on Dm – F – Bb – A throughout)"
        ],
    },

    "echake-bashadot": {
        "chartSections": [],
        "formSteps": [
            "בית — Break", "בית", "פזמון — Break",
            "סולו — Break", "בית", "פזמון — Break",
            "בית — Break", "סיום"
        ],
    },

    "nitzotzot": {
        # Fortisakharof. From slide 36 / images 63 + 64. Key: Am.
        "chartChords": ["Am", "C", "Fmaj7", "D9", "G", "F", "Bm", "A", "D", "B", "Em"],
        "chartSections": [
            {"name": "פתיחה (Intro)", "reps": "fingerpicked walk",
             "lines": [["(arpeggio: e-3-2-0 / B-3-1-0 / G-2-0 / D-4-2-0 / A-0-2-3)"]]},
            {"name": "פתיחה ווקאלית (Intro vocals)", "reps": "×4",
             "lines": [["D", "G", "C"], ["D", "G", "C"]]},
            {"name": "בית (Verse)",
             "lines": [
                 ["Fmaj7", "C", "Am"],
                 ["Am", "D9", "Fmaj7"],
                 ["Fmaj7", "C", "Am"],
                 ["C", "D9", "Fmaj7"],
             ]},
            {"name": "פזמון (Chorus)",
             "lines": [
                 ["Am", "G", "C"],
                 ["C", "Fmaj7"],
                 ["Am", "G"],
                 ["G", "F"],
                 ["Bm"],
                 ["A", "D"],
                 ["B", "Em"],
                 ["G", "C"],
                 ["D"],
             ]},
            {"name": "סיום (Outro)", "reps": "×4",
             "lines": [["Am", "Fmaj7", "Fmaj7", "Am"]]},
        ],
        "formSteps": [
            "פתיחה (אריבג׳יו)",
            "פתיחה ווקאלית — D G C ×4",
            "בית 1",
            "פזמון",
            "בית 2",
            "פזמון",
            "סיום — Am Fmaj7 Fmaj7 Am ×4",
        ],
    },

    "haperach-begani": {
        "chartChords": ["Cm", "Cm/Bb", "Ab", "G", "G7", "Gsus4", "Fm", "Eb",
                        "Cm/G", "Cm/Ab", "Dm7b5", "Bb", "C#"],
        "chartSections": [
            {"name": "אינטרו (Intro)",
             "lines": [["Cm", "G"]]},
            {"name": "בית (Verse)", "reps": "×2",
             "lines": [
                 ["Cm", "Cm/Bb", "Ab", "G7"],
                 ["Cm", "Ab", "Fm", "G7"],
                 ["Eb", "Fm", "Ab", "G7"],
                 ["Cm", "Fm", "Ab", "G7"],
             ]},
            {"name": "מעבר (Bridge)",
             "lines": [
                 ["Cm", "Ab", "G", "G"],
                 ["Fm", "Ab", "G", "G"],
             ]},
            {"name": "פזמון (Chorus)",
             "lines": [
                 ["Cm", "Cm/Bb", "Ab", "Cm/G"],
                 ["Cm", "Cm/Bb", "Ab", "G"],
                 ["Eb", "Eb", "Fm", "G"],
                 ["Ab", "Fm", "Dm7b5", "G"],
             ]},
            {"name": "בית (Verse)", "colBreak": True,
             "lines": [
                 ["Cm", "Cm/Bb", "Ab", "G7"],
                 ["Cm", "Ab", "Fm", "G7"],
                 ["Eb", "Fm", "Ab", "G7"],
                 ["Cm", "Fm", "Ab", "G7"],
             ]},
            {"name": "מעבר (Bridge)",
             "lines": [
                 ["Cm", "Ab", "G", "G"],
                 ["Fm", "Ab", "G", "G"],
             ]},
            {"name": "פזמון (Chorus)", "reps": "×2",
             "lines": [
                 ["Cm", "Cm/Bb", "Ab", "Cm/G"],
                 ["Cm", "Cm/Bb", "Ab", "G"],
                 ["Eb", "Eb", "Fm", "G"],
                 ["Ab", "Fm", "Dm7b5", "G"],
             ]},
            {"name": "סיום (Ending)",
             "lines": [
                 ["Ab", "Fm", "Dm7b5", "G"],
                 ["Bb", "Cm"],
             ]},
        ],
        "formSteps": [
            "אינטרו",
            "בית",
            "מעבר",
            "פזמון",
            "בית",
            "מעבר",
            "פזמון",
            "סיום",
        ],
    },

    "valerie": {
        "chartChords": ["Db", "Ebm", "Ebm7", "Gb", "Fm", "Ab", "Dbmaj7"],
        "chartSections": [
            {"name": "Intro / Groove", "reps": "2 bars",
             "lines": [["Db"]]},
            {"name": "Verse", "reps": "8 bars (bars 3+4 minor)",
             "lines": [["Db", "Db", "Ebm", "Ebm"], ["Db", "Db", "Ebm7", "Ebm7"]]},
            {"name": "Pre-Chorus", "reps": "8 bars",
             "lines": [["Gb", "Fm", "Gb", "Fm"], ["Gb", "Fm", "Ab", "Ab"]]},
            {"name": "Chorus", "reps": "4 bars",
             "lines": [["Dbmaj7", "Dbmaj7", "Ebm7", "Ebm7"]]},
        ],
        "formSteps": [
            "Intro (groove)",
            "Verse 1",
            "Pre-Chorus",
            "Chorus",
            "Verse 2",
            "Pre-Chorus",
            "Chorus",
            "Bridge / Solo",
            "Chorus",
            "Outro (fade on Db)",
        ],
    },

    "tzar-li-charlie": {
        "chartChords": ["Dm", "Gm", "A7"],
        "chartSections": [
            {"name": "פתיחה (build-up)", "reps": "all on Dm",
             "lines": [
                 ["Dm", "Dm", "Dm", "Dm"],
             ]},
            {"name": "12-bar blues (Dm)",
             "lines": [
                 ["Dm", "Dm", "Dm", "Dm"],
                 ["Gm", "Gm", "Dm", "Dm"],
                 ["A7", "Gm", "Dm", "A7"],
             ]},
        ],
        "formSteps": [
            "בס + תופים + גיטרה — 4 בארים (Dm)",
            "+ פסנתר וחצוצרה — 4 בארים",
            "Break",
            "נכנסת השירה — ראש (head)",
            "סולו × N",
            "ראש (חזרה)",
            "סיום על Dm",
        ],
    },

    # ---------------------------------------------------------------------
    # Charts populated from the chord-chart images embedded in the original
    # Guest House.pptx (slides 12, 21, 32, 35, 36).
    # ---------------------------------------------------------------------

    "shir-hamakolet": {
        # Kaveret. From slides 32 / images 55 + 56. Key: Em.
        "chartChords": ["Em", "D", "Am", "Cadd9", "F", "Bb", "Cmaj7", "B", "Esus4"],
        "chartSections": [
            {"name": "אינטרו (Intro)", "reps": "Am bass riff",
             "lines": [["Am"]]},
            {"name": "בית (Verse)", "reps": "8 bars",
             "lines": [
                 ["Em D", "Am"],
                 ["Em D"],
                 ["Em D", "Cadd9"],
                 ["Em D", "Cadd9"],
             ]},
            {"name": "פזמון (Chorus)",
             "lines": [
                 ["Em"],
                 ["D", "F"],
                 ["Em", "B", "Bb"],
                 ["F D", "Em"],
                 ["Cmaj7", "B", "Bb"],
             ]},
            {"name": "תזוזה לפזמון (Pre-chorus tag)",
             "lines": [["Em Esus4", "Em Esus4"]]},
        ],
        "formSteps": [
            "אינטרו",
            "בית 1",
            "תזוזה",
            "פזמון",
            "בית 2",
            "פזמון",
            "מעבר",
            "פזמון",
            "סיום",
        ],
    },

    "mishehu": {
        # מישהו פעם — Ivri Lider. From slides 35 / images 53 + 54 + 61.
        # Each verse modulates UP a whole step: Bb → C → D → E.
        "chartChords": ["Bb", "Bbmaj7", "F", "Fmaj7", "C", "C6", "Csus4", "Gm",
                        "Cmaj7", "G", "D", "D6", "Am",
                        "Dmaj7", "A", "E", "Esus4", "Bm",
                        "Emaj7", "B", "F#", "F#sus4", "C#m",
                        "B/Bb", "A/Ab"],
        "chartSections": [
            {"name": "פתיחה / מעבר (Intro / Bridge)", "reps": "×2",
             "lines": [["B B/Bb", "A A/Ab"]]},
            {"name": "בית 1 — Bb",
             "lines": [
                 ["Bbmaj7", "F"],
                 ["C C6", "Gm"],
                 ["Bbmaj7", "F"],
                 ["C C6", "Gm"],
             ]},
            {"name": "בית 2 — C (mod up)",
             "lines": [
                 ["Cmaj7", "G"],
                 ["D D6", "Am"],
                 ["Cmaj7", "G"],
                 ["D D6", "Am"],
             ]},
            {"name": "בית 3 — D (mod up)",
             "lines": [
                 ["Dmaj7", "A"],
                 ["E Esus4", "Bm"],
                 ["Dmaj7", "A"],
                 ["E Esus4", "Bm"],
             ]},
            {"name": "בית 4 — E (mod up)",
             "lines": [
                 ["Emaj7", "B"],
                 ["F# F#sus4", "C#m"],
                 ["Emaj7", "B"],
                 ["F# F#sus4", "C#m"],
             ]},
            {"name": "סיום — חזרה ל-Bb (Outro)",
             "lines": [
                 ["Bbmaj7", "F"],
                 ["C Csus4", "Gm"],
                 ["Bbmaj7", "F"],
                 ["Fmaj7 C", "Csus4 Gm"],
                 ["B Bbmaj7", "C Bbmaj7", "(×2)"],
             ]},
        ],
        "formSteps": [
            "פתיחה (B B/Bb A A/Ab ×2)",
            "בית 1 (Bb)",
            "מעבר",
            "בית 2 (C)",
            "מעבר",
            "בית 3 (D)",
            "מעבר",
            "בית 4 (E)",
            "מעבר",
            "סיום (חזרה ל-Bb → קדנציה על Bbmaj7)",
        ],
    },

    "parperei-titua": {
        # Carmella Gross-Wagner / Eran Tzur. From slide 21 / images 50 + 42 + 36.
        # Key: C major.
        "chartChords": ["C", "Cmaj7", "F", "A", "Fm", "Dm", "Am", "E",
                        "C/B", "Em", "B"],
        "chartSections": [
            {"name": "פתיחה (Intro)", "reps": "Cmaj7-loop, 4 bars",
             "lines": [["C Cmaj7", "C Cmaj7"], ["C Cmaj7", "C Cmaj7"]]},
            {"name": "בית (Verse)",
             "lines": [
                 ["Cmaj7 C", "Cmaj7 C"],
                 ["F", "Cmaj7 C"],
                 ["A", "C", "Fm"],
                 ["Dm"],
                 ["Am", "E"],
             ]},
            {"name": "פזמון (Chorus) — “פרפרי תעתוע”",
             "lines": [
                 ["Am C/B", "C", "Fm F", "Em"],
                 ["Em", "Am"],
                 ["C", "Fm F"],
             ]},
            {"name": "פזמון מורחב (Extended chorus)",
             "lines": [
                 ["Am C/B", "C", "Fm F", "Em"],
                 ["Em", "Am Em B", "C"],
                 ["Fm F", "Em"],
             ]},
            {"name": "מעבר (Bridge)",
             "lines": [
                 ["Em F Fm", "C C/B Am"],
                 ["Em F Fm", "C C/B Am"],
             ]},
            {"name": "סיום (Outro)",
             "lines": [["C Cmaj7", "F", "A", "(×2)"]]},
        ],
        "formSteps": [
            "פתיחה",
            "בית 1",
            "פזמון",
            "בית 2",
            "פזמון",
            "מעבר",
            "פזמון מורחב",
            "סיום (C Cmaj7 F A ×2)",
        ],
    },

    "spontaneous": {
        "chartChords": ["A", "E", "F#m", "D", "D7", "C#7", "A/E", "D/E", "C#m"],
        "chartSections": [
            {"name": "Intro", "reps": "4 bars",
             "lines": [["A", "E", "F#m", "D"]]},
            {"name": "Verse", "reps": "8 bars",
             "lines": [["A", "E", "F#m", "D"],
                       ["A", "E", "F#m", "D7"]]},
            {"name": "Pre-Chorus", "reps": "8 bars",
             "lines": [["A", "F#m", "D", "E"],
                       ["A", "C#7", "D", "A/E E"]]},
            {"name": "Chorus", "reps": "8 bars",
             "lines": [["A", "E", "F#m", "D E"],
                       ["A", "E", "D", "D7"]]},
            {"name": "Bridge", "reps": "16 bars",
             "lines": [["A", "E", "F#m", "D D/E"],
                       ["A", "E", "F#m", "D D/E"],
                       ["A", "E", "F#m", "D D/E"],
                       ["A", "C#m", "D", "E"]]},
        ],
        "formSteps": [
            "Intro (4 bars)",
            "Verse 1",
            "Pre-Chorus 1",
            "Chorus 1",
            "Intro (return)",
            "Verse 2",
            "Pre-Chorus 2",
            "Chorus 2",
            "Bridge",
            "Chorus (final, repeat)",
        ],
    },

    "lama-lo-amart-li": {
        "chartChords": ["Em", "Bm7", "A7", "C", "Ebm", "Bbm7", "Ab7", "B", "Dm", "Am7", "G7", "Bb"],
        "chartSections": [
            {"name": "בית (No modulation)",
             "lines": [["Em", "Bm7", "Em"], ["Em", "Bm7", "Em"], ["A7", "Bm7", "Em"], ["C", "A7"]]},
            {"name": "סולו גיטרה",
             "lines": [["Em", "Bm7"]]},
            {"name": "בית (1st modulation)",
             "lines": [["Ebm", "Bbm7", "Ebm"], ["Ebm", "Bbm7", "Ebm"], ["Ab7", "Bbm7", "Ebm"], ["B", "Ab7"]]},
            {"name": "בית (2nd modulation)",
             "lines": [["Dm", "Am7", "Dm"], ["Dm", "Am7", "Dm"], ["G7", "Am7", "Dm"], ["Bb", "G7"]]},
        ],
        "formSteps": [
            "בית 1 (Em)", "בית 2 (Em)", "סולו גיטרה קצר",
            "בית 3 (Em)", "סולו גיטרה ארוך",
            "סיום — מודולציה ל-Ebm", "בית (Ebm)",
            "מודולציה ל-Dm", "בית (Dm)", "בית (Dm)"
        ],
    },

    # ---------------------------------------------------------------------
    # New show songs not in the pptx — best-shot charts from common
    # knowledge. Sections marked "(verify)" need confirmation at practice.
    # ---------------------------------------------------------------------

    "smooth": {
        # Santana feat. Rob Thomas. Key: Am. The whole song loops on Am – F – E.
        "chartChords": ["Am", "F", "E", "Dm", "G", "C"],
        "chartSections": [
            {"name": "Intro / Verse", "reps": "Am – F – E loop",
             "lines": [["Am", "F", "E", "Am"]]},
            {"name": "Pre-Chorus", "reps": "build on iv → V",
             "lines": [["Dm", "G"], ["F", "E"]]},
            {"name": "Chorus",
             "lines": [["Am", "F"], ["E", "Am"], ["Am", "F"], ["E", "Am"]]},
            {"name": "Solo / Outro", "reps": "Am – F – E loop",
             "lines": [["Am", "F", "E", "Am"]]},
        ],
        "formSteps": [
            "Intro (Am – F – E ×4)",
            "Verse 1",
            "Pre-Chorus",
            "Chorus",
            "Verse 2",
            "Pre-Chorus",
            "Chorus",
            "Guitar Solo",
            "Pre-Chorus",
            "Chorus",
            "Outro (Am – F – E fade)",
        ],
    },

    "one-way-or-another": {
        # Blondie. Key: E (mixolydian feel, single-tonic verse riff).
        # Verse riff sits on E5; pre-chorus alternates B–A; bridge moves
        # through G–B–D before resolving back to E. Verify chorus voicings.
        "chartChords": ["E", "E5", "B", "A", "G", "D", "F#", "B5", "A5"],
        "chartSections": [
            {"name": "Intro / Verse", "reps": "E5 riff",
             "lines": [["E"]]},
            {"name": "Pre-Chorus", "reps": "“gonna get-cha…” — verify",
             "lines": [["B", "A"], ["B", "A"]]},
            {"name": "Chorus", "reps": "“one way or another” — verify",
             "lines": [["E", "E"], ["E", "E"]]},
            {"name": "Bridge", "reps": "“and if the lights are all out…” — verify",
             "lines": [["G", "D"], ["G", "D"], ["F#", "B"]]},
        ],
        "formSteps": [
            "Intro (E riff)",
            "Verse 1",
            "Pre-Chorus",
            "Chorus",
            "Verse 2",
            "Pre-Chorus",
            "Chorus",
            "Bridge",
            "Solo over verse riff",
            "Pre-Chorus",
            "Chorus (×2 to fade)",
            "(skeleton — verify exact voicings at practice)",
        ],
    },

    "all-the-small-things": {
        # Blink-182. Key C major. Confirmed by user against UG.
        # Boxes laid out top-to-bottom in performance order; the form
        # sidebar uses a single "Chorus" entry per chorus block.
        "chartChords": ["C", "F", "G"],
        "chartSections": [
            {"name": "Intro",
             "lines": [["C", "F", "G", "G (F)"]]},
            {"name": "Verse 1", "reps": "×4",
             "lines": [["C", "G", "F", "G"]]},
            {"name": "Chorus (\"say it ain't so\")",
             "lines": [["C", "(C)", "(G)", "(F)"]]},
            {"name": "Chorus (\"na na na\")", "reps": "×2",
             "lines": [["C", "G", "F", "C"]]},
            {"name": "Bridge", "reps": "×2",
             "lines": [["C", "F", "E", "G (F)"]]},
            {"name": "Verse 2", "reps": "×2",
             "lines": [["C", "G", "F", "G"]]},
            {"name": "Chorus (\"say it ain't so\")",
             "lines": [["C", "(C)", "(G)", "(F)"]]},
            {"name": "Chorus (\"na na na\")", "reps": "×2",
             "lines": [["C", "G", "F", "C"]]},
            {"name": "Instrumental", "reps": "×4",
             "lines": [["C", "C", "F", "G"]]},
            {"name": "Chorus (\"say it ain't so\") — outro", "reps": "×4",
             "lines": [["C", "C", "G", "F"]]},
            {"name": "Ending",
             "lines": [["F", "C"]]},
        ],
        "formSteps": [
            "Intro",
            "Verse 1",
            "Chorus",
            "Bridge",
            "Verse 2",
            "Chorus",
            "Instrumental",
            "Chorus",
            "Ending",
        ],
    },

    "these-boots": {
        # Nancy Sinatra. Key E. Verse is built on a famous descending bass
        # walk under a sustained E tonic; chorus moves to A and resolves
        # via B7. Slash-chord notation here represents the bass note
        # walking down (the upper voicing stays close to E).
        "chartChords": ["E", "E/D#", "E/D", "E/C#", "E/C", "E/B", "E/Bb", "A", "B7"],
        "chartSections": [
            {"name": "Intro — descending bass walk",
             "lines": [["E", "E/D#", "E/D", "E/C#"],
                       ["E/C", "E/B", "E/Bb", "A"]]},
            {"name": "Verse — bass walks down on E",
             "lines": [["E", "E/D#", "E/D", "E/C#"],
                       ["E/C", "E/B", "E/Bb", "A"]]},
            {"name": "Chorus",
             "lines": [["A", "E"], ["A", "E"], ["A", "E"], ["B7", "E"]]},
            {"name": "Outro — bass walk fade",
             "lines": [["E", "E/D#", "E/D", "E/C#"],
                       ["E/C", "E/B", "E/Bb", "A"]]},
        ],
        "formSteps": [
            "Intro (bass walk on E)",
            "Verse 1",
            "Chorus",
            "Verse 2",
            "Chorus",
            "Bridge / spoken break",
            "Verse 3",
            "Chorus",
            "Outro (bass walk fade)",
        ],
    },
}
