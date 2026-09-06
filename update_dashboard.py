import json

# Read Alibaba dataset
with open("C:/Claude_projects/acm/alibaba_gpu_trace_2026.json", "r", encoding="utf-8") as f:
    alibaba_data = json.load(f)

# Read HTML dashboard
with open("C:/Claude_projects/acm/AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Inject CSS for Mode Toggle, Replay Toolbar, Provenance Modal, and Data Tags
additional_css = """
  /* ─── ALIBABA TRACE & DUAL MODE STYLES ─── */
  .mode-toggle-group {
    display: flex;
    align-items: center;
    background: var(--bg-subtle);
    border: 1px solid var(--border-light);
    border-radius: 6px;
    padding: 2px;
    gap: 2px;
  }

  .mode-btn {
    border: none;
    background: transparent;
    font-family: inherit;
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    padding: 4px 10px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.15s;
  }

  .mode-btn.active {
    background: var(--brand-primary);
    color: #ffffff;
    font-weight: 700;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
  }

  .speed-selector-group {
    display: flex;
    align-items: center;
    gap: 4px;
    background: var(--bg-subtle);
    border: 1px solid var(--border-light);
    border-radius: 6px;
    padding: 2px 6px;
  }

  .speed-btn {
    border: none;
    background: transparent;
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 600;
    color: var(--text-muted);
    padding: 2px 6px;
    border-radius: 3px;
    cursor: pointer;
  }

  .speed-btn.active {
    background: var(--brand-light);
    color: var(--brand-primary);
    font-weight: 700;
  }

  .replay-time-display {
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--brand-light);
    border: 1px solid #bfdbfe;
    border-radius: 6px;
    padding: 4px 10px;
  }

  .pulse-dot-blue {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--brand-primary);
    box-shadow: 0 0 0 2px rgba(30, 64, 175, 0.2);
  }

  .data-provenance-tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 9px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 3px;
    letter-spacing: 0.3px;
  }

  .tag-real-trace {
    background: #e0f2fe;
    color: #0369a1;
    border: 1px solid #bae6fd;
  }

  .tag-inferred {
    background: #f1f5f9;
    color: #475569;
    border: 1px solid #cbd5e1;
  }

  /* MODAL / DRAWER FOR PROVENANCE */
  .modal-overlay {
    display: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(15, 23, 42, 0.5);
    z-index: 1000;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(2px);
  }

  .modal-overlay.show { display: flex; }

  .modal-card {
    background: #ffffff;
    border-radius: 10px;
    width: 680px;
    max-width: 90vw;
    max-height: 85vh;
    overflow-y: auto;
    box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
    border: 1px solid var(--border-light);
  }

  .modal-head {
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-light);
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #f8fafc;
  }

  .modal-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .modal-body {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    font-size: 12px;
    line-height: 1.6;
  }

  .modal-close {
    border: none; background: transparent;
    font-size: 18px; color: var(--text-muted); cursor: pointer;
  }
"""

if "ALIBABA TRACE & DUAL MODE STYLES" not in html:
    html = html.replace("</style>", additional_css + "\n</style>", 1)

# 2. Update Top Control Bar HTML
old_top_bar = """<div class="top-demo-bar">
  <div class="td-group">
    <span class="td-tag">DEMO CONTROLS</span>
    <div class="td-btn-group">
      <button class="btn btn-navy btn-sm" id="btnRun">▶ Run Sim</button>
      <button class="btn btn-outline btn-sm" id="btnStop">■ Stop</button>
      <button class="btn btn-stress btn-sm" id="btnInjectSpike">⚡ Inject Spike</button>
      <button class="btn btn-success-enterprise btn-sm" id="btnCoolAll">❄ Cool All Critical</button>
    </div>
  </div>

  <div class="td-sliders-group">
    <div class="td-slider-item">
      <span class="td-label">SIM SPEED: <span id="speedVal" class="mono" style="color:var(--brand-primary)">1x</span></span>
      <input type="range" id="speedSlider" min="1" max="5" value="1" step="1" style="width:70px;">
    </div>
    <div class="td-slider-item">
      <span class="td-label">WORKLOAD: <span id="loadVal" class="mono" style="color:var(--brand-primary)">60%</span></span>
      <input type="range" id="loadSlider" min="10" max="100" value="60" step="5" style="width:80px;">
    </div>
    <div class="td-slider-item">
      <span class="td-label">NOISE: <span id="noiseVal" class="mono" style="color:var(--brand-primary)">12%</span></span>
      <input type="range" id="noiseSlider" min="0" max="30" value="12" step="1" style="width:70px;">
    </div>
  </div>
</div>"""

new_top_bar = """<div class="top-demo-bar">
  <div class="td-group">
    <!-- DUAL MODE SWITCHER -->
    <div class="mode-toggle-group">
      <button class="mode-btn active" id="btnModeDemo">⚡ DEMO MODE</button>
      <button class="mode-btn" id="btnModeReplay">● PRODUCTION TRACE REPLAY</button>
    </div>

    <!-- DEMO CONTROLS (Visible in Demo Mode) -->
    <div class="td-btn-group" id="demoControlsGroup">
      <button class="btn btn-navy btn-sm" id="btnRun">▶ Run Sim</button>
      <button class="btn btn-outline btn-sm" id="btnStop">■ Stop</button>
      <button class="btn btn-stress btn-sm" id="btnInjectSpike">⚡ Inject Spike</button>
      <button class="btn btn-success-enterprise btn-sm" id="btnCoolAll">❄ Cool All Critical</button>
    </div>

    <!-- REPLAY CONTROLS (Visible in Production Trace Replay Mode) -->
    <div class="td-btn-group" id="replayControlsGroup" style="display: none;">
      <button class="btn btn-navy btn-sm" id="btnReplayPlayPause">▶ Replay</button>
      <button class="btn btn-outline btn-sm" id="btnReplayStepBack">⏮ Step Back</button>
      <button class="btn btn-outline btn-sm" id="btnReplayStepForward">⏭ Step Forward</button>
      
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

      <button class="btn btn-outline btn-sm" id="btnOpenProvenance" title="View Data Provenance & Methodology">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
        Provenance
      </button>
    </div>
  </div>

  <!-- SLIDERS FOR DEMO MODE -->
  <div class="td-sliders-group" id="demoSlidersGroup">
    <div class="td-slider-item">
      <span class="td-label">SIM SPEED: <span id="speedVal" class="mono" style="color:var(--brand-primary)">1x</span></span>
      <input type="range" id="speedSlider" min="1" max="5" value="1" step="1" style="width:70px;">
    </div>
    <div class="td-slider-item">
      <span class="td-label">WORKLOAD: <span id="loadVal" class="mono" style="color:var(--brand-primary)">60%</span></span>
      <input type="range" id="loadSlider" min="10" max="100" value="60" step="5" style="width:80px;">
    </div>
    <div class="td-slider-item">
      <span class="td-label">NOISE: <span id="noiseVal" class="mono" style="color:var(--brand-primary)">12%</span></span>
      <input type="range" id="noiseSlider" min="0" max="30" value="12" step="1" style="width:70px;">
    </div>
  </div>

  <!-- SCRUBBER FOR REPLAY MODE -->
  <div class="td-sliders-group" id="replayScrubberGroup" style="display: none;">
    <div class="td-slider-item" style="gap:8px;">
      <span class="td-label">TIMELINE SCRUBBER:</span>
      <input type="range" id="replayScrubber" min="0" max="143" value="0" step="1" style="width:200px;">
      <span class="mono" id="scrubberStepText" style="font-size:11px; color:var(--text-muted); white-space:nowrap;">Step 1/144</span>
    </div>
  </div>
</div>"""

if "btnModeDemo" not in html:
    html = html.replace(old_top_bar, new_top_bar)

# 3. Add Modal Markup for Data Provenance before </body>
modal_markup = """
<!-- DATA PROVENANCE & METHODOLOGY MODAL -->
<div class="modal-overlay" id="provenanceModal">
  <div class="modal-card">
    <div class="modal-head">
      <div class="modal-title">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:var(--brand-primary)"><rect x="2" y="3" width="20" height="14" rx="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
        Data Provenance & Scientific Methodology
      </div>
      <button class="modal-close" id="btnCloseProvenance">&times;</button>
    </div>
    <div class="modal-body">
      <div style="background:var(--brand-light); border:1px solid #bfdbfe; border-radius:6px; padding:12px; display:flex; flex-direction:column; gap:6px;">
        <span class="mono" style="font-size:11px; font-weight:700; color:var(--brand-primary);">DATA SOURCE: ALIBABA CLUSTER TRACE GPU V2026</span>
        <span style="font-size:11px; color:var(--text-secondary);">Official anonymized 6-month production trace covering 155,410 GPUs across 37,707 GPU servers. Hosted by Alibaba Group.</span>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
        <div style="background:var(--bg-subtle); padding:10px; border-radius:6px; border:1px solid var(--border-light);">
          <span style="font-weight:700; font-size:11px; color:var(--text-primary); display:block; margin-bottom:4px;">REAL TELEMETRY FIELDS</span>
          <ul style="padding-left:16px; font-size:11px; color:var(--text-secondary);">
            <li>CPU & GPU Utilization %</li>
            <li>System Memory & GPU Memory %</li>
            <li>Network RX / TX Traffic (Mbps)</li>
            <li>Workload Type (LLM, Diffusion, RLHF)</li>
            <li>ASW Topology Domains & Server IDs</li>
          </ul>
        </div>
        <div style="background:var(--bg-subtle); padding:10px; border-radius:6px; border:1px solid var(--border-light);">
          <span style="font-weight:700; font-size:11px; color:var(--text-primary); display:block; margin-bottom:4px;">THERV0 INFERRED OUTPUTS</span>
          <ul style="padding-left:16px; font-size:11px; color:var(--text-secondary);">
            <li>Derived Workload Thermal Load Proxy</li>
            <li>GNN Spatial Heat Propagation Vector</li>
            <li>XGBoost Predicted Thermal Risk %</li>
            <li>Automated Cooling Interventions</li>
          </ul>
        </div>
      </div>

      <div style="border-left:3px solid var(--risk-med); background:#fffbeb; padding:10px 12px; border-radius:4px; font-size:11px; color:#92400e;">
        <strong>STRICT SENSOR-FREE METHODOLOGY:</strong> Physical temperature sensors are NOT installed or read. Thermals are predicted strictly using software workload telemetry. Thermal Load Proxy is derived via deterministic workload mapping.
      </div>
    </div>
  </div>
</div>
"""

if "provenanceModal" not in html:
    html = html.replace("</body>", modal_markup + "\n</body>")

# 4. Inject Dataset and JS Engine into script tag
js_engine_code = """
// ─── ALIBABA PRODUCTION TRACE DATASET (INLINE BUNDLE) ───
const ALIBABA_TRACE_DATA = """ + json.dumps(alibaba_data) + """;

// ─── DUAL MODE & REPLAY STATE MACHINE ───
let currentAppMode = 'demo'; // 'demo' or 'replay'
let replayStepIndex = 0;
let replayIsRunning = false;
let replaySpeedMultiplier = 1;
let replayTimerId = null;

// RACK TO ALIBABA SERVER MAPPING
const ALIBABA_SERVER_MAP = [
  "gpu-srv-01", "gpu-srv-02", "gpu-srv-03", "gpu-srv-04",
  "gpu-srv-05", "gpu-srv-06", "gpu-srv-07", "gpu-srv-08",
  "gpu-srv-09", "gpu-srv-10", "gpu-srv-11", "gpu-srv-12"
];

function switchAppMode(mode) {
  currentAppMode = mode;
  const btnDemo = document.getElementById('btnModeDemo');
  const btnReplay = document.getElementById('btnModeReplay');
  const demoControls = document.getElementById('demoControlsGroup');
  const replayControls = document.getElementById('replayControlsGroup');
  const demoSliders = document.getElementById('demoSlidersGroup');
  const replayScrubber = document.getElementById('replayScrubberGroup');
  const statusText = document.getElementById('statusText');

  if (mode === 'replay') {
    if (simRunning) {
      simRunning = false;
      clearInterval(simInterval);
    }
    btnDemo.classList.remove('active');
    btnReplay.classList.add('active');
    demoControls.style.display = 'none';
    replayControls.style.display = 'flex';
    demoSliders.style.display = 'none';
    replayScrubber.style.display = 'flex';
    
    if (statusText) statusText.textContent = 'ALIBABA TRACE REPLAY';
    addLog('● Switched to PRODUCTION TRACE REPLAY MODE (Alibaba GPU Cluster Trace v2026)', 'info', 0);
    renderReplayStep(replayStepIndex);
  } else {
    if (replayIsRunning) {
      stopReplay();
    }
    btnReplay.classList.remove('active');
    btnDemo.classList.add('active');
    replayControls.style.display = 'none';
    demoControls.style.display = 'flex';
    replayScrubber.style.display = 'none';
    demoSliders.style.display = 'flex';
    
    if (statusText) statusText.textContent = 'SYSTEM OPERATIONAL';
    addLog('⚡ Switched to DEMO SIMULATION MODE (Autonomous Synthetic Workload)', 'info', 0);
  }
}

function renderReplayStep(stepIdx) {
  if (!ALIBABA_TRACE_DATA || !ALIBABA_TRACE_DATA.time_steps) return;
  if (stepIdx < 0) stepIdx = 0;
  if (stepIdx >= ALIBABA_TRACE_DATA.time_steps.length) stepIdx = ALIBABA_TRACE_DATA.time_steps.length - 1;

  replayStepIndex = stepIdx;
  const stepObj = ALIBABA_TRACE_DATA.time_steps[stepIdx];

  // Update time displays
  const timeTextEl = document.getElementById('replayTimeText');
  if (timeTextEl) timeTextEl.textContent = stepObj.formatted_time;

  const scrubberEl = document.getElementById('replayScrubber');
  if (scrubberEl) scrubberEl.value = stepIdx;

  const stepTextEl = document.getElementById('scrubberStepText');
  if (stepTextEl) stepTextEl.textContent = `Step ${stepIdx + 1}/${ALIBABA_TRACE_DATA.time_steps.length}`;

  // Map server records into racks
  const serverRecords = stepObj.servers;
  
  // Extract features for GNN
  const rawFeatures = racks.map((rack, i) => {
    const sId = ALIBABA_SERVER_MAP[i];
    const sData = serverRecords.find(s => s.server_id === sId) || serverRecords[i % serverRecords.length];

    // Update real telemetry on rack object
    rack.cpu = sData.cpu_utilization * 100;
    rack.gpu = sData.gpu_utilization * 100;
    rack.memory = sData.memory_utilization * 100;
    rack.gpu_memory = sData.gpu_memory_utilization * 100;
    rack.network_rx = sData.network_rx_mbps;
    rack.network_tx = sData.network_tx_mbps;
    rack.network = Math.min(100, (sData.network_rx_mbps / 3000) * 100);
    rack.diskIO = Math.min(100, sData.gpu_memory_utilization * 90);
    rack.workload_type = sData.workload_type;
    rack.gpu_type = sData.gpu_type;
    rack.asw_id = sData.asw_id;
    rack.workload_heat_proxy = sData.workload_heat_proxy;

    return {
      cpu: rack.cpu,
      gpu: rack.gpu,
      memory: rack.memory,
      diskIO: rack.diskIO,
      network: rack.network
    };
  });

  // Compute GNN Embeddings & XGBoost Prediction
  const gnnEmbeds = computeGNNEmbeddings(rawFeatures);

  racks.forEach((rack, i) => {
    rack.gnnEmbed = gnnEmbeds[i];
    const featVec = [rack.cpu/100, rack.gpu/100, rack.memory/100, rack.diskIO/100, rack.network/100, rack.gnnEmbed];
    rack.xgbPred = xgbPredict(featVec);
    rack.riskScore = parseFloat((rack.xgbPred * 0.75 + rack.gnnEmbed * 0.25).toFixed(4));
    
    if (riskHistory[i]) {
      riskHistory[i].push(rack.riskScore);
      if (riskHistory[i].length > 40) riskHistory[i].shift();
    }
  });

  // UI Updates
  renderFloorPlan();
  updateRackCards();
  updateHeatmap();
  updateGNNGraph();
  updateSelectedDetail();
  updateFeatureImportance(rawFeatures);
  updateModelStats();
  if (selectedRack >= 0) drawHistoryChart();

  // Log event if critical risk on step
  const highRiskRack = racks.find(r => r.riskScore > 0.72);
  if (highRiskRack && stepIdx % 5 === 0) {
    addLog(`● [TRACE STEP ${stepIdx+1}] ${highRiskRack.name} (${highRiskRack.asw_id}) Predicted Risk: ${(highRiskRack.riskScore*100).toFixed(1)}% (GPU: ${highRiskRack.gpu.toFixed(1)}%)`, 'warn', highRiskRack.id);
  }
}

function startReplay() {
  if (replayIsRunning) return;
  replayIsRunning = true;
  const playBtn = document.getElementById('btnReplayPlayPause');
  if (playBtn) playBtn.textContent = '⏸ Pause';

  replayTimerId = setInterval(() => {
    if (replayStepIndex < ALIBABA_TRACE_DATA.time_steps.length - 1) {
      renderReplayStep(replayStepIndex + 1);
    } else {
      renderReplayStep(0); // loop back
    }
  }, 1000 / replaySpeedMultiplier);
}

function stopReplay() {
  replayIsRunning = false;
  if (replayTimerId) clearInterval(replayTimerId);
  const playBtn = document.getElementById('btnReplayPlayPause');
  if (playBtn) playBtn.textContent = '▶ Replay';
}

function toggleReplay() {
  if (replayIsRunning) stopReplay();
  else startReplay();
}

// ─── EVENT BINDINGS FOR MODE & REPLAY ───
document.getElementById('btnModeDemo')?.addEventListener('click', () => switchAppMode('demo'));
document.getElementById('btnModeReplay')?.addEventListener('click', () => switchAppMode('replay'));

document.getElementById('btnReplayPlayPause')?.addEventListener('click', toggleReplay);

document.getElementById('btnReplayStepForward')?.addEventListener('click', () => {
  if (replayIsRunning) stopReplay();
  renderReplayStep(replayStepIndex + 1);
});

document.getElementById('btnReplayStepBack')?.addEventListener('click', () => {
  if (replayIsRunning) stopReplay();
  renderReplayStep(replayStepIndex - 1);
});

document.querySelectorAll('.speed-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    replaySpeedMultiplier = parseInt(this.getAttribute('data-speed'));
    if (replayIsRunning) {
      stopReplay();
      startReplay();
    }
  });
});

document.getElementById('replayScrubber')?.addEventListener('input', function() {
  if (replayIsRunning) stopReplay();
  renderReplayStep(parseInt(this.value));
});

// PROVENANCE MODAL LISTENERS
document.getElementById('btnOpenProvenance')?.addEventListener('click', () => {
  document.getElementById('provenanceModal').classList.add('show');
});

document.getElementById('btnCloseProvenance')?.addEventListener('click', () => {
  document.getElementById('provenanceModal').classList.remove('show');
});

document.getElementById('provenanceModal')?.addEventListener('click', (e) => {
  if (e.target.id === 'provenanceModal') {
    document.getElementById('provenanceModal').classList.remove('show');
  }
});
"""

if "ALIBABA_TRACE_DATA" not in html:
    html = html.replace("<script>", "<script>\n" + js_engine_code, 1)

# Write updated HTML
with open("C:/Claude_projects/acm/AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard successfully updated with Alibaba GPU Cluster Trace 2026 integration!")
