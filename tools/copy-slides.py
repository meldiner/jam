#!/usr/bin/env python3
"""
Copy exported pptx slide PNGs into the public slides/ directory.

Source: /tmp/jam_slides_export/slide-NN.png (produced by exporting
"Guest House.pptx" through Keynote to PDF, then pdftoppm -r 180).

The mapping comes from SONGS in build-songs.py. Songs with a non-empty
`slides` list get their slides copied to:

    slides/<slug>.png            (single slide)
    slides/<slug>-1.png ...      (multi-slide)
    slides/<slug>-lyrics.png     (for lyricsSlides)

The matching `slideImages` / `lyricsImages` paths are written by
build-songs.py into the public songs/<slug>.json — this script just
handles the binary copies.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLIDES_DIR = ROOT / "slides"
SOURCE_DIR = Path("/tmp/jam_slides_export")

sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module
SONGS = import_module("build-songs").SONGS  # type: ignore


def copy_set(slug, slides, suffix):
    """Copy slides for a song into SLIDES_DIR with `<slug><suffix>-N.png`
    (or just `<slug><suffix>.png` if a single slide). Returns the count
    of files actually copied."""
    n_copied = 0
    for i, n in enumerate(slides, 1):
        src = SOURCE_DIR / f"slide-{n:02d}.png"
        if not src.exists():
            print(f"  skip {slug}{suffix} slide {n}: {src} missing")
            continue
        dst_name = f"{slug}{suffix}-{i}.png" if len(slides) > 1 else f"{slug}{suffix}.png"
        shutil.copy2(src, SLIDES_DIR / dst_name)
        n_copied += 1
    return n_copied


def main():
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    for song in SONGS:
        slug = song["slug"]
        slides = song.get("slides") or []
        lyrics_slides = song.get("lyricsSlides") or []
        if slides:
            total += copy_set(slug, slides, "")
        if lyrics_slides:
            total += copy_set(slug, lyrics_slides, "-lyrics")
    print(f"Copied {total} slide images into {SLIDES_DIR}/")


if __name__ == "__main__":
    main()
