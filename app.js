// Jam — band practice charts. Plain HTML/JS, no build step.
// Routing via URL hash:
//   #              -> picker
//   #<slug>        -> chart view
//   #<slug>/lyrics -> lyrics view

const state = {
  index: null,        // { songs: [{slug,title,artist}, ...] }
  song: null,         // current song data
  slug: null,
  view: 'chart',      // 'chart' | 'lyrics'
  wakeLock: null,
};

const root = () => document.getElementById('root');

// ---------------- Boot ----------------
window.addEventListener('DOMContentLoaded', init);
window.addEventListener('hashchange', route);
window.addEventListener('keydown', onKey);
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible' && state.slug) requestWakeLock();
});

async function init() {
  applySavedTheme();
  try {
    state.index = await fetchJSON('songs/index.json');
  } catch (err) {
    showFatal(`Couldn't load songs/index.json — ${err.message}.\nMake sure you're serving via http (e.g. \`python3 -m http.server\` from the jam folder), not opening the file directly.`);
    return;
  }
  await route();
}

// ---------------- Routing ----------------
async function route() {
  const hash = location.hash.replace(/^#/, '');
  if (!hash) {
    state.song = null; state.slug = null;
    releaseWakeLock();
    document.body.classList.remove('in-song');
    renderPicker();
    return;
  }
  const [slug, view] = hash.split('/');
  state.view = view === 'lyrics' ? 'lyrics' : 'chart';
  if (state.slug !== slug) {
    try {
      state.song = await fetchJSON(`songs/${slug}.json`);
      // Try to merge a local-only lyrics overlay (gitignored: songs-local/).
      // Public site has no overlay → fetch fails silently; chart-only rendered.
      try {
        const overlay = await fetchJSON(`songs-local/${slug}.json`);
        if (overlay && overlay.lyrics) state.song.lyrics = overlay.lyrics;
      } catch (_) { /* no overlay — that's fine */ }
      state.slug = slug;
    } catch (err) {
      showFatal(`Couldn't load song "${slug}" — ${err.message}`);
      return;
    }
  }
  document.body.classList.add('in-song');
  requestWakeLock();
  renderSong();
}

// ---------------- Picker ----------------
function renderPicker() {
  const songs = state.index.songs;
  const setlistName = state.index.setlist || 'Show';
  const showSongs = songs.filter(s => s.show).slice().sort((a, b) => a.show - b.show);
  const otherSongs = songs.filter(s => !s.show);

  const cardHTML = (s, badge) => `
    <button class="song-card${s.show ? ' show-song' : ''}" data-slug="${attr(s.slug)}">
      ${badge ? `<div class="show-badge">${badge}</div>` : ''}
      <div class="title">${esc(s.title)}</div>
      <div class="artist">${esc(s.artist || '')}</div>
      <div class="meta">${songMetaLine(s)}</div>
    </button>
  `;

  const showSection = showSongs.length ? `
    <section class="setlist-section">
      <h2 class="setlist-h">🎤 ${esc(setlistName)} <span class="count">· ${showSongs.length} songs</span></h2>
      <div class="grid">
        ${showSongs.map(s => cardHTML(s, String(s.show))).join('')}
      </div>
    </section>
  ` : '';

  const otherSection = otherSongs.length ? `
    <section class="setlist-section">
      <h2 class="setlist-h other">Other songs <span class="count">· ${otherSongs.length}</span></h2>
      <div class="grid">
        ${otherSongs.map(s => cardHTML(s, '')).join('')}
      </div>
    </section>
  ` : '';

  root().innerHTML = `
    <div class="picker">
      <h1>Jam <span class="sub">band practice charts · ${songs.length} songs</span></h1>
      <div class="picker-scroll">
        ${showSection}
        ${otherSection}
      </div>
    </div>
  `;
  root().querySelectorAll('.song-card').forEach(el => {
    el.addEventListener('click', () => {
      location.hash = `#${el.dataset.slug}`;
    });
  });
}

function songMetaLine(s) {
  const parts = [];
  if (s.key) parts.push(esc(s.key));
  if (s.bpm) parts.push(`${s.bpm} bpm`);
  if (s.timeSig) parts.push(esc(s.timeSig));
  return parts.join('<span class="dot">·</span>');
}

// ---------------- Song shell ----------------
function renderSong() {
  const song = state.song;
  const slug = state.slug;
  const songsList = state.index.songs;
  const idx = songsList.findIndex(s => s.slug === slug);
  const prev = songsList[(idx - 1 + songsList.length) % songsList.length];
  const next = songsList[(idx + 1) % songsList.length];

  root().innerHTML = `
    <div class="song" dir="${song.dir === 'rtl' ? 'rtl' : 'ltr'}">
      <div class="song-head">
        <div class="title-block">
          ${song.show ? `<span class="show-pill">🎤 #${song.show}</span>` : ''}
          <span class="title">${esc(song.title)}</span>
          <span class="artist">— ${esc(song.artist || '')}</span>
        </div>
        <div class="meta">
          ${song.key    ? `<span>Key <b>${esc(song.key)}</b></span><span class="dot">·</span>` : ''}
          ${song.bpm    ? `<span><b>${song.bpm}</b> bpm</span><span class="dot">·</span>` : ''}
          ${song.timeSig? `<span>${esc(song.timeSig)}</span><span class="dot">·</span>` : ''}
          ${song.opening? `<span class="cue">▶ ${esc(song.opening)}</span>` : ''}
          ${song.opening && song.ending ? '<span class="dot">·</span>' : ''}
          ${song.ending ? `<span class="cue">■ ${esc(song.ending)}</span>` : ''}
        </div>
        <div class="view-toggle">
          <button data-view="chart"  class="${state.view==='chart' ?'active':''}">Chart</button>
          <button data-view="lyrics" class="${state.view==='lyrics'?'active':''}">Lyrics</button>
        </div>
      </div>
      <div class="song-body">
        <aside class="form-side">${renderFormSide(song)}</aside>
        <main class="song-main"><div id="view-area"></div></main>
      </div>
    </div>
  `;

  root().querySelectorAll('.view-toggle button').forEach(b => {
    b.addEventListener('click', () => setView(b.dataset.view));
  });

  if (state.view === 'lyrics') renderLyricsView(); else renderChartView();
}

function chordNamesFor(song) {
  if (!song.chords) return [];
  if (Array.isArray(song.chords)) return song.chords.filter(Boolean);
  return Object.keys(song.chords);
}

// ---------------- Form sidebar ----------------
function parseForm(song) {
  // Returns array of { text, note? } items.
  // Source of truth: song.form (string with " → " separator) or song.formSteps (array).
  if (Array.isArray(song.formSteps) && song.formSteps.length) {
    return song.formSteps.map(s => typeof s === 'string' ? { text: s } : s);
  }
  if (typeof song.form === 'string' && song.form.trim()) {
    return song.form.split(/\s*(?:→|->|>>|»)\s*/).map(s => ({ text: s.trim() })).filter(x => x.text);
  }
  return [];
}

function renderFormSide(song) {
  const items = parseForm(song);
  if (!items.length) {
    return `<div class="lbl">Form</div>
            <ol><li class="note">No form set —<br>fill in during practice</li></ol>`;
  }
  return `
    <div class="lbl">Form</div>
    <ol>
      ${items.map(it => `<li class="${it.note ? 'note' : ''}">${esc(it.text)}</li>`).join('')}
    </ol>
  `;
}

// ---------------- Chart view ----------------
function renderChartView() {
  const song = state.song;
  const area = document.getElementById('view-area');
  area.className = '';
  area.innerHTML = `
    <div class="chart">
      <div class="chords-row" id="chordsRow" dir="ltr"></div>
      <div class="sections" id="sectionsGrid" dir="ltr"></div>
    </div>
  `;

  // chord row — `song.chords` may be an array of names or a {name: shape} object.
  const chordsRow = document.getElementById('chordsRow');
  const chordList = chordNamesFor(song);
  const customShapes = song.chordShapes || {};
  const renderableEntries = chordList.map(name => {
    const shape = customShapes[name]
      || (song.chords && !Array.isArray(song.chords) && song.chords[name])
      || window.ChordRenderer.getShape(name);
    return shape ? { name, shape } : null;
  }).filter(Boolean);

  if (renderableEntries.length) {
    const colCount = Math.min(Math.max(renderableEntries.length, 4), 10);
    chordsRow.style.gridTemplateColumns = `repeat(${colCount}, 1fr)`;
    renderableEntries.forEach(({ name, shape }) => {
      const div = document.createElement('div');
      div.style.cssText = 'width:100%;display:flex;justify-content:center';
      div.innerHTML = window.ChordRenderer.render(name, shape);
      chordsRow.appendChild(div);
    });
  } else {
    chordsRow.style.display = 'none';
  }

  // sections
  const sections = song.sections || [];
  const grid = document.getElementById('sectionsGrid');
  // pick column count: 1 col if <=3 sections, 2 if <=6, else 3
  const cols = sections.length <= 3 ? 1 : sections.length <= 6 ? 2 : 3;
  grid.classList.add(`cols-${cols}`);

  // size bars font based on the longest line, so they fit
  const maxBarsInLine = Math.max(1, ...sections.flatMap(s => (s.lines || []).map(l => l.length)));
  // approximate font sizing: more bars => smaller. clamp() handles min/max.
  const barFont = `clamp(14px, ${Math.max(1.2, 3.0 - 0.18 * maxBarsInLine)}vw, 30px)`;
  grid.style.setProperty('--bar-font', barFont);

  sections.forEach(sec => {
    const block = document.createElement('div');
    block.className = 'sec';
    const lines = (sec.lines || []).map(line => `
      <div class="bars" dir="ltr" style="font-size:${barFont}">
        <span class="sep">|</span>
        ${line.map(b => `<span class="ch">${esc(b)}</span><span class="sep">|</span>`).join(' ')}
      </div>
    `).join('');
    block.innerHTML = `
      <div class="tag">
        <span>${esc(sec.name)}</span>
        ${sec.reps ? `<span class="reps">${esc(sec.reps)}</span>` : ''}
      </div>
      ${lines}
    `;
    grid.appendChild(block);
  });
}

// ---------------- Lyrics view ----------------
function renderLyricsView() {
  const song = state.song;
  const area = document.getElementById('view-area');
  const lyrics = song.lyrics;

  if (!lyrics || !lyrics.length) {
    area.innerHTML = `
      <div class="lyrics">
        <div class="lyrics-empty">
          <div class="big">No lyrics added for this song yet.</div>
          <div>Edit <code>songs/${esc(state.slug)}.json</code> and add a <code>lyrics</code> array,<br>then press <kbd>R</kbd> to reload this song.</div>
        </div>
      </div>
    `;
    return;
  }

  // Each section gets a "weight" approximating its vertical lines (header + body lines).
  const weighted = lyrics.map(sec => ({
    sec,
    weight: 1 + (sec.lines || []).length
  }));
  const totalLines = weighted.reduce((n, w) => n + w.weight, 0);
  const colCount = totalLines > 28 ? 3 : totalLines > 14 ? 2 : 1;

  // Distribute sections into columns greedily — keep each section intact (never split).
  const cols = Array.from({ length: colCount }, () => ({ items: [], weight: 0 }));
  for (const w of weighted) {
    const target = cols.reduce((a, b) => a.weight <= b.weight ? a : b);
    target.items.push(w.sec);
    target.weight += w.weight;
  }
  const tallestCol = Math.max(...cols.map(c => c.weight));
  // Aim: tallestCol lines should fit in roughly 88vh of vertical space.
  // Each line is ~1.6× the font height (chord row + lyric row + spacing).
  const fontVh = Math.max(1.4, Math.min(2.6, 88 / (tallestCol * 2.2)));
  const fontSize = `clamp(13px, ${fontVh.toFixed(2)}vh, 30px)`;

  const colHTML = cols.map(col => {
    const inner = col.items.map(sec => {
      const dir = sec.dir || song.dir || 'ltr';
      const lines = (sec.lines || []).map(line => renderLyricLine(line, dir)).join('');
      return `
        <div class="lyric-section" dir="${dir}">
          <div class="name">${esc(sec.section || '')}</div>
          ${lines}
        </div>
      `;
    }).join('');
    return `<div class="col">${inner}</div>`;
  }).join('');

  area.innerHTML = `
    <div class="lyrics" style="font-size:${fontSize}">
      <div class="lyrics-grid">
        ${colHTML}
      </div>
    </div>
  `;
}

function renderLyricLine(line, dir) {
  // Two formats:
  //   "[F]Hate to give the [A]satisfaction"
  //   { chords: ["F","A","Bb","Bm"] }   -> chord-only line (instrumental run)
  if (typeof line === 'object' && Array.isArray(line.chords)) {
    const segs = line.chords.map(c => `<span class="seg no-text"><span class="chord">${esc(c)}</span></span>`).join('');
    return `<div class="lyric-line chord-only">${segs}</div>`;
  }
  if (line === '' || line === null) return `<div class="lyric-line">&nbsp;</div>`;
  const segments = parseLyricLine(String(line));
  if (segments.length === 0) return `<div class="lyric-line">&nbsp;</div>`;
  const html = segments.map(s => {
    const chordHtml = `<span class="chord">${esc(s.chord || ' ')}</span>`;
    const textHtml  = `<span class="text">${esc(s.text || '')}</span>`;
    const cls = ['seg'];
    if (!s.chord) cls.push('no-chord');
    if (!s.text)  cls.push('no-text');
    return `<span class="${cls.join(' ')}">${chordHtml}${textHtml}</span>`;
  }).join('');
  return `<div class="lyric-line">${html}</div>`;
}

function parseLyricLine(line) {
  // Returns [{chord, text}, ...]
  const out = [];
  const re = /\[([^\]]+)\]/g;
  let lastEnd = 0;
  let pending = null; // chord waiting for its text
  let m;
  while ((m = re.exec(line)) !== null) {
    const between = line.slice(lastEnd, m.index);
    if (pending) {
      pending.text = between;
      out.push(pending);
    } else if (between.length) {
      out.push({ chord: '', text: between });
    }
    pending = { chord: m[1], text: '' };
    lastEnd = m.index + m[0].length;
  }
  if (pending) {
    pending.text = line.slice(lastEnd);
    out.push(pending);
  } else if (lastEnd < line.length) {
    out.push({ chord: '', text: line.slice(lastEnd) });
  }
  return out;
}

// ---------------- View / song switching ----------------
function setView(v) {
  if (!state.slug) return;
  location.hash = v === 'lyrics' ? `#${state.slug}/lyrics` : `#${state.slug}`;
}

function gotoSong(delta) {
  if (!state.slug) return;
  const list = state.index.songs;
  const i = list.findIndex(s => s.slug === state.slug);
  const next = list[(i + delta + list.length) % list.length];
  location.hash = `#${next.slug}` + (state.view === 'lyrics' ? '/lyrics' : '');
}

async function reloadSong() {
  if (!state.slug) return;
  try {
    state.song = await fetchJSON(`songs/${state.slug}.json?ts=${Date.now()}`);
    try {
      const overlay = await fetchJSON(`songs-local/${state.slug}.json?ts=${Date.now()}`);
      if (overlay && overlay.lyrics) state.song.lyrics = overlay.lyrics;
    } catch (_) { /* no overlay */ }
    renderSong();
  } catch (err) {
    showFatal(`Reload failed: ${err.message}`);
  }
}

// ---------------- Keyboard ----------------
function onKey(e) {
  // Don't intercept when user is typing in an input
  if (e.target && /input|textarea|select/i.test(e.target.tagName)) return;

  switch (e.key) {
    case 'f': case 'F':
      toggleFullscreen(); break;
    case 'l': case 'L':
      if (state.slug) setView('lyrics'); break;
    case 'c': case 'C':
      if (state.slug) setView('chart'); break;
    case 'ArrowLeft':
      gotoSong(-1); break;
    case 'ArrowRight':
      gotoSong(+1); break;
    case 'r': case 'R':
      if (state.slug) reloadSong(); break;
    case 't': case 'T':
      cycleTheme(); break;
    case 'Escape':
      if (state.slug) location.hash = '';
      break;
    case 's': case 'S':
      location.hash = '';
      break;
  }
}

// ---------------- Fullscreen ----------------
async function toggleFullscreen() {
  if (!document.fullscreenElement) {
    try {
      await document.documentElement.requestFullscreen();
      document.body.classList.add('fullscreen');
    } catch (err) { /* ignore */ }
  } else {
    await document.exitFullscreen();
    document.body.classList.remove('fullscreen');
  }
}

document.addEventListener('fullscreenchange', () => {
  if (document.fullscreenElement) {
    document.body.classList.add('fullscreen');
    // Fullscreen transition can drop the wake lock — re-acquire and
    // re-start the silent-video keep-awake fallback.
    if (state.slug) requestWakeLock();
  } else {
    document.body.classList.remove('fullscreen');
  }
});

// Re-request wake lock whenever the user clicks/presses something — Safari
// in particular requires a gesture to start media playback.
['click', 'keydown', 'touchstart'].forEach(ev => {
  window.addEventListener(ev, () => {
    if (state.slug && !state.wakeLock) requestWakeLock();
  }, { passive: true });
});

// ---------------- Wake Lock ----------------
// Two layers of protection against the screen turning off / screensaver:
//   1. Screen Wake Lock API (Chrome/Edge/Firefox 126+ on https/localhost).
//      Auto-released by the browser when the tab is hidden — we re-acquire
//      on visibilitychange and on a periodic ping.
//   2. Silent looping <video> playback fallback. Some macOS/iOS configurations
//      ignore the Wake Lock; an actively-playing media element keeps the
//      display awake even when Wake Lock is unavailable.

let wakeLockPing = null;
let silentVideoEl = null;

async function requestWakeLock() {
  startSilentVideo();
  if (!('wakeLock' in navigator)) {
    setWakeLockStatus('fallback', 'Wake Lock API not supported — using silent-video fallback');
    return;
  }
  if (state.wakeLock) return;
  try {
    state.wakeLock = await navigator.wakeLock.request('screen');
    setWakeLockStatus('on', 'Wake lock active');
    state.wakeLock.addEventListener('release', () => {
      state.wakeLock = null;
      setWakeLockStatus('released', 'Wake lock released — will re-acquire on focus');
    });
    if (!wakeLockPing) {
      // Periodically re-acquire in case the OS-level setting drops it.
      wakeLockPing = setInterval(() => {
        if (state.slug && !state.wakeLock && document.visibilityState === 'visible') {
          requestWakeLock();
        }
      }, 30_000);
    }
  } catch (err) {
    setWakeLockStatus('error', `Wake lock failed: ${err.message}`);
  }
}

function releaseWakeLock() {
  if (state.wakeLock) {
    state.wakeLock.release().catch(() => {});
    state.wakeLock = null;
  }
  if (wakeLockPing) { clearInterval(wakeLockPing); wakeLockPing = null; }
  stopSilentVideo();
  setWakeLockStatus('off', '');
}

// ---------------- Silent video fallback ----------------
function startSilentVideo() {
  if (silentVideoEl) return;
  // A 1-pixel, silent looping video keeps macOS / iOS displays awake.
  // The data URL is a minimal mp4 (silent, ~30s loop) — this is well under 1KB.
  const v = document.createElement('video');
  v.muted = true;
  v.loop = true;
  v.playsInline = true;
  v.autoplay = true;
  v.src = 'assets/keepawake.mp4';
  v.style.cssText = 'position:fixed;top:-2px;left:-2px;width:1px;height:1px;opacity:0.01;pointer-events:none;z-index:-1';
  document.body.appendChild(v);
  silentVideoEl = v;
  v.play().catch(() => {});
}
function stopSilentVideo() {
  if (silentVideoEl) {
    silentVideoEl.pause();
    silentVideoEl.remove();
    silentVideoEl = null;
  }
}

// ---------------- Wake-lock UI badge ----------------
function setWakeLockStatus(state_, msg) {
  let el = document.getElementById('wake-status');
  if (!el) {
    el = document.createElement('div');
    el.id = 'wake-status';
    el.className = 'wake-status';
    document.body.appendChild(el);
  }
  const labels = {
    'on':       { text: '🔒 screen on',  cls: 'on' },
    'fallback': { text: '🎬 video keep-awake', cls: 'on' },
    'released': { text: '⚠ wake lock released', cls: 'warn' },
    'error':    { text: '⚠ wake lock failed', cls: 'warn' },
    'off':      { text: '', cls: 'off' },
  };
  const lab = labels[state_] || labels.off;
  el.className = `wake-status ${lab.cls}`;
  el.textContent = lab.text;
  el.title = msg || '';
  if (state_ === 'on' || state_ === 'fallback') {
    // hide after 3s
    clearTimeout(el._t);
    el._t = setTimeout(() => { el.style.opacity = '0.15'; }, 3000);
    el.style.opacity = '0.95';
  }
}

// ---------------- Theme ----------------
function applySavedTheme() {
  const t = localStorage.getItem('jam-theme');
  if (t === 'light' || t === 'dark') document.body.classList.add(`theme-${t}`);
}
function cycleTheme() {
  const cur = localStorage.getItem('jam-theme') || 'system';
  const next = cur === 'system' ? 'dark' : cur === 'dark' ? 'light' : 'system';
  document.body.classList.remove('theme-light', 'theme-dark');
  if (next === 'system') localStorage.removeItem('jam-theme');
  else { localStorage.setItem('jam-theme', next); document.body.classList.add(`theme-${next}`); }
}

// ---------------- Utils ----------------
async function fetchJSON(url) {
  const r = await fetch(url, { cache: 'no-store' });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}
function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }[c]));
}
function attr(s) { return esc(s); }
function showFatal(msg) {
  root().innerHTML = `<div class="picker"><h1>Error</h1><pre style="white-space:pre-wrap;color:var(--text-2)">${esc(msg)}</pre></div>`;
}
