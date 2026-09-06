import re

file_path = "C:/Claude_projects/acm/AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add CSS for THERVO Switch & Resource Panel
css_to_add = """
  /* ─── THERVO VS TRADITIONAL COOLING SWITCH & RESOURCE STYLES ─── */
  .thervo-mode-switch-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--bg-subtle);
    border: 1px solid var(--border-light);
    padding: 3px 10px;
    border-radius: 20px;
  }

  .thervo-slider:before {
    position: absolute; content: ""; height: 14px; width: 14px; left: 3px; bottom: 3px; background-color: white; transition: .25s; border-radius: 50%; box-shadow: 0 1px 3px rgba(0,0,0,0.2);
  }

  input:checked + .thervo-slider {
    background-color: var(--brand-primary);
  }

  input:checked + .thervo-slider:before {
    transform: translateX(16px);
  }
"""

if "thervo-mode-switch-wrapper" not in html:
    html = html.replace("</style>", css_to_add + "\n</style>", 1)

# 2. Add Header Switch HTML
header_switch_html = """
    <!-- THERVO VS TRADITIONAL COOLING MODE SWITCH -->
    <div class="thervo-mode-switch-wrapper">
      <span style="font-size:10px; font-weight:700; color:var(--text-muted); letter-spacing:0.5px;">COOLING MODE:</span>
      <label class="thervo-toggle" style="position:relative; display:inline-block; width:36px; height:20px; cursor:pointer; margin:0;">
        <input type="checkbox" id="thervoCoolingSwitch" checked style="opacity:0; width:0; height:0;">
        <span class="thervo-slider" style="position:absolute; top:0; left:0; right:0; bottom:0; background-color:#cbd5e1; transition:.25s; border-radius:20px;"></span>
      </label>
      <span id="thervoSwitchStatusText" style="font-size:11px; font-weight:700; color:var(--brand-primary); min-width:115px;">WITH THERVO (ON)</span>
    </div>
"""

if "thervoCoolingSwitch" not in html:
    html = html.replace('<div class="model-badge">', header_switch_html + '\n    <div class="model-badge">', 1)

# 3. Add Resources Saved Panel HTML above main dashboard grid
resource_panel_html = """
  <!-- RESOURCES SAVED & COOLING COMPARISON BANNER -->
  <div class="card-panel" id="thervoResourcePanel" style="padding:14px 20px; background:linear-gradient(135deg, #eff6ff 0%, #ffffff 100%); border:1px solid #bfdbfe; border-radius:10px; margin-bottom:16px; transition:all 0.3s ease;">
    <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px;">
      <div style="display:flex; align-items:center; gap:12px;">
        <div id="thervoResourceIcon" style="width:36px; height:36px; border-radius:8px; background:var(--brand-light); color:var(--brand-primary); display:flex; align-items:center; justify-content:center; font-size:18px;">❄</div>
        <div>
          <div style="display:flex; align-items:center; gap:8px;">
            <span id="thervoResourceModeBadge" style="font-size:11px; font-weight:700; padding:2px 8px; border-radius:4px; background:#dbeafe; color:#1e40af;">WITH THERVO (PREDICTIVE COOLING)</span>
            <span id="thervoResourceSub" style="font-size:11px; color:var(--text-muted);">Targeted rack cooling active</span>
          </div>
          <h3 id="thervoResourceTitle" style="font-size:13px; font-weight:700; color:var(--text-primary); margin-top:2px;">Targeted Workload-Driven Cooling Active — Only At-Risk Racks Cooled</h3>
        </div>
      </div>

      <div style="display:flex; align-items:center; gap:20px; font-family:var(--font-mono);">
        <div>
          <div style="font-size:9px; font-weight:700; color:var(--text-muted);">ACTIVE COOLING RACKS</div>
          <div style="font-size:13px; font-weight:700; color:var(--text-primary);" id="resActiveRacks">3 / 12 (25.0%)</div>
        </div>
        <div style="width:1px; height:20px; background:var(--border-light);"></div>
        <div>
          <div style="font-size:9px; font-weight:700; color:var(--text-muted);">COOLING LOAD DEMAND</div>
          <div style="font-size:13px; font-weight:700; color:var(--brand-primary);" id="resCoolingKw">65.0 kW</div>
        </div>
        <div style="width:1px; height:20px; background:var(--border-light);"></div>
        <div>
          <div style="font-size:9px; font-weight:700; color:var(--text-muted);">RESOURCES SAVED</div>
          <div style="font-size:13px; font-weight:700; color:#16a34a;" id="resEnergySaved">35.0% (~306,600 kWh/yr)</div>
        </div>
      </div>
    </div>
  </div>
"""

if "thervoResourcePanel" not in html:
    html = html.replace('<div class="dashboard-grid">', resource_panel_html + '\n  <div class="dashboard-grid">', 1)

# 4. Add JavaScript state variable and logic
js_code_to_add = """
// ─── THERVO VS TRADITIONAL COOLING TOGGLE STATE ───
let thervoCoolingEnabled = true;

function updateThervoSwitchView() {
  const switchEl = document.getElementById('thervoCoolingSwitch');
  const labelEl = document.getElementById('thervoSwitchStatusText');
  const panelEl = document.getElementById('thervoResourcePanel');
  const modeBadgeEl = document.getElementById('thervoResourceModeBadge');
  const subEl = document.getElementById('thervoResourceSub');
  const titleEl = document.getElementById('thervoResourceTitle');
  const iconEl = document.getElementById('thervoResourceIcon');
  
  const resActiveEl = document.getElementById('resActiveRacks');
  const resKwEl = document.getElementById('resCoolingKw');
  const resSavedEl = document.getElementById('resEnergySaved');
  const energyEl = document.getElementById('energySaved');
  const coolingOnEl = document.getElementById('coolingOn');

  if (thervoCoolingEnabled) {
    if (labelEl) { labelEl.textContent = 'WITH THERVO (ON)'; labelEl.style.color = 'var(--brand-primary)'; }
    if (panelEl) { panelEl.style.background = 'linear-gradient(135deg, #eff6ff 0%, #ffffff 100%)'; panelEl.style.borderColor = '#bfdbfe'; }
    if (modeBadgeEl) { modeBadgeEl.textContent = 'WITH THERVO (PREDICTIVE COOLING)'; modeBadgeEl.style.background = '#dbeafe'; modeBadgeEl.style.color = '#1e40af'; }
    if (subEl) subEl.textContent = 'Targeted rack cooling active';
    if (titleEl) titleEl.textContent = 'Targeted Workload-Driven Cooling Active — Only At-Risk Racks Cooled';
    if (iconEl) { iconEl.textContent = '❄'; iconEl.style.background = 'var(--brand-light)'; iconEl.style.color = 'var(--brand-primary)'; }

    const activeCount = racks.filter(r => r.riskScore > 0.72).length;
    const activePct = ((activeCount / NUM_RACKS) * 100).toFixed(1);
    const coolingKw = (65.0 * (activeCount / 3.8)).toFixed(1);
    
    if (resActiveEl) resActiveEl.textContent = `${activeCount} / ${NUM_RACKS} (${activePct}%)`;
    if (resKwEl) resKwEl.textContent = `${Math.min(100, Math.max(30, coolingKw))} kW`;
    if (resSavedEl) resSavedEl.textContent = `${energySavedTotal.toFixed(1)}% (~306,600 kWh/yr)`;
    if (energyEl) { energyEl.textContent = `${energySavedTotal.toFixed(1)}%`; energyEl.className = 'kpi-value mono text-success'; }
  } else {
    if (labelEl) { labelEl.textContent = 'TRADITIONAL (OFF)'; labelEl.style.color = 'var(--risk-high)'; }
    if (panelEl) { panelEl.style.background = 'linear-gradient(135deg, #fff7ed 0%, #ffffff 100%)'; panelEl.style.borderColor = '#fed7aa'; }
    if (modeBadgeEl) { modeBadgeEl.textContent = 'TRADITIONAL COOLING (WITHOUT THERVO)'; modeBadgeEl.style.background = '#ffedd5'; modeBadgeEl.style.color = '#9a3412'; }
    if (subEl) subEl.textContent = 'Blanket / Always-On cooling active across all racks';
    if (titleEl) titleEl.textContent = 'Traditional Cooling Active — 100% Constant Cooling Capacity Running on All Racks';
    if (iconEl) { iconEl.textContent = '🔥'; iconEl.style.background = '#ffedd5'; iconEl.style.color = '#ea580c'; }

    if (resActiveEl) resActiveEl.textContent = `12 / 12 (100.0%)`;
    if (resKwEl) resKwEl.textContent = `100.0 kW (Max)`;
    if (resSavedEl) resSavedEl.textContent = `0.0% (No Savings - Baseline)`;
    if (energyEl) { energyEl.textContent = `0.0%`; energyEl.className = 'kpi-value mono text-danger'; }
    if (coolingOnEl) coolingOnEl.textContent = '12';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('thervoCoolingSwitch')?.addEventListener('change', function() {
    thervoCoolingEnabled = this.checked;
    racks.forEach(r => {
      r.coolingActive = thervoCoolingEnabled ? (r.riskScore > 0.72) : true;
    });
    if (typeof addLog === 'function') {
      if (thervoCoolingEnabled) {
        addLog('⚡ Switched to PREDICTIVE THERVO COOLING MODE (Targeted Risk-Based Cooling)', 'info');
      } else {
        addLog('● Switched to TRADITIONAL COOLING MODE (Without THERVO - 100% Blanket Cooling)', 'warn');
      }
    }
    updateThervoSwitchView();
    updateRackCards();
    renderFloorPlan();
  });
});
"""

if "thervoCoolingEnabled" not in html:
    html = html.replace("<script>", "<script>\n" + js_code_to_add, 1)

# Update coolingActive setting logic in processStep
old_cooling_logic = "rack.coolingActive = risk > 0.72;"
new_cooling_logic = "rack.coolingActive = thervoCoolingEnabled ? (risk > 0.72) : true;"
if old_cooling_logic in html:
    html = html.replace(old_cooling_logic, new_cooling_logic)

# Update coolingActive setting logic in renderReplayStep if present
old_replay_cooling = "rack.coolingActive = rack.riskScore > 0.72;"
new_replay_cooling = "rack.coolingActive = thervoCoolingEnabled ? (rack.riskScore > 0.72) : true;"
if old_replay_cooling in html:
    html = html.replace(old_replay_cooling, new_replay_cooling)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully patched AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html with THERVO Cooling Mode switch and Resources Saved panel!")
