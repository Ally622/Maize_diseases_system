import mysql.connector

# -----------------------------
# 1️⃣ Connect to MariaDB
# -----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",   # put your password here if you set one
    database="maize_diseases"
)

cursor = conn.cursor()

# -----------------------------
# 2️⃣ Ask user for symptoms
# -----------------------------
symptoms_input = input("Enter observed symptoms (comma-separated): ")
symptoms = [s.strip() for s in symptoms_input.split(',')]

# -----------------------------
# 3️⃣ Ask user for conditions (optional)
# -----------------------------
conditions_input = input("Enter current conditions (comma-separated, or leave blank): ")
conditions = [c.strip() for c in conditions_input.split(',')] if conditions_input else []

# -----------------------------
# 4️⃣ Initialize disease scoring
# -----------------------------
disease_scores = {}

# -----------------------------
# 5️⃣ Score diseases based on symptoms
# -----------------------------
for symptom in symptoms:
    # Diseases indicated by symptom
    cursor.execute("""
        SELECT DISTINCT disease
        FROM indicates
        WHERE symptom = %s
    """, (symptom,))
    for (disease,) in cursor.fetchall():
        disease_scores[disease] = disease_scores.get(disease, 0) + 2  # symptom match = +2

    # Diseases that have this symptom directly
    cursor.execute("""
        SELECT DISTINCT disease
        FROM has_symptom
        WHERE symptom = %s
    """, (symptom,))
    for (disease,) in cursor.fetchall():
        disease_scores[disease] = disease_scores.get(disease, 0) + 1  # direct symptom = +1

# -----------------------------
# 6️⃣ Score diseases based on conditions
# -----------------------------
for condition in conditions:
    # Triggered by condition
    cursor.execute("""
        SELECT DISTINCT disease
        FROM triggered_by
        WHERE condition_name = %s
    """, (condition,))
    for (disease,) in cursor.fetchall():
        disease_scores[disease] = disease_scores.get(disease, 0) + 2  # triggered condition = +2

    # Risk factor
    cursor.execute("""
        SELECT DISTINCT disease
        FROM risk_factor
        WHERE condition_name = %s
    """, (condition,))
    for (disease,) in cursor.fetchall():
        disease_scores[disease] = disease_scores.get(disease, 0) + 1  # risk factor = +1

# -----------------------------
# 7️⃣ Include severity rules
# -----------------------------
for condition in conditions:
    cursor.execute("""
        SELECT DISTINCT disease
        FROM severe_under
        WHERE condition_name = %s
    """, (condition,))
    for (disease,) in cursor.fetchall():
        disease_scores[disease] = disease_scores.get(disease, 0) + 3  # severe = +3

# -----------------------------
# 8️⃣ Include co-occurring diseases
# -----------------------------
current_diseases = list(disease_scores.keys())
for disease in current_diseases:
    cursor.execute("""
        SELECT disease2
        FROM co_occurs
        WHERE disease1 = %s
    """, (disease,))
    for (co_disease,) in cursor.fetchall():
        disease_scores[co_disease] = disease_scores.get(co_disease, 0) + 1  # co-occurs = +1

# -----------------------------
# 9️⃣ Print ranked possible diseases
# -----------------------------
if disease_scores:
    print("\nPossible diseases ranked by likelihood:")
    for disease, score in sorted(disease_scores.items(), key=lambda x: x[1], reverse=True):
        print(f"- {disease} (score: {score})")
else:
    print("\nNo diseases found for the given symptoms and conditions.")

# -----------------------------
# 🔟 Close connection
# -----------------------------
cursor.close()
conn.close()

