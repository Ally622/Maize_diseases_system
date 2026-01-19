import re
import csv

# Patterns to extract facts from the Coq file
patterns = {
    "has_symptom": r"Constructor\s+\w+\s+:\s+has_symptom\s+(\w+)\s+(\w+)\.",
    "indicates": r"Constructor\s+\w+\s+:\s+indicates\s+(\w+)\s+(\w+)\.",
    "triggered_by": r"Constructor\s+\w+\s+:\s+triggered_by\s+(\w+)\s+(\w+)\.",
    "risk_factor": r"Constructor\s+\w+\s+:\s+risk_factor\s+(\w+)\s+(\w+)\.",
    "co_occurs": r"Constructor\s+\w+\s+:\s+co_occurs\s+(\w+)\s+(\w+)\.",
    "severe_under": r"Constructor\s+\w+\s+:\s+severe_under\s+(\w+)\s+(\w+)\."
}

data = {key: [] for key in patterns}

# Read the Coq file
with open("maize.v", "r", encoding="utf-8") as f:
    text = f.read()

# Extract matches
for key, pattern in patterns.items():
    matches = re.findall(pattern, text)
    data[key].extend(matches)

# Write CSV files
for key, rows in data.items():
    with open(f"{key}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if key == "indicates":
            writer.writerow(["symptom", "disease"])
        elif key == "co_occurs":
            writer.writerow(["disease1", "disease2"])
        else:
            writer.writerow(["disease", "symptom_or_condition"])

        writer.writerows(rows)

print("✅ CSV files created successfully!")
