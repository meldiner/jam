#!/usr/bin/env python3
"""
Copy exported pptx slide PNGs into songs-local/slides/ and inject a
`slideImages` array into each song's local overlay JSON.

Source: /tmp/jam_slides_export/slide-NN.png (produced by exporting
"Guest House.pptx" through Keynote to PDF, then pdftoppm -r 180).

The mapping comes from SONGS in build-songs.py. Songs with a non-empty
`slides` list get their slides copied to:

    songs-local/slides/<slug>-1.png
    songs-local/slides/<slug>-2.png
    ...

And the local overlay songs-local/<slug>.json gains a `slideImages` field
pointing at those files (relative paths the browser can fetch).
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCAL_DIR = ROOT / "songs-local"
SLIDES_DIR = LOCAL_DIR / "slides"
SOURCE_DIR = Path("/tmp/jam_slides_export")

sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module
SONGS = import_module("build-songs").SONGS  # type: ignore


def copy_set(slug, slides, suffix):
    """Copy slides for a song into SLIDES_DIR with `<slug><suffix>-N.png`
    (or just `<slug><suffix>.png` if a single slide). Returns the list of
    relative paths in browser-fetchable form."""
    rel = []
    for i, n in enumerate(slides, 1):
        src = SOURCE_DIR / f"slide-{n:02d}.png"
        if not src.exists():
            print(f"  skip {slug}{suffix} slide {n}: {src} missing")
            continue
        dst_name = f"{slug}{suffix}-{i}.png" if len(slides) > 1 else f"{slug}{suffix}.png"
        dst = SLIDES_DIR / dst_name
        shutil.copy2(src, dst)
        rel.append(f"songs-local/slides/{dst_name}")
    return rel


def main():
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    for song in SONGS:
        slug = song["slug"]
        slides = song.get("slides") or []
        lyrics_slides = song.get("lyricsSlides") or []
        if not slides and not lyrics_slides:
            continue
        chart_rel = copy_set(slug, slides, "") if slides else []
        lyrics_rel = copy_set(slug, lyrics_slides, "-lyrics") if lyrics_slides else []
        if not chart_rel and not lyrics_rel:
            continue
        total += len(chart_rel) + len(lyrics_rel)
        # Update overlay JSON
        overlay_path = LOCAL_DIR / f"{slug}.json"
        data = {}
        if overlay_path.exists():
            try:
                data = json.loads(overlay_path.read_text(encoding="utf-8"))
            except Exception:
                data = {}
        if chart_rel:
            data["slideImages"] = chart_rel
        else:
            data.pop("slideImages", None)
        if lyrics_rel:
            data["lyricsImages"] = lyrics_rel
        else:
            data.pop("lyricsImages", None)
        overlay_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"Copied {total} slide images total.")


if __name__ == "__main__":
    main()
