import streamlit as st
import mysql.connector
import pandas as pd

# -----------------------------
# 1️ Page setup
# -----------------------------
st.set_page_config(page_title="Maize Disease Diagnosis", page_icon="🌽", layout="wide")
st.title("🌽 Maize Disease Diagnosis Tool")
st.markdown("""
Welcome! Select the symptoms observed and current conditions of your maize crop.
The tool will predict possible diseases and rank them by likelihood.
""")

# -----------------------------
# 2️ Connect to MariaDB
# -----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # put your password here
    database="maize_diseases"
)
cursor = conn.cursor()

# -----------------------------
# 3️ Fetch all symptoms and conditions from DB
# -----------------------------
cursor.execute("SELECT DISTINCT symptom FROM has_symptom")
all_symptoms = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT DISTINCT condition_name FROM triggered_by")
all_conditions = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT DISTINCT disease FROM has_symptom")
all_diseases = [row[0] for row in cursor.fetchall()]

# -----------------------------
# 4️ Sidebar selection
# -----------------------------
st.sidebar.header("Select Input Options")

symptoms = st.sidebar.multiselect("Observed Symptoms:", all_symptoms)
conditions = st.sidebar.multiselect("Current Conditions:", all_conditions)

st.sidebar.markdown("---")
st.sidebar.header("Optional Analysis")
show_analysis = st.sidebar.checkbox("Show Disease Statistics")

# -----------------------------
# 5️ Disease scoring function
# -----------------------------
def diagnose(symptoms, conditions):
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

    return disease_scores

# -----------------------------
# 6️ Diagnose button
# -----------------------------
if st.button("Diagnose"):
    if not symptoms and not conditions:
        st.warning("Please select at least one symptom or condition.")
    else:
        scores = diagnose(symptoms, conditions)

        if scores:
            df = pd.DataFrame(
                sorted(scores.items(), key=lambda x: x[1], reverse=True),
                columns=["Disease", "Score"]
            )

            st.subheader("📊 Possible Diseases Ranked by Likelihood")
            st.bar_chart(df.set_index("Disease"))
            st.table(df)

            # -----------------------------
            # 7️ Prevention tips
            # -----------------------------
            prevention_tips = {
                "Rust": "Use resistant varieties, apply fungicides.",
                "MLND": "Use clean seed, control insect vectors.",
                "Blight": "Avoid dense planting, fungicide application.",
                "EarRot": "Ensure good storage and drying.",
                "Anthracnose": "Control humidity and remove infected debris.",
                "DiplodiaEarRot": "Rotate crops and ensure good drying.",
                "DownyMildew": "Improve drainage and reduce humidity.",
                "GrayLeafSpot": "Avoid wet foliage, rotate crops.",
                "AspergillusRot": "Good storage and hygiene.",
                "MosaicVirus": "Control insect vectors.",
                "FusariumWilt": "Use resistant varieties and rotate crops.",
                "StalkRot": "Avoid dense planting and high humidity.",
                "LeafCurl": "Control insect vectors."
            }

            st.subheader("🌿 Suggested Prevention/Control Measures")
            for disease, _ in df.head(5).values:  # show top 5
                tip = prevention_tips.get(disease, "No tips available.")
                st.write(f"- **{disease}**: {tip}")
        else:
            st.write("No diseases found for the selected symptoms and conditions.")

# -----------------------------
# 8️ Optional analysis tab
# -----------------------------
if show_analysis:
    st.subheader("📈 Disease Occurrence Statistics")
    cursor.execute("SELECT disease, COUNT(*) FROM has_symptom GROUP BY disease ORDER BY COUNT(*) DESC")
    analysis_data = cursor.fetchall()
    if analysis_data:
        df_analysis = pd.DataFrame(analysis_data, columns=["Disease", "Number of Symptoms"])
        st.bar_chart(df_analysis.set_index("Disease"))
        st.table(df_analysis)
    else:
        st.write("No data available for analysis.")

# -----------------------------
# 9️ Close DB connection
# -----------------------------
cursor.close()
conn.close()

