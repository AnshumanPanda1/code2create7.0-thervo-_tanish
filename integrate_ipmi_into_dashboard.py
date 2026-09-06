import json

# Read datasets
with open("C:/Claude_projects/acm/ipmi_hardware_trace_2020.json", "r", encoding="utf-8") as f:
    ipmi_data = json.load(f)

with open("C:/Claude_projects/acm/AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Mode Switcher HTML to 3 Modes
old_mode_switcher = """    <!-- DUAL MODE SWITCHER -->
    <div class="mode-toggle-group">
      <button class="mode-btn active" id="btnModeDemo">⚡ DEMO MODE</button>
      <button class="mode-btn" id="btnModeReplay">● PRODUCTION TRACE REPLAY</button>
    </div>"""

new_mode_switcher = """    <!-- 3-MODE ARCHITECTURE SWITCHER -->
    <div class="mode-toggle-group">
      <button class="mode-btn active" id="btnModeDemo">⚡ DEMO MODE</button>
      <button class="mode-btn" id="btnModeReplay">● ALIBABA GPU TRACE</button>
      <button class="mode-btn" id="btnModeIpmi">🔬 IPMI PHYSICAL SENSORS</button>
    </div>"""

if "btnModeIpmi" not in html:
    html = html.replace(old_mode_switcher, new_mode_switcher)

# 2. Update Provenance Modal Content to include IPMI dataset details
old_modal_content = """      <div style="background:var(--brand-light); border:1px solid #bfdbfe; border-radius:6px; padding:12px; display:flex; flex-direction:column; gap:6px;">
        <span class="mono" style="font-size:11px; font-weight:700; color:var(--brand-primary);">DATA SOURCE: ALIBABA CLUSTER TRACE GPU V2026</span>
        <span style="font-size:11px; color:var(--text-secondary);">Official anonymized 6-month production trace covering 155,410 GPUs across 37,707 GPU servers. Hosted by Alibaba Group.</span>
      </div>"""

new_modal_content = """      <div style="display:flex; flex-direction:column; gap:8px;">
        <div style="background:var(--brand-light); border:1px solid #bfdbfe; border-radius:6px; padding:10px; display:flex; flex-direction:column; gap:4px;">
          <span class="mono" style="font-size:11px; font-weight:700; color:var(--brand-primary);">1. PRODUCTION TRACE: ALIBABA CLUSTER TRACE GPU V2026</span>
          <span style="font-size:11px; color:var(--text-secondary);">Anonymized 6-month production AI trace covering 155,410 GPUs across 37,707 servers. Provides software workload, utilization, and ASW topology.</span>
        </div>
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:6px; padding:10px; display:flex; flex-direction:column; gap:4px;">
          <span class="mono" style="font-size:11px; font-weight:700; color:#166534;">2. GROUND-TRUTH SENSOR VALIDATION: SC20 HPC IPMI DATASET (20-03.tar / 20-04.tar)</span>
          <span style="font-size:11px; color:#15803d;">High-density 20-second physical sensor trace covering 104 hardware metrics (NVIDIA V100 GPU Core/Mem Temp °C, CPU Core Temp °C, DIMM Temp °C, PSU Power W, Fan RPM) across ~1,000 HPC servers.</span>
        </div>
      </div>"""

if "SC20 HPC IPMI DATASET" not in html:
    html = html.replace(old_modal_content, new_modal_content)

# 3. Inject IPMI dataset JS & Replay Logic
js_ipmi_code = """
// ─── IPMI HARDWARE PHYSICAL SENSOR DATASET (INLINE BUNDLE) ───
const IPMI_TRACE_DATA = """ + json.dumps(ipmi_data) + """;

// Add IPMI mode switch listener
document.getElementById('btnModeIpmi')?.addEventListener('click', () => switchAppMode('ipmi'));

// Enhance switchAppMode function to handle 'ipmi'
const originalSwitchAppMode = switchAppMode;
switchAppMode = function(mode) {
  const btnIpmi = document.getElementById('btnModeIpmi');
  const btnDemo = document.getElementById('btnModeDemo');
  const btnReplay = document.getElementById('btnModeReplay');
  const demoControls = document.getElementById('demoControlsGroup');
  const replayControls = document.getElementById('replayControlsGroup');
  const demoSliders = document.getElementById('demoSlidersGroup');
  const replayScrubber = document.getElementById('replayScrubberGroup');
  const statusText = document.getElementById('statusText');

  if (mode === 'ipmi') {
    currentAppMode = 'ipmi';
    if (simRunning) { simRunning = false; clearInterval(simInterval); }
    if (replayIsRunning) stopReplay();

    btnDemo.classList.remove('active');
    btnReplay.classList.remove('active');
    if (btnIpmi) btnIpmi.classList.add('active');

    demoControls.style.display = 'none';
    replayControls.style.display = 'flex';
    demoSliders.style.display = 'none';
    replayScrubber.style.display = 'flex';

    if (statusText) statusText.textContent = 'IPMI GROUND-TRUTH VALIDATION';
    addLog('🔬 Switched to GROUND-TRUTH PHYSICAL SENSOR MODE (SC20 HPC IPMI Trace 20-03/20-04)', 'info', 0);
    renderReplayStep(replayStepIndex);
  } else {
    if (btnIpmi) btnIpmi.classList.remove('active');
    originalSwitchAppMode(mode);
  }
};

// Modify renderReplayStep to format IPMI physical readings when in 'ipmi' mode
const originalRenderReplayStep = renderReplayStep;
renderReplayStep = function(stepIdx) {
  if (currentAppMode === 'ipmi') {
    if (!IPMI_TRACE_DATA || !IPMI_TRACE_DATA.time_steps) return;
    if (stepIdx < 0) stepIdx = 0;
    if (stepIdx >= IPMI_TRACE_DATA.time_steps.length) stepIdx = IPMI_TRACE_DATA.time_steps.length - 1;

    replayStepIndex = stepIdx;
    const stepObj = IPMI_TRACE_DATA.time_steps[stepIdx];

    const timeTextEl = document.getElementById('replayTimeText');
    if (timeTextEl) timeTextEl.textContent = stepObj.formatted_time;

    const scrubberEl = document.getElementById('replayScrubber');
    if (scrubberEl) scrubberEl.value = stepIdx;

    const stepTextEl = document.getElementById('scrubberStepText');
    if (stepTextEl) stepTextEl.textContent = `20s Step ${stepIdx + 1}/${IPMI_TRACE_DATA.time_steps.length}`;

    const serverRecords = stepObj.servers;

    const rawFeatures = racks.map((rack, i) => {
      const sData = serverRecords[i % serverRecords.length];

      rack.cpu = sData.derived_cpu_util;
      rack.gpu = sData.derived_gpu_util;
      rack.memory = minMax(30, 85, sData.dimm_temp_c * 2.0);
      rack.diskIO = minMax(20, 90, sData.total_power_w / 8.0);
      rack.network = minMax(15, 80, sData.cpu_power_w * 0.5);
      rack.workload_type = "HPC_PHYSICAL_BENCHMARK";
      rack.gpu_type = "NVIDIA V100-SXM2-32GB";
      rack.asw_id = sData.physical_rack;
      rack.ipmi_gpu_temp = sData.gpu_core_temp_c;
      rack.ipmi_cpu_temp = sData.cpu_core_temp_c;
      rack.ipmi_power_w = sData.total_power_w;

      return { cpu: rack.cpu, gpu: rack.gpu, memory: rack.memory, diskIO: rack.diskIO, network: rack.network };
    });

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

    renderFloorPlan();
    updateRackCards();
    updateHeatmap();
    updateGNNGraph();
    updateSelectedDetail();
    updateFeatureImportance(rawFeatures);
    updateModelStats();
    if (selectedRack >= 0) drawHistoryChart();

    if (stepIdx % 5 === 0) {
      const targetR = racks[selectedRack] || racks[0];
      addLog(`🔬 [IPMI GROUND-TRUTH] ${targetR.name} V100 GPU: ${targetR.ipmi_gpu_temp}°C | CPU Core: ${targetR.ipmi_cpu_temp}°C | Power: ${targetR.ipmi_power_w}W | Pred Risk: ${(targetR.riskScore*100).toFixed(1)}%`, 'info', targetR.id);
    }
  } else {
    originalRenderReplayStep(stepIdx);
  }
};

function minMax(min, max, val) {
  return Math.min(max, Math.max(min, val));
}
"""

if "IPMI_TRACE_DATA" not in html:
    html = html.replace("// ─── DUAL MODE & REPLAY STATE MACHINE ───", js_ipmi_code + "\n// ─── DUAL MODE & REPLAY STATE MACHINE ───")

with open("C:/Claude_projects/acm/AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard successfully updated with 3-Mode Architecture & IPMI dataset integration!")
