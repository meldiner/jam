#!/usr/bin/env python3
"""Validate the latest rehearsal selection without rewriting song files."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
index = json.loads((ROOT / 'songs/index.json').read_text())
expected = ['somebody-told-me', 'milim-yafot-meele', 'yesh-li-chor-balev',
            'mehapes-tshuva', 'dont-stop-me-now', 'al-titpashti-li']
slugs = [s['slug'] for s in index['songs']]
assert len(slugs) == len(set(slugs)), 'Duplicate catalog slug'

def members(name):
    rows = [(m['position'], s['slug']) for s in index['songs']
            for m in s.get('setlists', []) if m['name'] == name]
    assert len({p for p, _ in rows}) == len(rows), 'Duplicate list position'
    return [slug for _, slug in sorted(rows)]

assert members('Jam · November 2026') == expected
assert members('Jam · Tentative') == ['ten-li-ktzat-mimcha']
assert index['setlists'][:2] == ['Jam · November 2026', 'Jam · Tentative']
for slug in slugs:
    assert (ROOT / f'songs/{slug}.json').exists(), slug
for slug in expected + ['ten-li-ktzat-mimcha']:
    song = json.loads((ROOT / f'songs/{slug}.json').read_text())
    assert song['sections'] and song['sources'], slug
    assert song.get('chartStatus') and song.get('chartNote'), slug
    assert song['lyrics'] is None and not song.get('slideImages'), slug
    assert all(section.get('unit') == 'changes' for section in song['sections']), slug
print('Rehearsal catalog, ordering, source links and draft chart data passed.')
