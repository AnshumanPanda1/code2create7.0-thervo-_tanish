import re
import json

# Read HTML dashboard
with open("C:/Claude_projects/acm/AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html", "r", encoding="utf-8") as f:
    html = f.read()

print("Original HTML file size:", len(html), "bytes.")

# 1. Update CSS styles for compact header, popover settings, status strip, thin pipeline indicator, and KPI row
compact_css = """
  /* ─── ENTERPRISE COMPACT HEADER (46px) ─── */
  .app-header {
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border-light);
    height: 46px;
    padding: 0 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .header-brand {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .brand-logo {
    display: flex;
    align-items: center;
    gap: 6px;
    color: var(--brand-primary);
  }

  .brand-title {
    font-weight: 700;
    font-size: 15px;
    letter-spacing: -0.4px;
    color: var(--text-primary);
  }

  .brand-divider { color: var(--border-color); font-size: 13px; }
  .brand-subtitle { font-size: 11px; font-weight: 500; color: var(--text-muted); }

  .app-nav {
    display: flex;
    align-items: center;
    gap: 2px;
  }

  .nav-link {
    padding: 4px 10px;
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    font-size: 12px;
    border-radius: 4px;
    transition: all 0.15s;
  }

  .nav-link:hover { color: var(--text-primary); background: var(--bg-subtle); }
  .nav-link.active { background: var(--brand-light); color: var(--brand-primary); font-weight: 600; }

  .header-controls {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .facility-selector {
    display: flex;
    align-items: center;
    gap: 4px;
    background: var(--bg-subtle);
    border: 1px solid var(--border-light);
    border-radius: 4px;
    padding: 2px 6px;
  }

  .facility-selector select {
    background: transparent;
    border: none;
    font-family: inherit;
    font-size: 11px;
    font-weight: 500;
    color: var(--text-primary);
    outline: none;
    cursor: pointer;
  }

  .status-pill-enterprise {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    font-weight: 600;
    color: #166534;
  }

  .pulse-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--risk-low);
    box-shadow: 0 0 0 2px rgba(22, 163, 74, 0.2);
  }

  .model-badge {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 10px;
    font-weight: 600;
    color: var(--brand-primary);
    background: var(--brand-light);
    border: 1px solid #bfdbfe;
    padding: 2px 6px;
    border-radius: 4px;
  }

  .model-badge-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--brand-primary);
  }

  .user-profile {
    display: flex;
    align-items: center;
    gap: 6px;
    padding-left: 8px;
    border-left: 1px solid var(--border-light);
  }

  .avatar {
    width: 24px; height: 24px;
    border-radius: 50%;
    background: var(--text-primary);
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 600;
  }

  .user-role { font-size: 11px; color: var(--text-muted); font-weight: 500; }

  /* ─── CONSOLIDATED CONTROL BAR & SETTINGS POPOVER (38px) ─── */
  .top-demo-bar {
    background: #ffffff;
    border-bottom: 1px solid var(--border-light);
    padding: 4px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    position: sticky;
    top: 46px;
    z-index: 99;
    height: 38px;
  }

  .td-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .mode-toggle-group {
    display: flex;
    align-items: center;
    background: var(--bg-subtle);
    border: 1px solid var(--border-light);
    border-radius: 4px;
    padding: 1px;
    gap: 1px;
  }

  .mode-btn {
    border: none;
    background: transparent;
    font-family: inherit;
    font-size: 10px;
    font-weight: 600;
    color: var(--text-muted);
    padding: 3px 8px;
    border-radius: 3px;
    cursor: pointer;
    transition: all 0.15s;
  }

  .mode-btn.active {
    background: var(--brand-primary);
    color: #ffffff;
    font-weight: 700;
  }

  .td-btn-group {
    display: flex;
    align-items: center;
    gap: 4px;
  }

  /* SIMULATION SETTINGS POPOVER */
  .popover-container {
    position: relative;
    display: inline-block;
  }

  .popover-panel {
    display: none;
    position: absolute;
    top: calc(100% + 6px);
    right: 0;
    width: 320px;
    background: #ffffff;
    border: 1px solid var(--border-light);
    border-radius: 6px;
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
    padding: 14px;
    z-index: 200;
    flex-direction: column;
    gap: 12px;
  }

  .popover-panel.show { display: flex; }

  .popover-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border-light);
    padding-bottom: 8px;
    font-size: 11px;
    font-weight: 700;
    color: var(--text-primary);
  }

  .popover-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .popover-label {
    font-size: 10px;
    font-weight: 700;
    color: var(--text-muted);
    display: flex;
    justify-content: space-between;
  }

  /* ─── SINGLE COMPACT STATUS STRIP (26px) ─── */
  .status-strip {
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border-light);
    padding: 3px 20px;
    display: flex;
    align-items: center;
    gap: 14px;
    height: 26px;
    font-size: 11px;
    overflow-x: auto;
  }

  .strip-item {
    display: flex;
    align-items: center;
    gap: 5px;
    white-space: nowrap;
  }

  .strip-label { font-size: 10px; font-weight: 600; color: var(--text-muted); }
  .strip-val { font-size: 11px; font-weight: 600; color: var(--text-primary); }
  .strip-val.status-ok { color: var(--risk-low); }
  .strip-divider { width: 1px; height: 12px; background: var(--border-light); }

  /* ─── THIN PIPELINE PROCESS INDICATOR (30px) ─── */
  .decision-flow-bar {
    background: var(--bg-subtle);
    border-bottom: 1px solid var(--border-light);
    padding: 4px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 30px;
    gap: 6px;
  }

  .df-step {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 10px;
    font-weight: 600;
    color: var(--text-muted);
    padding: 2px 8px;
    border-radius: 4px;
    position: relative;
    cursor: help;
  }

  .df-step.highlight { color: var(--brand-primary); font-weight: 700; background: var(--brand-light); }

  .df-step .df-tooltip {
    display: none;
    position: absolute;
    top: calc(100% + 4px);
    left: 50%;
    transform: translateX(-50%);
    background: #0f172a;
    color: #ffffff;
    padding: 6px 10px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 400;
    white-space: nowrap;
    z-index: 300;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }

  .df-step:hover .df-tooltip { display: block; }
  .df-arrow { color: var(--border-color); font-weight: 700; font-size: 10px; }

  /* ─── COMPACT KPI ROW (56px) ─── */
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 10px;
  }

  .kpi-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-light);
    border-radius: 6px;
    padding: 8px 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 2px;
    height: 54px;
  }

  .kpi-card.primary-kpi {
    border: 1px solid #bfdbfe;
    border-left: 4px solid var(--brand-primary);
    background: #eff6ff;
  }

  .kpi-label { font-size: 9px; font-weight: 700; color: var(--text-muted); letter-spacing: 0.3px; }
  .kpi-value { font-size: 16px; font-weight: 700; color: var(--text-primary); line-height: 1.2; }
  .kpi-card.primary-kpi .kpi-value { font-size: 18px; color: var(--brand-primary); }

  /* ─── DENSE DASHBOARD GRID ─── */
  .dashboard-body {
    padding: 14px 20px;
    max-width: 1720px;
    margin: 0 auto;
  }

  .dashboard-grid {
    display: grid;
    grid-template-columns: 1fr 370px;
    gap: 16px;
    align-items: start;
  }

  /* ACCORDION / TOGGLES FOR LEVEL 3 DETAIL IN RACK PANEL */
  .rack-detail-section {
    border: 1px solid var(--border-light);
    border-radius: 6px;
    background: var(--bg-surface);
    overflow: hidden;
  }

  .rds-head {
    padding: 8px 12px;
    background: var(--bg-subtle);
    font-size: 10px;
    font-weight: 700;
    color: var(--text-muted);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .rds-body { padding: 10px; display: flex; flex-direction: column; gap: 8px; }
"""

# Replace stylesheet section in HTML
html = re.sub(r'/\* ─── APP HEADER ─── \*/.*?(?=</style>)', compact_css, html, flags=re.DOTALL)

# 2. Update Header HTML
header_html = """<!-- TOP ENTERPRISE NAVIGATION BAR -->
<header class="app-header">
  <div class="header-brand">
    <div class="brand-logo">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <rect x="2" y="2" width="20" height="8" rx="2"></rect>
        <rect x="2" y="14" width="20" height="8" rx="2"></rect>
        <line x1="6" y1="6" x2="6.01" y2="6"></line>
        <line x1="6" y1="18" x2="6.01" y2="18"></line>
      </svg>
      <span class="brand-title">THERVO</span>
    </div>
    <span class="brand-divider">/</span>
    <span class="brand-subtitle">Predictive Thermal Intelligence</span>
  </div>

  <nav class="app-nav">
    <a href="#overview" class="nav-link active" data-tab="overview">Overview</a>
    <a href="#thermal-map" class="nav-link" data-tab="thermal-map">Thermal Map</a>
    <a href="#racks" class="nav-link" data-tab="racks">Racks</a>
    <a href="#predictions" class="nav-link" data-tab="predictions">Predictions</a>
    <a href="#events" class="nav-link" data-tab="events">Events</a>
  </nav>

  <div class="header-controls">
    <div class="facility-selector">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
      <select id="facilitySelect">
        <option value="dc-01">DC-01 / Primary Facility (US-East)</option>
        <option value="dc-02">DC-02 / Secondary Facility (US-West)</option>
        <option value="dc-03">DC-03 / EU-Central Ops</option>
      </select>
    </div>

    <div class="status-pill-enterprise">
      <span class="pulse-dot"></span>
      <span class="status-label" id="statusText">SYSTEM OPERATIONAL</span>
    </div>

    <div class="model-badge">
      <span class="model-badge-dot"></span>
      <span>MODEL ACTIVE</span>
    </div>

    <div class="user-profile">
      <span class="avatar">SR</span>
      <span class="user-role">SRE Lead</span>
    </div>
  </div>
</header>"""

html = re.sub(r'<header class="app-header">.*?</header>', header_html, html, flags=re.DOTALL)

# 3. Update Consolidated Control Bar & Popover HTML
top_bar_html = """<!-- CONSOLIDATED DEMO CONTROL BAR & SETTINGS POPOVER -->
<div class="top-demo-bar">
  <div class="td-group">
    <!-- 3-MODE ARCHITECTURE SWITCHER -->
    <div class="mode-toggle-group">
      <button class="mode-btn active" id="btnModeDemo">⚡ DEMO MODE</button>
      <button class="mode-btn" id="btnModeReplay">● ALIBABA GPU TRACE</button>
      <button class="mode-btn" id="btnModeIpmi">🔬 IPMI PHYSICAL SENSORS</button>
    </div>

    <!-- PRIMARY DEMO ACTION BUTTONS -->
    <div class="td-btn-group" id="demoControlsGroup">
      <button class="btn btn-navy btn-sm" id="btnRun">▶ Run Sim</button>
      <button class="btn btn-outline btn-sm" id="btnStop">■ Stop</button>
      <button class="btn btn-stress btn-sm" id="btnInjectSpike">⚡ Inject Spike</button>
      <button class="btn btn-success-enterprise btn-sm" id="btnCoolAll">❄ Cool Critical</button>
    </div>

    <!-- REPLAY CONTROLS (Active in Replay Mode) -->
    <div class="td-btn-group" id="replayControlsGroup" style="display: none;">
      <button class="btn btn-navy btn-sm" id="btnReplayPlayPause">▶ Replay</button>
      <button class="btn btn-outline btn-sm" id="btnReplayStepBack">⏮ Back</button>
      <button class="btn btn-outline btn-sm" id="btnReplayStepForward">⏭ Next</button>
      
      <div class="speed-selector-group">
        <span class="td-label" style="font-size:9px;">SPEED:</span>
        <button class="speed-btn active" data-speed="1">1x</button>
        <button class="speed-btn" data-speed="5">5x</button>
        <button class="speed-btn" data-speed="10">10x</button>
        <button class="speed-btn" data-speed="25">25x</button>
      </div>

      <div class="replay-time-display">
        <span class="pulse-dot-blue"></span>
        <span class="mono" id="replayTimeText" style="font-weight:700; color:var(--brand-primary); font-size:11px;">Day 01 · 00:00:00 UTC</span>
      </div>

      <button class="btn btn-outline btn-sm" id="btnOpenProvenance" title="View Data Provenance">Provenance</button>
    </div>
  </div>

  <!-- RIGHT SIDE: SIMULATION SETTINGS POPOVER BUTTON & SCRUBBER -->
  <div class="td-group">
    <!-- SCRUBBER (Replay Mode) -->
    <div class="td-sliders-group" id="replayScrubberGroup" style="display: none;">
      <div class="td-slider-item" style="gap:6px;">
        <span class="td-label" style="font-size:9px;">SCRUBBER:</span>
        <input type="range" id="replayScrubber" min="0" max="143" value="0" step="1" style="width:160px;">
        <span class="mono" id="scrubberStepText" style="font-size:10px; color:var(--text-muted); white-space:nowrap;">Step 1/144</span>
      </div>
    </div>

    <!-- POPOVER SETTINGS TOGGLE -->
    <div class="popover-container">
      <button class="btn btn-outline btn-sm" id="btnToggleSettings">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
        Simulation Settings ▾
      </button>
      
      <div class="popover-panel" id="settingsPopover">
        <div class="popover-head">
          <span>SIMULATION & WORKLOAD SETTINGS</span>
          <button style="border:none;background:transparent;cursor:pointer;" id="btnCloseSettings">&times;</button>
        </div>
        <div class="popover-item">
          <div class="popover-label"><span>SIMULATION SPEED</span><span id="speedVal" class="mono" style="color:var(--brand-primary)">1x</span></div>
          <input type="range" id="speedSlider" min="1" max="5" value="1" step="1">
        </div>
        <div class="popover-item">
          <div class="popover-label"><span>SYNTHETIC WORKLOAD BASE</span><span id="loadVal" class="mono" style="color:var(--brand-primary)">60%</span></div>
          <input type="range" id="loadSlider" min="10" max="100" value="60" step="5">
        </div>
        <div class="popover-item">
          <div class="popover-label"><span>NOISE & DRIFT FLUCTUATION</span><span id="noiseVal" class="mono" style="color:var(--brand-primary)">12%</span></div>
          <input type="range" id="noiseSlider" min="0" max="30" value="12" step="1">
        </div>
      </div>
    </div>
  </div>
</div>"""

html = re.sub(r'<div class="top-demo-bar">.*?</div>\n</div>', top_bar_html, html, flags=re.DOTALL)
if "top-demo-bar" not in html or "btnToggleSettings" not in html:
    html = re.sub(r'<div class="top-demo-bar">.*?</div>\n</div>\n</div>', top_bar_html, html, flags=re.DOTALL)

# 4. Update Compact Status Strip HTML
status_strip_html = """<!-- SINGLE COMPACT OPERATIONAL STATUS STRIP -->
<div class="status-strip">
  <div class="strip-item">
    <span class="pulse-dot"></span>
    <span class="strip-val status-ok">SYSTEM OPERATIONAL</span>
  </div>
  <div class="strip-divider"></div>
  <div class="strip-item">
    <span class="strip-label">Thermal Risk:</span>
    <span class="strip-val" id="stripHotZones">0 racks</span>
  </div>
  <div class="strip-divider"></div>
  <div class="strip-item">
    <span class="strip-label">Cooling:</span>
    <span class="strip-val" id="stripCoolingActive">0 active</span>
  </div>
  <div class="strip-divider"></div>
  <div class="strip-item">
    <span class="strip-label">Model:</span>
    <span class="strip-val" style="color:var(--brand-primary)">GNN + XGBoost (Live)</span>
  </div>
  <div class="strip-divider"></div>
  <div class="strip-item">
    <span class="strip-label">Last Update:</span>
    <span class="strip-val mono" id="stripLastUpdate">0s ago</span>
  </div>
</div>"""

html = re.sub(r'<div class="status-strip">.*?</div>', status_strip_html, html, flags=re.DOTALL)

# 5. Update Thin Pipeline Process Indicator HTML with Tooltips
pipeline_html = """<!-- STREAMLINED PROCESS INDICATOR PIPELINE -->
<div class="decision-flow-bar">
  <div class="df-step highlight">
    <span>1. WORKLOAD TELEMETRY</span>
    <div class="df-tooltip">Captures GPU, CPU, Memory & Network demand</div>
  </div>
  <span class="df-arrow">→</span>
  <div class="df-step">
    <span>2. GNN HEAT PROPAGATION</span>
    <div class="df-tooltip">Models spatial heat influence between adjacent racks</div>
  </div>
  <span class="df-arrow">→</span>
  <div class="df-step">
    <span>3. XGBOOST RISK PREDICTION</span>
    <div class="df-tooltip">Evaluates non-linear feature risk vector via 30 decision trees</div>
  </div>
  <span class="df-arrow">→</span>
  <div class="df-step">
    <span>4. COMPOSITE THERMAL RISK</span>
    <div class="df-tooltip">Fuses XGBoost prediction (75%) + GNN spatial embedding (25%)</div>
  </div>
  <span class="df-arrow">→</span>
  <div class="df-step">
    <span>5. TARGETED COOLING INTERVENTION</span>
    <div class="df-tooltip">Triggers automated proactive cooling at 72% threshold</div>
  </div>
</div>"""

html = re.sub(r'<div class="decision-flow-bar">.*?</div>', pipeline_html, html, flags=re.DOTALL)

# 6. Add JS handler for Popover Toggle
popover_js = """
// Popover Toggle Event Listener
document.getElementById('btnToggleSettings')?.addEventListener('click', (e) => {
  e.stopPropagation();
  document.getElementById('settingsPopover')?.classList.toggle('show');
});

document.getElementById('btnCloseSettings')?.addEventListener('click', () => {
  document.getElementById('settingsPopover')?.classList.remove('show');
});

document.addEventListener('click', (e) => {
  const pop = document.getElementById('settingsPopover');
  const btn = document.getElementById('btnToggleSettings');
  if (pop && pop.classList.contains('show') && !pop.contains(e.target) && !btn.contains(e.target)) {
    pop.classList.remove('show');
  }
});
"""

if "btnToggleSettings" not in html:
    html = html.replace("</script>", popover_js + "\n</script>", 1)

# Write updated HTML
with open("C:/Claude_projects/acm/AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Redesign applied successfully!")
