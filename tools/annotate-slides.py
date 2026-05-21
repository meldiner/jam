#!/usr/bin/env python3
"""Add chord-name annotations on top of exported slide PNGs.

Each entry in ANNOTATIONS targets one slide by slug, with a list of
`(text, x, y, size)` tuples in 1800×1013 image coordinates ((x,y) is the
upper-left of the text). The script reads pristine slides from
/tmp/jam_slides_export/ (re-run the Keynote PDF → pdftoppm export to
regenerate) and overwrites the copies in songs-local/slides/, so it's
idempotent — each run starts from the un-annotated source.

Run `tools/copy-slides.py` first to ensure target files exist, then this
to apply annotations.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLIDES_DIR = ROOT / "songs-local" / "slides"
SOURCE_DIR = Path("/tmp/jam_slides_export")

BLUE = (43, 87, 209)
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"

# slug → list of (text, x, y, size)
ANNOTATIONS = {
    "nitzotzot": [
        ("F",  1600, 713, 28),   # above ניצוצות in chorus
        ("(Bb)", 1480, 920, 28), # after מהקליפה (final line)
    ],
}


def slide_source(slug):
    """Map slug → pristine PDF-exported PNG. The dst filenames in
    songs-local/slides/ follow `<slug>.png` or `<slug>-N.png`; we infer
    the slide number from the existing target file's mtime+filename, but
    for now we hard-code the mapping below."""
    # Hard-coded: slug → slide number in the exported deck
    SLUG_TO_SLIDE = {
        "nitzotzot": 36,
    }
    n = SLUG_TO_SLIDE.get(slug)
    if n is None:
        return None
    return SOURCE_DIR / f"slide-{n:02d}.png"


def main():
    for slug, anns in ANNOTATIONS.items():
        src = slide_source(slug)
        dst = SLIDES_DIR / f"{slug}.png"
        # Prefer the pristine /tmp export; fall back to dst when the export
        # dir was cleared. Loses strict idempotency but keeps annotations
        # recoverable without re-exporting the pptx.
        if not src or not src.exists():
            if dst.exists():
                print(f"  {slug}: /tmp source missing, using {dst} (non-idempotent)")
                src = dst
            else:
                print(f"  skip {slug}: no source available")
                continue
        img = Image.open(src).convert("RGB")
        draw = ImageDraw.Draw(img)
        for text, x, y, size in anns:
            font = ImageFont.truetype(FONT_PATH, size)
            draw.text((x, y), text, font=font, fill=BLUE)
        img.save(dst, "PNG")
        print(f"annotated {slug}: {len(anns)} mark(s) → {dst}")


if __name__ == "__main__":
    main()
