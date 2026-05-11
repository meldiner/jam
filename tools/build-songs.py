#!/usr/bin/env python3
"""
Build per-song JSON files from the pptx slide XML.

Reads slide XML from /tmp/pptx_extract/ppt/slides/slide<N>.xml and writes
one JSON file per song into ../songs/<slug>.json plus updates ../songs/index.json.

The slide-to-song mapping is in SONGS below. Each entry is:
  {
    "slug": "...",
    "title": "...",
    "artist": "...",
    "slides": [n, n, ...],     # slide numbers whose body holds the song
    "key": "...", "bpm": ..., "timeSig": "...",  # optional metadata
    "opening": "...", "ending": "...",            # optional cues
    "form": "Intro -> Verse -> ...",              # optional override
    "chords": [...],                              # optional chord-name array (else inferred)
    "dir": "rtl" | "ltr",                          # optional song-level text direction
    "skipParse": True,                             # if True, leave lyrics: null (title-only)
  }

The parser converts pptx-style chord-line/lyric-line pairs into the inline
"[Chord]text" lyric format used by the viewer.
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SONGS_DIR = ROOT / "songs"
LOCAL_DIR = ROOT / "songs-local"   # gitignored — lyrics overlay
SLIDES_DIR = Path("/tmp/pptx_extract/ppt/slides")

NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}

# -------------------- Slide text extraction --------------------

def slide_text(n):
    """Return the slide's text as a list of lines, preserving spacing within paragraphs."""
    p = SLIDES_DIR / f"slide{n}.xml"
    if not p.exists():
        return []
    tree = ET.parse(p)
    root = tree.getroot()
    paragraphs = []
    for para in root.iter(f"{{{NS['a']}}}p"):
        # Concatenate all runs within the paragraph, preserving spaces.
        s = ""
        for r in para.iter(f"{{{NS['a']}}}r"):
            t = r.find(f"{{{NS['a']}}}t")
            if t is not None and t.text:
                s += t.text
        paragraphs.append(s)
    return paragraphs


def join_slides(slide_nums):
    out = []
    for n in slide_nums:
        out.extend(slide_text(n))
        out.append("")  # blank line between slides
    return out


# -------------------- Chord-line detection --------------------

# Matches a single chord token like "C", "Am", "F#m7", "Bbsus2", "G/B", "D9", "N.C.", "Abaug"
CHORD_TOKEN_RE = re.compile(
    r"^("
    r"N\.?C\.?"
    r"|"
    r"[A-G](?:#|b)?"
    r"(?:m|min|maj|sus|add|aug|dim|°)?"
    r"(?:\d+)?"
    r"(?:add\d+|sus[24]|maj\d+|#\d+|b\d+|\+|\(\d+\))*"
    r"(?:/[A-G](?:#|b)?\d?)?"
    r")[.,;:]?$"
)
# Variant for tokens that have brackets like [Abaug]
BRACKETED_RE = re.compile(r"^\[([^\]]+)\]$")


def normalize_chord_token(tok):
    tok = tok.strip().rstrip(".,;:*")
    m = BRACKETED_RE.match(tok)
    if m:
        tok = m.group(1)
    # Strip trailing reps marker like "x2", "X2"
    return tok


def is_chord_token(tok):
    if not tok:
        return False
    tok = normalize_chord_token(tok)
    if not tok:
        return False
    # reject pure-digit, pure-punctuation
    if re.fullmatch(r"\d+", tok):
        return False
    return bool(CHORD_TOKEN_RE.match(tok))


def is_chord_line(line):
    s = line.strip()
    if not s:
        return False
    # Reject lines that are mostly text (have lowercase words, punctuation phrases)
    if re.search(r"[a-z]{4,}", s):
        return False
    # Reject Hebrew lines
    if re.search(r"[֐-׿]", s):
        return False
    # Reject tab notation (e|---, B|---, etc)
    if re.search(r"^[eEABDGabdg]\|", s):
        return False
    # Reject bar notation lines like | F | A | (those are pure-bars, treat separately)
    toks = s.split()
    if not toks:
        return False
    # Allow tokens that are bracket-wrapped
    return all(is_chord_token(t) for t in toks)


def find_chord_positions(line):
    positions = []
    for m in re.finditer(r"\S+", line):
        tok = m.group(0)
        if is_chord_token(tok):
            positions.append((m.start(), normalize_chord_token(tok)))
    return positions


# -------------------- Block parsing --------------------

SECTION_RE = re.compile(r"^\s*\[([^\]]+)\]\s*[xX]?\d*\s*$")
TAB_RE = re.compile(r"^[eEABDGabdg]\|")
BAR_NOTATION_RE = re.compile(r"^\s*\|.*\|\s*([xX]\s*\d+)?\s*$")


def merge_chord_into_lyric(chord_line, lyric_line):
    """Insert [chord] markers into a lyric line at the columns where chords appeared above."""
    positions = find_chord_positions(chord_line)
    if not positions:
        return lyric_line
    if not lyric_line.strip():
        return None  # signal: chord-only run
    # Pad lyric line to be at least as wide as the rightmost chord
    pad_len = max(p[0] for p in positions) + 1
    padded = lyric_line.ljust(pad_len)
    out_parts = []
    last = 0
    for pos, chord in positions:
        out_parts.append(padded[last:pos])
        out_parts.append(f"[{chord}]")
        last = pos
    out_parts.append(padded[last:])
    return "".join(out_parts).rstrip()


def is_blank(s):
    return not s.strip()


def parse_lyric_block(lines):
    """Convert a block of lyric/chord lines into [{section, lines: [...]}] structure."""
    sections = []
    cur = None

    def flush():
        nonlocal cur
        if cur and cur["lines"]:
            sections.append(cur)
        cur = None

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if is_blank(line):
            i += 1
            continue
        m = SECTION_RE.match(line)
        if m:
            flush()
            cur = {"section": m.group(1).strip(), "lines": []}
            i += 1
            continue
        # Skip tab lines
        if TAB_RE.match(line):
            i += 1
            continue
        # Bar notation like "| F | A | x4" — keep as a chord-only run
        if BAR_NOTATION_RE.match(line):
            chords = re.findall(r"[A-G][\w/#+°]*", line)
            chords = [normalize_chord_token(c) for c in chords if is_chord_token(c)]
            if chords:
                if cur is None:
                    cur = {"section": "", "lines": []}
                cur["lines"].append({"chords": chords})
            i += 1
            continue
        if is_chord_line(line):
            # Look ahead for a lyric line
            if i + 1 < len(lines):
                nxt = lines[i + 1].rstrip()
                if (not is_blank(nxt)
                        and not is_chord_line(nxt)
                        and not SECTION_RE.match(nxt)
                        and not TAB_RE.match(nxt)
                        and not BAR_NOTATION_RE.match(nxt)):
                    merged = merge_chord_into_lyric(line, nxt)
                    if cur is None:
                        cur = {"section": "", "lines": []}
                    if merged is None:
                        chords = [normalize_chord_token(t) for t in line.split() if is_chord_token(t)]
                        if chords:
                            cur["lines"].append({"chords": chords})
                    else:
                        cur["lines"].append(merged)
                    i += 2
                    continue
            # chord-only line
            chords = [normalize_chord_token(t) for t in line.split() if is_chord_token(t)]
            if chords:
                if cur is None:
                    cur = {"section": "", "lines": []}
                cur["lines"].append({"chords": chords})
            i += 1
            continue
        # plain lyric line
        if cur is None:
            cur = {"section": "", "lines": []}
        cur["lines"].append(line)
        i += 1
    flush()
    return sections


# -------------------- Hebrew block parsing --------------------

def parse_hebrew_block(lines):
    """For Hebrew songs the chord line typically *follows* an empty/sparse layout.
    The pptx structure is: chord line, then the next non-empty line is the Hebrew lyric.
    Same algorithm but the lyric line is RTL — we just store it; the viewer applies dir=rtl."""
    return parse_lyric_block(lines)


# -------------------- Section utility --------------------

def collect_chords_used(sections):
    """Return a sorted list of unique chord names referenced in sections (for chart view)."""
    chords = []
    seen = set()
    def add(c):
        c = normalize_chord_token(c)
        if c and c not in seen and c != "N.C.":
            seen.add(c)
            chords.append(c)
    for sec in sections:
        for line in sec["lines"]:
            if isinstance(line, dict) and "chords" in line:
                for c in line["chords"]:
                    add(c)
            elif isinstance(line, str):
                for m in re.finditer(r"\[([^\]]+)\]", line):
                    add(m.group(1))
    return chords


def build_form_steps(sections):
    """Reduce a section list into a non-redundant form sequence."""
    steps = []
    for sec in sections:
        name = sec["section"].strip()
        if not name:
            continue
        # Strip "1", "2" suffixes for de-dup grouping
        base = re.sub(r"\s*\d+\s*$", "", name)
        steps.append(name if name else base)
    return steps


# -------------------- Song structure for sections (chart view) --------------------

def build_chart_sections(sections):
    """For chart view: sections array with name + bar lines (chord-only)."""
    out = []
    seen_names = set()
    for sec in sections:
        name = sec["section"].strip()
        if not name:
            continue
        # one block per *unique* section name; first occurrence
        if name in seen_names:
            continue
        seen_names.add(name)
        bar_lines = []
        for line in sec["lines"]:
            if isinstance(line, dict) and "chords" in line:
                bar_lines.append(line["chords"])
            elif isinstance(line, str):
                # Extract chord changes from the inline-format line
                chords = re.findall(r"\[([^\]]+)\]", line)
                if chords:
                    bar_lines.append([normalize_chord_token(c) for c in chords])
        # collapse adjacent identical lines
        dedup = []
        for bl in bar_lines:
            if not dedup or dedup[-1] != bl:
                dedup.append(bl)
        if not dedup:
            continue
        out.append({"name": name, "lines": dedup[:4]})  # cap at 4 lines per block for fit
    return out


# -------------------- Song specs --------------------

SHOW_NAME = "5/29/26"

SONGS = [
    # ---- New songs not in the pptx (added for the show) ----
    # tzar-li-charlie and valerie are defined further below (user-edited entries).
    {"slug": "one-way-or-another", "title": "One Way Or Another", "artist": "Blondie",
     "slides": [], "skipParse": True,
     "key": "E", "bpm": 164},
    {"slug": "smooth", "title": "Smooth", "artist": "Santana feat. Rob Thomas",
     "slides": [], "skipParse": True,
     "key": "Am", "bpm": 116},

    # ---- Songs from the pptx ----
    # NOTE: slides 3, 4, 38, 48 (modulation page) are skipped.
    {"slug": "dont-speak", "title": "Don't Speak", "artist": "No Doubt",
     "slides": [2], "key": "Bm", "bpm": 76,
     "form": "Intro → Long Verse → Chorus → Short Verse → Chorus → Bridge+Solo → Bridge (gtr+vox) → Chorus → Solo+Outro",
     "opening": "Guitar intro on Bm (×4 bars)", "ending": "End on Bm"},

    {"slug": "rehab", "title": "Rehab", "artist": "Amy Winehouse",
     "slides": [5], "key": "C major", "bpm": 71,
     "opening": "Drums + bass riff", "ending": "End on C"},

    {"slug": "blues-cnaani", "title": "בלוז כנעני", "artist": "אהוד בנאי",
     "slides": [6], "dir": "rtl", "key": "Am", "show": 9,
     "form": "פתיחה → בית → פזמון → פתיחה → בית → פזמון → מעבר → בית → פזמון → מעבר → בית → פזמון → מעבר → חצי בית → סיום"},

    {"slug": "ah-ah-ah", "title": "אה אה אה", "artist": "אפרת גוש",
     "slides": [7], "dir": "rtl", "key": "C", "show": 2,
     "form": "פתיחה → בית 1 → פזמון → בית 2 → פזמון → בית 3 → פזמון → מעבר פסנתר → בית 4 → פזמון (×4) → סיום"},

    {"slug": "kerach-9", "title": "איתו לנצח", "artist": "קרח 9",
     "slides": [8, 9], "dir": "rtl", "key": "Bb", "bpm": 160, "show": 12,
     "form": "פתיחה → בית → פזמון → פתיחה → בית → פזמון → מעבר → בית → פזמון → מעבר → Outro → פזמון*"},

    {"slug": "yehudim-kah-oti", "title": "קח אותי", "artist": "היהודים",
     "slides": [10, 11], "dir": "rtl", "skipParse": True, "show": 10},

    {"slug": "ahava-hadasha", "title": "אהבה חדשה", "artist": "אסף אמדורסקי",
     "slides": [12], "dir": "rtl", "show": 3,
     "opening": "Bass: D & E | E & G | A & B | A & C   /   Guitar: F# & G | A & B | C & B & F# & E"},

    {"slug": "everybody-hurts", "title": "Everybody Hurts", "artist": "R.E.M.",
     "slides": [13], "key": "D major", "bpm": 70},

    {"slug": "something", "title": "Something", "artist": "The Beatles",
     "slides": [14], "key": "C major", "bpm": 66},

    {"slug": "oh-darling", "title": "Oh Darling", "artist": "The Beatles",
     "slides": [15], "key": "A major", "bpm": 88,
     "timeSig": "12/8"},

    {"slug": "ksheze-amok", "title": "כשזה עמוק", "artist": "",
     "slides": [16], "dir": "rtl", "skipParse": True},

    {"slug": "under-the-bridge", "title": "Under The Bridge", "artist": "Red Hot Chili Peppers",
     "slides": [17], "key": "E major", "bpm": 86,
     "opening": "Guitar lick: D / F# (×4)"},

    {"slug": "whats-up", "title": "What's Up", "artist": "4 Non Blondes",
     "slides": [18], "key": "G major", "bpm": 130,
     "opening": "G - Am - C - Gsus2 (×2)"},

    {"slug": "feeling-good", "title": "Feeling Good", "artist": "Nina Simone",
     "slides": [19], "key": "Gm", "bpm": 76},

    {"slug": "ani-taluy", "title": "אני תלוי על הצלב", "artist": "",
     "slides": [20], "dir": "rtl", "skipParse": True,
     "opening": "Pull-off lick on Am, then E, then C (see pptx tab)"},

    {"slug": "parperei-titua", "title": "פרפרי תעתוע", "artist": "כרמלה גרוס וגנר / ערן צור",
     "slides": [21], "dir": "rtl", "skipParse": True, "show": 6},

    {"slug": "pahei-show", "title": "פחי שואו", "artist": "",
     "slides": [22], "dir": "rtl",
     "form": "פתיחה → בית → בית → פזמון → מעבר → בית → פזמון → סולו (חצי בית) → פזמון ×2 → סיום"},

    {"slug": "true-colors", "title": "True Colors", "artist": "Cyndi Lauper",
     "slides": [23], "key": "C major", "bpm": 120},

    {"slug": "son-of-a-preacher-man", "title": "Son of a Preacher Man", "artist": "Dusty Springfield",
     "slides": [24], "key": "E major", "bpm": 124},

    {"slug": "dreams", "title": "Dreams", "artist": "The Cranberries",
     "slides": [25], "key": "E major", "bpm": 138,
     "form": "Intro → Verse 1 → Bridge → Verse 2 → Outro"},

    {"slug": "powerful", "title": "Powerful", "artist": "",
     "slides": [26], "key": "Bm"},

    {"slug": "purple-rain", "title": "Purple Rain", "artist": "Prince",
     "slides": [27], "key": "Bb major", "bpm": 60,
     "opening": "Bbadd9/D - Gm7add11 - F - Eb"},

    {"slug": "ziggy-stardust", "title": "Ziggy Stardust", "artist": "David Bowie",
     "slides": [28], "key": "G major", "bpm": 138},

    {"slug": "take-me-out", "title": "Take Me Out", "artist": "Franz Ferdinand",
     "slides": [29], "key": "Em", "bpm": 105},

    {"slug": "easy", "title": "Easy", "artist": "Commodores",
     "slides": [30], "skipParse": True},

    {"slug": "give-it-away", "title": "Give it Away", "artist": "Red Hot Chili Peppers",
     "slides": [31], "key": "Am", "bpm": 102},

    {"slug": "shir-hamakolet", "title": "שיר המכולת", "artist": "כוורת",
     "slides": [32], "dir": "rtl", "skipParse": True, "show": 7},

    {"slug": "yeled-mizdaken", "title": "ילד מזדקן", "artist": "",
     "slides": [33], "dir": "rtl", "skipParse": True},

    {"slug": "ballad-of-a-thin-man", "title": "Ballad of a Thin Man", "artist": "Bob Dylan",
     "slides": [34], "key": "Am", "bpm": 100},

    {"slug": "mishehu", "title": "מישהו פעם", "artist": "עברי לידר",
     "slides": [35], "dir": "rtl", "skipParse": True, "show": 8},

    {"slug": "nitzotzot", "title": "ניצוצות", "artist": "ברי סחרוף ורמי פורטיס",
     "slides": [36], "dir": "rtl", "key": "Am", "show": 13,
     "opening": "Intro: Am – C – Fmaj7 – Dadd9 (×4)",
     "ending": "Outro on C – G/B – D"},

    {"slug": "after-midnight", "title": "After Midnight", "artist": "JJ Cale / Eric Clapton",
     "slides": [37], "key": "D major", "bpm": 124,
     "opening": "D - G/D - D (×4)"},

    {"slug": "seven-nation-army", "title": "Seven Nation Army", "artist": "The White Stripes",
     "slides": [39, 40], "key": "Em", "bpm": 124,
     "form": "Verse 1 → Inst. Chorus → Interlude → Verse 2 → Solo → Interlude → Verse 3 → Inst. Chorus"},

    {"slug": "hakaas", "title": "הכעס", "artist": "",
     "slides": [40], "dir": "rtl", "skipParse": True,
     "form": "פתיחה (גיטרה ← בס ← תופים) → בית → פזמון → מעבר קצר → בית → פזמון → סולו (E ← G#m ← A ← B) → פזמון → פזמון → סולו (סיום)"},

    {"slug": "hamimut-holefet", "title": "חמימות חולפת", "artist": "",
     "slides": [41], "dir": "rtl", "skipParse": True,
     "opening": "גיטרה מתחילה, נכנסים עם השירה"},

    {"slug": "crazy", "title": "Crazy", "artist": "Gnarls Barkley",
     "slides": [42], "key": "Cm",
     "form": "Dm - F - Bb - A"},

    {"slug": "hacheder-haintimi", "title": "החדר האינטימי", "artist": "",
     "slides": [43], "dir": "rtl", "skipParse": True,
     "opening": "פתיחה גיטרה ואורטל מכניסה"},

    {"slug": "echake-bashadot", "title": "אחכה לך בשדות", "artist": "",
     "slides": [44], "dir": "rtl", "skipParse": True,
     "form": "בית - Break → בית → פזמון - Break → סולו - Break → בית → פזמון - Break → בית - Break → סיום"},

    {"slug": "i-put-a-spell-on-you", "title": "I Put a Spell on You", "artist": "Nina Simone",
     "slides": [45], "key": "Dm", "bpm": 70},

    {"slug": "or-hayareach", "title": "אור הירח", "artist": "",
     "slides": [46], "dir": "rtl", "skipParse": True,
     "opening": "פסנתר ושירה, כניסה של כולם אחרי 'אור הירח'"},

    {"slug": "mehapes-tshuva", "title": "מחפש תשובה", "artist": "",
     "slides": [47], "dir": "rtl", "skipParse": True,
     "opening": "כולם יחד"},

    {"slug": "lama-lo-amart-li", "title": "למה לא אמרת לי", "artist": "",
     "slides": [48], "dir": "rtl", "key": "Em",
     "opening": "כולם נכנסים בשיר"},

    {"slug": "tzar-li-charlie", "title": "צר לי צ'רלי", "artist": "כרולינה",
     "slides": [], "dir": "rtl", "key": "Dm", "skipParse": True, "show": 1,
     "opening": "12-bar blues in Dm"},

    {"slug": "valerie", "title": "Valerie", "artist": "Mark Ronson ft. Amy Winehouse",
     "slides": [], "key": "Db major", "bpm": 102, "skipParse": True, "show": 5,
     "opening": "Drums + bass groove on Db"},

    {"slug": "haperach-begani", "title": "הפרח בגני", "artist": "זהר ארגוב",
     "slides": [], "dir": "ltr", "key": "Cm", "skipParse": True, "show": 11,
     "opening": "Intro: G – Cm"},

    {"slug": "spontaneous", "title": "Spontaneous", "artist": "Netta Balter / Omree Gal-Oz",
     "slides": [], "skipParse": True,
     "key": "A major", "timeSig": "4/4",
     "opening": "Intro: A – E – F#m – D (4 bars), pickup into V"},
]

# vampire is a hand-curated chart that pre-existed; we keep its existing JSON.
VAMPIRE_SLUG = "vampire"


# -------------------- Build --------------------

def slide_lines_for(song):
    return join_slides(song["slides"])


def maybe_strip_song_header(lines, song):
    """Drop a leading title/artist banner if present."""
    title = song["title"]
    artist = song.get("artist", "")
    out = list(lines)
    # Find consecutive non-blank lines at the start that contain title/artist words
    while out and (
        title and title in out[0] or
        artist and artist in out[0] or
        out[0].strip() in {"by", title, artist}
    ):
        out.pop(0)
    return out


def build_song_json(song):
    out = {
        "title": song["title"],
        "artist": song.get("artist", ""),
        "key": song.get("key", ""),
        "bpm": song.get("bpm"),
        "timeSig": song.get("timeSig", "4/4") if song.get("bpm") or song.get("key") else "",
        "opening": song.get("opening", ""),
        "ending": song.get("ending", ""),
        "form": song.get("form", ""),
        "dir": song.get("dir", "ltr"),
        "chords": [],
        "sections": [],
        "lyrics": None,
    }
    if song.get("show"):
        out["show"] = song["show"]

    # Optional explicit form-steps override (becomes the left-sidebar list)
    if song.get("formSteps"):
        out["formSteps"] = song["formSteps"]

    # Explicit chart-data override: chord row + sections come directly from the song spec.
    # This is the source of truth for the chart view.
    if song.get("chartChords") is not None or song.get("chartSections") is not None:
        if song.get("chartChords") is not None:
            out["chords"] = song["chartChords"]
        if song.get("chartSections") is not None:
            out["sections"] = song["chartSections"]
    elif not song.get("skipParse"):
        # Auto-parse from slide text
        raw = slide_lines_for(song)
        raw = maybe_strip_song_header(raw, song)
        sections = parse_lyric_block(raw)
        if sections:
            out["chords"] = collect_chords_used(sections)
            out["sections"] = build_chart_sections(sections)

    # Lyrics: always auto-parse from slide text (unless skipParse)
    if not song.get("skipParse"):
        raw = slide_lines_for(song)
        raw = maybe_strip_song_header(raw, song)
        sections = parse_lyric_block(raw)
        cleaned_lyrics = []
        for sec in sections:
            cleaned_lines = []
            for ln in sec["lines"]:
                if isinstance(ln, str) and not ln.strip():
                    continue
                cleaned_lines.append(ln)
            if cleaned_lines:
                cleaned_lyrics.append({"section": sec["section"], "lines": cleaned_lines})
        if cleaned_lyrics:
            out["lyrics"] = cleaned_lyrics

    # If we don't have a form yet, derive from form-steps or section names
    if not out.get("form") and not out.get("formSteps"):
        if out["sections"]:
            steps = [s.get("name", "") for s in out["sections"] if s.get("name")]
            if steps:
                out["form"] = " → ".join(steps)
    return out


def write_song(song):
    data = build_song_json(song)
    # Split lyrics out to the gitignored overlay (songs-local/<slug>.json),
    # leaving the public file (songs/<slug>.json) chart-only.
    lyrics = data.pop("lyrics", None)
    data["lyrics"] = None
    p = SONGS_DIR / f"{song['slug']}.json"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    if lyrics:
        LOCAL_DIR.mkdir(exist_ok=True)
        overlay_path = LOCAL_DIR / f"{song['slug']}.json"
        overlay = {}
        if overlay_path.exists():
            try:
                overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
            except Exception:
                overlay = {}
        overlay["lyrics"] = lyrics
        if data.get("dir"):
            overlay["dir"] = data["dir"]
        overlay_path.write_text(
            json.dumps(overlay, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    # Restore lyrics on the in-memory dict so callers can inspect counts
    data["lyrics"] = lyrics
    return data


VAMPIRE_SHOW_ORDER = 4


def write_index(all_songs):
    idx = {"setlist": SHOW_NAME, "songs": []}
    # Keep vampire (pre-existing manual chart) and mark its show order.
    vampire_path = SONGS_DIR / f"{VAMPIRE_SLUG}.json"
    if vampire_path.exists():
        v = json.loads(vampire_path.read_text(encoding="utf-8"))
        # Persist show order on the per-song JSON too, so the song view can show it.
        if v.get("show") != VAMPIRE_SHOW_ORDER:
            v["show"] = VAMPIRE_SHOW_ORDER
            vampire_path.write_text(json.dumps(v, ensure_ascii=False, indent=2), encoding="utf-8")
        idx["songs"].append({
            "slug": VAMPIRE_SLUG, "title": v.get("title", "vampire"),
            "artist": v.get("artist", ""), "key": v.get("key", ""),
            "bpm": v.get("bpm"), "timeSig": v.get("timeSig", ""),
            "show": VAMPIRE_SHOW_ORDER,
        })
    for song, data in all_songs:
        entry = {
            "slug": song["slug"],
            "title": data["title"],
            "artist": data["artist"],
            "key": data.get("key", ""),
            "bpm": data.get("bpm"),
            "timeSig": data.get("timeSig", ""),
        }
        if song.get("show"):
            entry["show"] = song["show"]
        idx["songs"].append(entry)
    (SONGS_DIR / "index.json").write_text(
        json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def merge_charts():
    """Merge entries from song-charts.py CHARTS dict into each SONGS entry."""
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        # Allow filename with hyphen via importlib
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "song_charts", Path(__file__).parent / "song-charts.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        charts = mod.CHARTS
    except Exception as e:
        sys.stderr.write(f"  (no song-charts overrides: {e})\n")
        return
    for song in SONGS:
        ov = charts.get(song["slug"])
        if not ov:
            continue
        for k, v in ov.items():
            song[k] = v


def main():
    SONGS_DIR.mkdir(parents=True, exist_ok=True)
    merge_charts()
    built = []
    for song in SONGS:
        data = write_song(song)
        sec_count = len(data.get("sections") or [])
        lyr_sections = len(data.get("lyrics") or [])
        chord_count = len(data.get("chords") or [])
        marker = "✓" if sec_count else " "
        sys.stdout.write(f"  {marker} {song['slug']:34} chords={chord_count:2d} sections={sec_count:2d} lyrics={lyr_sections:2d}\n")
        built.append((song, data))
    write_index(built)
    sys.stdout.write(f"Wrote {len(built)} songs + index.json\n")


if __name__ == "__main__":
    main()
