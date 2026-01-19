import streamlit as st

st.set_page_config(page_title="Maize Disease Diagnosis", page_icon="🌽", layout="wide")

st.title("🌽 Maize Disease Diagnosis Tool")
st.markdown("""
Welcome! Enter the observed symptoms and current conditions of your maize crop. 
The tool will predict possible diseases and rank them by likelihood.
""")
import mysql.connector

# -----------------------------
# 1️⃣ Connect to MariaDB
# -----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # put your MariaDB root password here
    database="maize_diseases"
)
cursor = conn.cursor()

# -----------------------------
# 2️⃣ Streamlit UI
# -----------------------------
st.title("🌽 Maize Disease Diagnosis Tool")

st.write("Enter observed symptoms and current conditions:")

# Input: symptoms
symptoms_input = st.text_input("Symptoms (comma-separated)", "LeafSpots, RustPustules")
symptoms = [s.strip().title() for s in symptoms_input.split(',')]

# Input: conditions
conditions_input = st.text_input("Conditions (comma-separated, optional)", "HighHumidity")
conditions = [c.strip().title() for c in conditions_input.split(',')] if conditions_input else []

# Button: Diagnose
if st.button("Diagnose"):

    # -----------------------------
    # 3️⃣ Initialize disease scoring
    # -----------------------------
    disease_scores = {}

    # Score based on symptoms
    for symptom in symptoms:
        cursor.execute("SELECT DISTINCT disease FROM indicates WHERE symptom = %s", (symptom,))
        for (disease,) in cursor.fetchall():
            disease_scores[disease] = disease_scores.get(disease, 0) + 2

        cursor.execute("SELECT DISTINCT disease FROM has_symptom WHERE symptom = %s", (symptom,))
        for (disease,) in cursor.fetchall():
            disease_scores[disease] = disease_scores.get(disease, 0) + 1

    # Score based on conditions
    for condition in conditions:
        cursor.execute("SELECT DISTINCT disease FROM triggered_by WHERE condition_name = %s", (condition,))
        for (disease,) in cursor.fetchall():
            disease_scores[disease] = disease_scores.get(disease, 0) + 2

        cursor.execute("SELECT DISTINCT disease FROM risk_factor WHERE condition_name = %s", (condition,))
        for (disease,) in cursor.fetchall():
            disease_scores[disease] = disease_scores.get(disease, 0) + 1

    # Severity rules
    for condition in conditions:
        cursor.execute("SELECT DISTINCT disease FROM severe_under WHERE condition_name = %s", (condition,))
        for (disease,) in cursor.fetchall():
            disease_scores[disease] = disease_scores.get(disease, 0) + 3

    # Co-occurring diseases
    current_diseases = list(disease_scores.keys())
    for disease in current_diseases:
        cursor.execute("SELECT disease2 FROM co_occurs WHERE disease1 = %s", (disease,))
        for (co_disease,) in cursor.fetchall():
            disease_scores[co_disease] = disease_scores.get(co_disease, 0) + 1

    # -----------------------------
    # 4️⃣ Display results
    # -----------------------------
    if disease_scores:
        st.subheader("Possible diseases ranked by likelihood:")
        for disease, score in sorted(disease_scores.items(), key=lambda x: x[1], reverse=True):
            st.write(f"- {disease} (score: {score})")
    else:
        st.write("No diseases found for the given symptoms and conditions.")

# -----------------------------
# 5️⃣ Close connection
# -----------------------------
cursor.close()
conn.close()
