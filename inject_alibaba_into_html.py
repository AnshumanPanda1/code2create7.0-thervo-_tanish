import json
import re

# Read generated dataset
with open("C:/Claude_projects/acm/alibaba_gpu_trace_2026.json", "r", encoding="utf-8") as f:
    alibaba_data = json.load(f)

# Read current HTML dashboard
with open("C:/Claude_projects/acm/AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Verify dataset loaded correctly
print(f"Loaded dataset with {len(alibaba_data['time_steps'])} time steps.")

# Prepare inline Javascript snippet
js_data_snippet = f"const ALIBABA_TRACE_DATA = {json.dumps(alibaba_data)};\n"

print("JS data snippet ready. Size:", len(js_data_snippet), "bytes.")
