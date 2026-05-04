/**
 * ui.js — UI utilities
 * Handles: clock, system log, connection status badges
 */

window.uiModule = (() => {

  /* ── Clock ── */
  function updateClock() {
    const el = document.getElementById('clock');
    if (el) {
      el.textContent = new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC';
    }
  }
  setInterval(updateClock, 1000);
  updateClock();

  /* ── Log ── */
  function log(msg, type = '') {
    const box = document.getElementById('log-box');
    if (!box) return;
    const ts  = new Date().toISOString().slice(11, 19);
    const el  = document.createElement('div');
    el.className = type ? `log-${type}` : '';
    el.textContent = `[${ts}] ${msg}`;
    box.appendChild(el);
    box.scrollTop = box.scrollHeight;
    // Keep last 120 entries
    while (box.children.length > 120) box.removeChild(box.firstChild);
  }

  /* ── Connection status ── */
  function setConnectionState(online) {
    const dot   = document.getElementById('ws-dot');
    const label = document.getElementById('ws-label');
    const badge = document.getElementById('conn-badge');
    const btn   = document.getElementById('btn-connect');

    if (online) {
      dot.className   = 'ws-dot online';
      label.textContent = 'ONLINE';
      badge.className = 'conn-badge connected';
      badge.textContent = 'CONNECTED';
      btn.textContent   = 'DISCONNECT';
    } else {
      dot.className   = 'ws-dot';
      label.textContent = 'OFFLINE';
      badge.className = 'conn-badge';
      badge.textContent = 'DISCONNECTED';
      btn.textContent   = 'CONNECT';
    }
  }

  /* ── Live metrics ── */
  function updateMetrics({ angle, pulse, targetsPerScan, totalTracks }) {
    const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    if (angle          !== undefined) set('m-angle',   `${angle.toFixed(1)}°`);
    if (pulse          !== undefined) set('m-pulse',   `${pulse} μs`);
    if (targetsPerScan !== undefined) set('m-targets', targetsPerScan);
    if (totalTracks    !== undefined) set('m-total',   totalTracks);
  }

  /* ── Footer stats ── */
  function updateFooter(tracks, messages) {
    const el = document.getElementById('footer-stats');
    if (el) el.textContent = `TRACKS: ${tracks} · MSG: ${messages}`;
  }

  /* ── Active config display ── */
  function updateConfigDisplay({ mpr, rs, ts }) {
    const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    if (mpr !== undefined) set('cfg-mpr',  mpr);
    if (rs  !== undefined) set('cfg-rs',   `${rs} rpm`);
    if (ts  !== undefined) set('cfg-ts',   `${ts} km/h`);
  }

  /* ── API status banner ── */
  function setApiStatus(msg, color = 'var(--c-text-dim)') {
    const el = document.getElementById('api-status');
    if (!el) return;
    el.textContent = msg;
    el.style.color = color;
  }

  /* ── Target list ── */
  function addDetection(angle, dist, power) {
    const list = document.getElementById('target-list');
    if (!list) return;

    // cap at 10 visible rows
    while (list.children.length >= 10) list.removeChild(list.firstChild);

    const item = document.createElement('div');
    item.className = 'target-item';
    item.innerHTML = `
      <div><div class="ti-key">ANGLE</div><div class="ti-val">${angle.toFixed(1)}°</div></div>
      <div><div class="ti-key">DIST</div><div class="ti-val">${dist.toFixed(1)} km</div></div>
      <div><div class="ti-key">PWR</div><div class="ti-val">${(power * 100).toFixed(0)}%</div></div>
    `;
    // tint left border by power
    item.style.borderLeftColor = window.chartModule
      ? window.chartModule.powerToColor(power)
      : '#6c3870';
    list.appendChild(item);
  }

  function clearTargetList() {
    const list = document.getElementById('target-list');
    if (list) list.innerHTML = '';
  }

  return { log, setConnectionState, updateMetrics, updateFooter, updateConfigDisplay, setApiStatus, addDetection, clearTargetList };
})();