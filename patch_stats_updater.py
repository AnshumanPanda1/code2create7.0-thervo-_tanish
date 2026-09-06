with open("C:/Claude_projects/acm/AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html", "r", encoding="utf-8") as f:
    html = f.read()

# Enhance updateModelStats to sync strip indicators
old_update_stats = "function updateModelStats() {"
new_update_stats = """function updateModelStats() {
  const hotCount = racks.filter(r => r.riskScore > 0.55).length;
  const coolCount = racks.filter(r => r.coolingActive || r.overrideEnabled).length;
  const stripHZ = document.getElementById('stripHotZones');
  const stripCA = document.getElementById('stripCoolingActive');
  if (stripHZ) stripHZ.textContent = `${hotCount} rack${hotCount !== 1 ? 's' : ''}`;
  if (stripCA) stripCA.textContent = `${coolCount} active`;
"""

if "const stripHZ = document.getElementById('stripHotZones');" not in html:
    html = html.replace(old_update_stats, new_update_stats, 1)

with open("C:/Claude_projects/acm/AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Status strip updater patched successfully.")
