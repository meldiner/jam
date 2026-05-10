#!/usr/bin/env python3
"""
One-shot migration: move `lyrics` arrays from songs/*.json (public) to
songs-local/*.json (gitignored). The public file gets `"lyrics": null`.

Run once after introducing the overlay system. Subsequent builds via
build-songs.py also write to songs-local/ when explicit lyrics are set.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "songs"
LOCAL = ROOT / "songs-local"

LOCAL.mkdir(exist_ok=True)
moved = 0
unchanged = 0
for p in sorted(PUBLIC.glob("*.json")):
    if p.name == "index.json":
        continue
    data = json.loads(p.read_text(encoding="utf-8"))
    lyrics = data.get("lyrics")
    if not lyrics:
        unchanged += 1
        continue

    # Write the lyrics-only overlay (preserve dir + title for reference)
    overlay_path = LOCAL / p.name
    overlay = {}
    if overlay_path.exists():
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    overlay["lyrics"] = lyrics
    if "dir" in data and "dir" not in overlay:
        overlay["dir"] = data["dir"]
    overlay_path.write_text(
        json.dumps(overlay, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Strip lyrics from the public file
    data["lyrics"] = None
    p.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    moved += 1

print(f"Moved lyrics for {moved} song(s) to {LOCAL.relative_to(ROOT)}/")
print(f"Unchanged (no lyrics): {unchanged}")
