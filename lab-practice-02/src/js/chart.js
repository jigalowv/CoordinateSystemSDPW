/**
 * chart.js — Polar radar chart (Plotly)
 * Handles: init, update, range change, clear, color interpolation
 */

window.chartModule = (() => {

  const CHART_ID = 'radar-chart';
  const SPEED_OF_LIGHT = 3e8; // m/s

  let initialized = false;
  let maxRange    = 200; // km

  /* ── Color interpolation: power ∈ [0,1] → #ffffff … #ff0000 ── */
  function powerToColor(power) {
    const p = Math.max(0, Math.min(1, power));
    // white (255,255,255) → red (255,0,0)
    const g = Math.round(255 * (1 - p));
    const b = Math.round(255 * (1 - p));
    return `rgb(255, ${g}, ${b})`;
  }

  /* ── Convert echo time → distance in km ── */
  function timeToKm(timeSec) {
    return (timeSec * SPEED_OF_LIGHT) / 2 / 1000;
  }

  /* ── Build Plotly layout ── */
  function buildLayout() {
    const tickStep = maxRange / 5;
    return {
      paper_bgcolor: 'transparent',
      plot_bgcolor:  'transparent',
      font: {
        family: "'Share Tech Mono', monospace",
        color:  '#6b4870',
        size:    9,
      },
      polar: {
        bgcolor: '#0d0a0e',
        radialaxis: {
          range:       [0, maxRange],
          dtick:       tickStep,
          ticksuffix:  ' km',
          tickfont:    { color: '#6b4870', size: 9 },
          gridcolor:   '#2a1830',
          linecolor:   '#3a2040',
          tickcolor:   '#2a1830',
          showline:    true,
          tickangle:   0,
        },
        angularaxis: {
          tickfont:  { color: '#8b4d90', size: 9 },
          gridcolor: '#2a1830',
          linecolor: '#3a2040',
          direction: 'clockwise',
          rotation:  90,
          dtick:     30,
        },
      },
      margin: { t: 36, b: 16, l: 16, r: 16 },
      showlegend: false,
    };
  }

  /* ── Init chart ── */
  function init() {
    Plotly.newPlot(
      CHART_ID,
      [{
        type:          'scatterpolar',
        mode:          'markers',
        r:             [],
        theta:         [],
        marker: {
          color:   [],
          size:    20,         // fixed size
          opacity: [],
          line:    { width: 0 },
        },
        hovertemplate: '<b>Dist:</b> %{r:.1f} km<br><b>Angle:</b> %{theta:.1f}°<extra></extra>',
      }],
      buildLayout(),
      { displayModeBar: false, responsive: true }
    );
    initialized = true;
  }

  /* ── Render target array ── */
  function render(targets) {
    if (!initialized) init();
    if (targets.length === 0) {
      Plotly.restyle(CHART_ID, { r: [[]], theta: [[]], 'marker.color': [[]], 'marker.opacity': [[]] }, 0);
      return;
    }
    Plotly.restyle(CHART_ID, {
      r:              [targets.map(t => t.r)],
      theta:          [targets.map(t => t.theta)],
      'marker.color': [targets.map(t => powerToColor(t.power))],
      'marker.opacity': [targets.map(t => 0.55 + t.power * 0.45)],
    }, 0);
  }

  /* ── Update max range ── */
  function setRange(km) {
    maxRange = km || 200;
    if (initialized) {
      Plotly.relayout(CHART_ID, {
        'polar.radialaxis.range': [0, maxRange],
        'polar.radialaxis.dtick': maxRange / 5,
      });
    }
  }

  /* ── Clear ── */
  function clear() {
    if (initialized) {
      Plotly.restyle(CHART_ID, { r: [[]], theta: [[]], 'marker.color': [[]], 'marker.opacity': [[]] }, 0);
    }
  }

  return { init, render, clear, setRange, timeToKm, powerToColor };
})();