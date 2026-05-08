// Inline SVG chord-diagram renderer + library of common chord shapes.
// Data shape per chord:
//   { frets: [low-E ... high-E], barre?: { fret, from, to } }
//   frets entries: 'x' (mute), 0 (open), or integer fret.
(function () {
  const LIB = {
    // A
    'A':       { frets: ['x', 0, 2, 2, 2, 0] },
    'Am':      { frets: ['x', 0, 2, 2, 1, 0] },
    'A7':      { frets: ['x', 0, 2, 0, 2, 0] },
    'Am7':     { frets: ['x', 0, 2, 0, 1, 0] },
    'Amaj7':   { frets: ['x', 0, 2, 1, 2, 0] },
    'Asus2':   { frets: ['x', 0, 2, 2, 0, 0] },
    'Asus4':   { frets: ['x', 0, 2, 2, 3, 0] },
    'A6':      { frets: ['x', 0, 2, 2, 2, 2] },
    'Aaug':    { frets: ['x', 0, 3, 2, 2, 1] },
    'Ab':      { frets: [4, 6, 6, 5, 4, 4], barre: { fret: 4, from: 0, to: 5 } },
    'Abm':     { frets: [4, 6, 6, 4, 4, 4], barre: { fret: 4, from: 0, to: 5 } },
    'Ab7':     { frets: [4, 6, 4, 5, 4, 4], barre: { fret: 4, from: 0, to: 5 } },
    'Abaug':   { frets: ['x', 'x', 2, 1, 1, 0] },

    // B
    'B':       { frets: ['x', 2, 4, 4, 4, 2], barre: { fret: 2, from: 1, to: 5 } },
    'Bm':      { frets: ['x', 2, 4, 4, 3, 2], barre: { fret: 2, from: 1, to: 5 } },
    'B7':      { frets: ['x', 2, 1, 2, 0, 2] },
    'Bm7':     { frets: ['x', 2, 4, 2, 3, 2], barre: { fret: 2, from: 1, to: 5 } },
    'Bb':      { frets: ['x', 1, 3, 3, 3, 1], barre: { fret: 1, from: 1, to: 5 } },
    'Bbm':     { frets: ['x', 1, 3, 3, 2, 1], barre: { fret: 1, from: 1, to: 5 } },
    'Bb7':     { frets: ['x', 1, 3, 1, 3, 1], barre: { fret: 1, from: 1, to: 5 } },
    'Bbm7':    { frets: ['x', 1, 3, 1, 2, 1], barre: { fret: 1, from: 1, to: 5 } },
    'Bbmaj7':  { frets: ['x', 1, 3, 2, 3, 1], barre: { fret: 1, from: 1, to: 5 } },

    // C
    'C':       { frets: ['x', 3, 2, 0, 1, 0] },
    'Cm':      { frets: ['x', 3, 5, 5, 4, 3], barre: { fret: 3, from: 1, to: 5 } },
    'C7':      { frets: ['x', 3, 2, 3, 1, 0] },
    'Cm7':     { frets: ['x', 3, 5, 3, 4, 3], barre: { fret: 3, from: 1, to: 5 } },
    'Cmaj7':   { frets: ['x', 3, 2, 0, 0, 0] },
    'Cadd9':   { frets: ['x', 3, 2, 0, 3, 0] },
    'Csus2':   { frets: ['x', 3, 0, 0, 1, 0] },
    'Csus4':   { frets: ['x', 3, 3, 0, 1, 1] },
    'C#':      { frets: ['x', 4, 6, 6, 6, 4], barre: { fret: 4, from: 1, to: 5 } },
    'C#m':     { frets: ['x', 4, 6, 6, 5, 4], barre: { fret: 4, from: 1, to: 5 } },
    'C#m7':    { frets: ['x', 4, 6, 4, 5, 4], barre: { fret: 4, from: 1, to: 5 } },
    'C#7':     { frets: ['x', 4, 3, 4, 2, 4], barre: { fret: 2, from: 1, to: 5 } },
    'Db':      { frets: ['x', 4, 6, 6, 6, 4], barre: { fret: 4, from: 1, to: 5 } },
    'Dbm':     { frets: ['x', 4, 6, 6, 5, 4], barre: { fret: 4, from: 1, to: 5 } },
    'Dbmaj7':  { frets: ['x', 4, 6, 5, 6, 4], barre: { fret: 4, from: 1, to: 5 } },
    'Dbm7':    { frets: ['x', 4, 6, 4, 5, 4], barre: { fret: 4, from: 1, to: 5 } },

    // D
    'D':       { frets: ['x', 'x', 0, 2, 3, 2] },
    'Dm':      { frets: ['x', 'x', 0, 2, 3, 1] },
    'D7':      { frets: ['x', 'x', 0, 2, 1, 2] },
    'Dm7':     { frets: ['x', 'x', 0, 2, 1, 1] },
    'Dmaj7':   { frets: ['x', 'x', 0, 2, 2, 2] },
    'Dsus2':   { frets: ['x', 'x', 0, 2, 3, 0] },
    'Dsus4':   { frets: ['x', 'x', 0, 2, 3, 3] },
    'D9':      { frets: ['x', 'x', 0, 2, 1, 0] },
    'Dadd9':   { frets: ['x', 'x', 0, 2, 3, 0] },
    'D6':      { frets: ['x', 'x', 0, 2, 0, 2] },
    'D#7':     { frets: ['x', 6, 5, 6, 4, 'x'] },
    'D7#5':    { frets: ['x', 'x', 0, 3, 3, 2] },
    'D5+':     { frets: ['x', 'x', 0, 3, 3, 2] },

    // E
    'E':       { frets: [0, 2, 2, 1, 0, 0] },
    'Em':      { frets: [0, 2, 2, 0, 0, 0] },
    'E7':      { frets: [0, 2, 0, 1, 0, 0] },
    'Em7':     { frets: [0, 2, 2, 0, 3, 0] },
    'Emaj7':   { frets: [0, 2, 1, 1, 0, 0] },
    'Eb':      { frets: ['x', 6, 5, 3, 4, 3] },
    'Ebm':     { frets: ['x', 6, 8, 8, 7, 6], barre: { fret: 6, from: 1, to: 5 } },
    'Ebm7':    { frets: ['x', 6, 8, 6, 7, 6], barre: { fret: 6, from: 1, to: 5 } },
    'E5':      { frets: [0, 2, 2, 'x', 'x', 'x'] },

    // F
    'F':       { frets: [1, 3, 3, 2, 1, 1], barre: { fret: 1, from: 0, to: 5 } },
    'Fm':      { frets: [1, 3, 3, 1, 1, 1], barre: { fret: 1, from: 0, to: 5 } },
    'F7':      { frets: [1, 3, 1, 2, 1, 1], barre: { fret: 1, from: 0, to: 5 } },
    'Fmaj7':   { frets: ['x', 'x', 3, 2, 1, 0] },
    'F#':      { frets: [2, 4, 4, 3, 2, 2], barre: { fret: 2, from: 0, to: 5 } },
    'F#m':     { frets: [2, 4, 4, 2, 2, 2], barre: { fret: 2, from: 0, to: 5 } },
    'F#7':     { frets: [2, 4, 2, 3, 2, 2], barre: { fret: 2, from: 0, to: 5 } },
    'F#m7':    { frets: [2, 4, 2, 2, 2, 2], barre: { fret: 2, from: 0, to: 5 } },
    'Gb':      { frets: [2, 4, 4, 3, 2, 2], barre: { fret: 2, from: 0, to: 5 } },
    'Gbm':     { frets: [2, 4, 4, 2, 2, 2], barre: { fret: 2, from: 0, to: 5 } },
    'Gbmaj7':  { frets: [2, 4, 3, 3, 2, 2], barre: { fret: 2, from: 0, to: 5 } },

    // G
    'G':       { frets: [3, 2, 0, 0, 0, 3] },
    'Gm':      { frets: [3, 5, 5, 3, 3, 3], barre: { fret: 3, from: 0, to: 5 } },
    'G7':      { frets: [3, 2, 0, 0, 0, 1] },
    'Gm7':     { frets: [3, 5, 3, 3, 3, 3], barre: { fret: 3, from: 0, to: 5 } },
    'Gmaj7':   { frets: [3, 2, 0, 0, 0, 2] },
    'Gsus':    { frets: [3, 'x', 0, 0, 1, 3] },
    'Gsus2':   { frets: [3, 'x', 0, 2, 3, 3] },
    'Gsus4':   { frets: [3, 'x', 0, 0, 1, 3] },
    'G#m':     { frets: [4, 6, 6, 4, 4, 4], barre: { fret: 4, from: 0, to: 5 } },
    'G6':      { frets: [3, 2, 0, 0, 0, 0] },

    // Common slash chords
    'C/G':     { frets: [3, 3, 2, 0, 1, 0] },
    'C/B':     { frets: ['x', 2, 2, 0, 1, 0] },
    'D/F#':    { frets: [2, 'x', 0, 2, 3, 2] },
    'D/A':     { frets: ['x', 0, 0, 2, 3, 2] },
    'G/B':     { frets: ['x', 2, 0, 0, 0, 3] },
    'G/A':     { frets: ['x', 0, 0, 0, 0, 3] },
    'G/D':     { frets: ['x', 'x', 0, 0, 0, 3] },
    'G/F':     { frets: [1, 'x', 0, 0, 0, 3] },
    'G/E':     { frets: [0, 'x', 0, 0, 0, 3] },
    'B/F#':    { frets: [2, 2, 4, 4, 4, 2], barre: { fret: 2, from: 0, to: 5 } },
    'A/E':     { frets: [0, 0, 2, 2, 2, 0] },
    'D/E':     { frets: [0, 'x', 0, 2, 3, 2] },
    'C6':      { frets: ['x', 3, 2, 2, 1, 0] },
    'D6':      { frets: ['x', 'x', 0, 2, 0, 2] },
    'Am6':     { frets: ['x', 0, 2, 2, 1, 2] },
    'Esus4':   { frets: [0, 2, 2, 2, 0, 0] },
    'Asus4':   { frets: ['x', 0, 2, 2, 3, 0] },
    'Csus4':   { frets: ['x', 3, 3, 0, 1, 1] },
    'F#sus4':  { frets: [2, 4, 4, 4, 2, 2], barre: { fret: 2, from: 0, to: 5 } },
    'B/Bb':    { frets: ['x', 1, 4, 4, 4, 2] },
    'A/Ab':    { frets: ['x', 'x', 6, 6, 5, 5] },
    'A/G':     { frets: [3, 0, 2, 2, 2, 0] },
    'B/F#':    { frets: [2, 2, 4, 4, 4, 2], barre: { fret: 2, from: 0, to: 5 } },
    'B':       { frets: ['x', 2, 4, 4, 4, 2], barre: { fret: 2, from: 1, to: 5 } },
    'F#':      { frets: [2, 4, 4, 3, 2, 2], barre: { fret: 2, from: 0, to: 5 } },
  };

  function getShape(name) {
    if (!name) return null;
    if (LIB[name]) return LIB[name];
    // Try a few normalizations
    const variants = [
      name.replace(/maj/i, 'maj'),
      name.replace(/^(.+?)([Mm]aj7)$/, '$1maj7'),
    ];
    for (const v of variants) if (LIB[v]) return LIB[v];
    return null;
  }

  function renderChord(name, data) {
    const SW = 70, SH = 92, xL = 12, xR = 58, yT = 22, yB = 70;
    const stringX = i => xL + (xR - xL) * i / 5;
    const played = data.frets.filter(f => typeof f === 'number' && f > 0);
    const hasOpens = data.frets.some(f => f === 0);
    const lowFret = played.length ? Math.min(...played) : 1;
    const showNut = hasOpens || lowFret <= 1;
    const shift = showNut ? 0 : lowFret - 1;
    const diagFret = f => f - shift;
    const fretY = f => yT + (yB - yT) * (diagFret(f) - 0.5) / 4;

    let s = `<svg viewBox="0 0 ${SW} ${SH}" preserveAspectRatio="xMidYMid meet">`;
    s += `<text x="${SW / 2}" y="14" font-size="14" font-weight="500" text-anchor="middle" fill="var(--text)">${escXML(name)}</text>`;

    if (showNut) {
      s += `<rect x="${xL}" y="${yT - 1.5}" width="${xR - xL}" height="3" fill="var(--text)"/>`;
    } else {
      s += `<line x1="${xL}" y1="${yT}" x2="${xR}" y2="${yT}" stroke="var(--border)" stroke-width="0.6"/>`;
      s += `<text x="${xL - 1}" y="${yT + 6}" font-size="8" text-anchor="end" fill="var(--text-2)">${shift + 1}fr</text>`;
    }
    for (let f = 1; f <= 4; f++) {
      const y = yT + (yB - yT) * f / 4;
      s += `<line x1="${xL}" y1="${y}" x2="${xR}" y2="${y}" stroke="var(--border)" stroke-width="0.6"/>`;
    }
    for (let i = 0; i < 6; i++) {
      const x = stringX(i);
      s += `<line x1="${x}" y1="${yT}" x2="${x}" y2="${yB}" stroke="var(--border)" stroke-width="0.6"/>`;
    }
    if (data.barre) {
      const b = data.barre;
      const x1 = stringX(b.from), x2 = stringX(b.to), y = fretY(b.fret);
      s += `<rect x="${x1 - 3.5}" y="${y - 3.5}" width="${x2 - x1 + 7}" height="7" rx="3.5" fill="var(--text)"/>`;
    }
    data.frets.forEach((f, i) => {
      const x = stringX(i);
      if (f === 'x') {
        s += `<text x="${x}" y="19" font-size="10" text-anchor="middle" fill="var(--text-2)">×</text>`;
      } else if (f === 0) {
        s += `<circle cx="${x}" cy="17" r="2.5" fill="none" stroke="var(--text-2)" stroke-width="1"/>`;
      } else {
        if (data.barre && data.barre.fret === f && i >= data.barre.from && i <= data.barre.to) return;
        s += `<circle cx="${x}" cy="${fretY(f)}" r="3.5" fill="var(--text)"/>`;
      }
    });
    s += '</svg>';
    return s;
  }

  function escXML(s) {
    return String(s).replace(/[<>&'"]/g, c => ({
      '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;'
    }[c]));
  }

  window.ChordRenderer = { render: renderChord, getShape, lib: LIB };
})();
