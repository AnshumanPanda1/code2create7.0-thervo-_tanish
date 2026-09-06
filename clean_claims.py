with open("C:/Claude_projects/acm/AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace any fake accuracy text
html = html.replace("98.7% Accuracy", "DEMO MODEL (MAE 0.024)")
html = html.replace("98.7%", "DEMO MODEL")
html = html.replace("MODEL ACCURACY", "MODEL STATUS")
html = html.replace("98.7", "0.024")

# Update energy labels to specify estimated cooling optimization
html = html.replace("ENERGY OPTIMIZATION", "ESTIMATED COOLING OPTIMIZATION")
html = html.replace("REAL-TIME SAVINGS", "SIMULATED COOLING SAVINGS")

with open("C:/Claude_projects/acm/AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Claims cleaned up successfully.")
