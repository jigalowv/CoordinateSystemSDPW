/**
 * config.js — Radar parameter API
 * Sends PUT /config to the radar server with updated parameters
 */

window.configModule = (() => {

  /* ── Read current host from ws-host input ── */
  function getApiBase() {
    const raw  = document.getElementById('ws-host').value.trim();
    const parts = raw.split(':');
    const host  = parts[0] || 'localhost';
    const port  = parts[1] || '4000';
    return `http://${host}:${port}`;
  }

  /* ── Apply config via PUT /config ── */
  async function apply() {
    const mpr = parseInt(document.getElementById('p-mpr').value);
    const rs  = parseInt(document.getElementById('p-rs').value);
    const ts  = parseInt(document.getElementById('p-ts').value);

    if ([mpr, rs, ts].some(isNaN)) {
      window.uiModule.setApiStatus('✗ INVALID INPUT', 'var(--c-red)');
      return;
    }

    const body = { measurementsPerRotation: mpr, rotationSpeed: rs, targetSpeed: ts };

    window.uiModule.setApiStatus('SENDING…', 'var(--c-amber)');
    window.uiModule.log(`API PUT /config: ${JSON.stringify(body)}`, 'info');

    try {
      const resp = await fetch(`${getApiBase()}/config`, {
        method:  'PUT',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(body),
      });

      if (resp.ok) {
        window.uiModule.setApiStatus('✓ CONFIG APPLIED', 'var(--c-purple-lite)');
        window.uiModule.updateConfigDisplay({ mpr, rs, ts });
        window.uiModule.log('Config applied successfully', 'ok');
      } else {
        window.uiModule.setApiStatus(`✗ HTTP ${resp.status}`, 'var(--c-red)');
        window.uiModule.log(`API error: HTTP ${resp.status}`, 'err');
      }
    } catch (e) {
      window.uiModule.setApiStatus('✗ CONN FAILED', 'var(--c-red)');
      window.uiModule.log(`API request failed: ${e.message}`, 'err');
    }

    // auto-clear status after 3 s
    setTimeout(() => window.uiModule.setApiStatus(''), 3000);
  }

  return { apply };
})();