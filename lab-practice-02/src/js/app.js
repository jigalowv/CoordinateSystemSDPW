/**
 * app.js — Main application orchestrator
 * Owns: track store, message processing, demo mode
 */

window.app = (() => {

  /* ── State ── */
  let targets    = [];   // { r, theta, power, ts }
  let totalTracks = 0;
  let msgCount   = 0;
  let demoTimer  = null;
  let demoAngle  = 0;

  /* ── Process incoming WebSocket message ── */
  function onMessage(data) {
    msgCount++;

    const angle   = data.scanAngle;
    const pulse   = data.pulseDuration;
    const echoes  = Array.isArray(data.echoResponses) ? data.echoResponses : [];

    window.uiModule.updateMetrics({
      angle,
      pulse,
      targetsPerScan: echoes.length,
    });

    const minPow   = parseFloat(document.getElementById('p-minpow').value) || 0;
    const trailLen = parseInt(document.getElementById('p-trail').value)    || 5;
    const now      = Date.now();

    echoes.forEach(echo => {
      if (echo.power < minPow) return;
      const dist = window.chartModule.timeToKm(echo.time);
      targets.push({ r: dist, theta: angle, power: echo.power, ts: now });
      totalTracks++;
      window.uiModule.addDetection(angle, dist, echo.power);
    });

    _pruneTargets(trailLen, now);
    _refreshDisplay();
  }

  /* ── Prune old / excess points ── */
  function _pruneTargets(trailSweeps, now) {
    // rough sweep period based on rotation speed
    const rpm    = parseInt(document.getElementById('p-rs')?.value) || 60;
    const period = (60 / rpm) * 1000; // ms per full rotation
    const cutoff = now - trailSweeps * period;
    targets = targets.filter(t => t.ts > cutoff);
    if (targets.length > 3000) targets = targets.slice(-3000);
  }

  /* ── Refresh chart + footer ── */
  function _refreshDisplay() {
    window.chartModule.render(targets);
    window.uiModule.updateMetrics({ totalTracks });
    window.uiModule.updateFooter(targets.length, msgCount);
  }

  /* ── Clear all tracks ── */
  function clearTracks() {
    targets     = [];
    totalTracks = 0;
    window.chartModule.clear();
    window.uiModule.clearTargetList();
    window.uiModule.updateFooter(0, msgCount);
    window.uiModule.log('Track history cleared', 'info');
  }

  /* ════════════════════════════════════════════
     DEMO MODE — simulated radar sweep
  ════════════════════════════════════════════ */
  const DEMO_TARGETS = [
    { r: 80,  baseAngle: 45,  drift: 0.15 },
    { r: 140, baseAngle: 130, drift: -0.10 },
    { r: 55,  baseAngle: 220, drift: 0.22 },
    { r: 175, baseAngle: 310, drift: 0.08 },
  ];
  // drift accumulator per target
  const _driftAcc = DEMO_TARGETS.map(() => 0);

  function _demoTick() {
    demoAngle = (demoAngle + 1) % 360;
    const SPEED_C = 3e8;
    const echoes  = [];

    DEMO_TARGETS.forEach((t, i) => {
      _driftAcc[i] += t.drift;
      const effective = (t.baseAngle + Math.floor(_driftAcc[i])) % 360;
      const diff      = Math.abs(((demoAngle - effective) + 360) % 360);

      if (diff < 4 || diff > 356) {
        const jitter  = (Math.random() - 0.5) * 3;
        const dist    = t.r + jitter;
        const time    = (dist * 2 * 1000) / SPEED_C;
        const power   = 0.25 + Math.random() * 0.75;
        echoes.push({ time, power });
      }
    });

    // occasional noise blip
    if (Math.random() < 0.04) {
      const maxR = parseFloat(document.getElementById('p-range').value) || 200;
      echoes.push({
        time:  (Math.random() * maxR * 2 * 1000) / SPEED_C,
        power: Math.random() * 0.12,
      });
    }

    onMessage({ scanAngle: demoAngle, pulseDuration: 1, echoResponses: echoes });
  }

  function startDemo() {
    if (demoTimer) return;
    window.uiModule.log('Demo mode activated — simulated radar data', 'info');
    demoTimer = setInterval(_demoTick, 30); // ~33 fps sweep
  }

  function stopDemo() {
    if (demoTimer) { clearInterval(demoTimer); demoTimer = null; }
    window.uiModule.log('Demo mode stopped', 'info');
  }

  let _demoActive = false;
  function toggleDemo() {
    _demoActive = !_demoActive;
    const btn   = document.getElementById('btn-demo');
    if (_demoActive) {
      startDemo();
      if (btn) btn.textContent = '■ STOP DEMO';
    } else {
      stopDemo();
      if (btn) btn.textContent = '▶ START DEMO';
    }
  }

  /* ── Bootstrap ── */
  (function init() {
    window.chartModule.init();
    window.uiModule.log('System initialized', 'ok');
    window.uiModule.log('Connect to WS server or start Demo mode', 'info');
  })();

  return { onMessage, clearTracks, toggleDemo };
})();