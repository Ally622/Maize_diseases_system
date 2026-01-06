import streamlit as st

# ---------------------------
# Ontology
# ---------------------------
diseases = [
    "MLND", "Rust", "Blight", "Smut", "DownyMildew", "GrayLeafSpot", "Anthracnose",
    "RootRot", "EarRot", "CommonBunt", "StalkRot", "ViralStreak", "LeafCurl",
    "Wilt", "StripeDisease", "ChlorosisComplex", "MosaicVirus", "FusariumWilt",
    "AspergillusRot", "DiplodiaEarRot"
]

symptoms = [
    "Yellowing", "Necrosis", "LeafSpots", "StemBreakage", "EarDiscoloration",
    "WhiteFungalGrowth", "RustPustules", "MoldyKernels", "Wilting", "Curling",
    "Streaks", "SoftRot", "Blisters", "PowderyGrowth", "WaterSoaking",
    "DampingOff", "GrayLesions", "DeadTissue", "StuntedGrowth", "Browning"
]

conditions = [
    "HighHumidity", "LowHumidity", "ModerateHumidity", "HighTemp", "LowTemp",
    "WetSoils", "PoorDrainage", "Drought", "InsectVector", "DensePlanting",
    "PoorFertility", "LatePlanting", "EarlyPlanting", "ContaminatedSeed", "MechanicalInjury"
]

# ---------------------------
# Knowledge Base (Facts)
# ---------------------------
# Disease -> Symptoms
has_symptom = {
    "MLND": ["Yellowing", "Necrosis", "StuntedGrowth"],
    "Rust": ["RustPustules", "LeafSpots"],
    "Blight": ["LeafSpots", "DeadTissue"],
    "Smut": ["Blisters", "MoldyKernels"],
    "DownyMildew": ["WhiteFungalGrowth", "WaterSoaking"],
    "GrayLeafSpot": ["GrayLesions", "DeadTissue"],
    "Anthracnose": ["DeadTissue", "Browning"],
    "RootRot": ["SoftRot", "Browning"],
    "EarRot": ["MoldyKernels", "EarDiscoloration"],
    "StalkRot": ["StemBreakage"],
    "ViralStreak": ["Streaks"],
    "LeafCurl": ["Curling"],
    "Wilt": ["Wilting"],
    "StripeDisease": ["Streaks"],
    "ChlorosisComplex": ["Yellowing"],
    "MosaicVirus": ["Yellowing"],
    "FusariumWilt": ["Wilting"],
    "AspergillusRot": ["MoldyKernels"],
    "DiplodiaEarRot": ["MoldyKernels", "EarDiscoloration"]
}

# Disease -> Conditions (triggers)
triggered_by = {
    "MLND": ["InsectVector", "LatePlanting", "DensePlanting"],
    "Rust": ["HighHumidity", "ModerateHumidity"],
    "Blight": ["HighHumidity"],
    "DownyMildew": ["HighHumidity", "WetSoils"],
    "GrayLeafSpot": ["HighTemp"],
    "Smut": ["ContaminatedSeed"],
    "RootRot": ["PoorDrainage", "WetSoils"],
    "EarRot": ["HighHumidity", "MechanicalInjury"],
    "Wilt": ["Drought"],
    "LeafCurl": ["InsectVector"],
    "MosaicVirus": ["InsectVector"],
    "FusariumWilt": ["WetSoils"],
    "StalkRot": ["HighTemp"],
    "Anthracnose": ["HighHumidity"],
    "AspergillusRot": ["HighTemp"],
    "DiplodiaEarRot": ["HighHumidity", "MechanicalInjury"]
}

# Co-occurrence rules
co_occurs = [
    ("Rust", "GrayLeafSpot"),
    ("EarRot", "AspergillusRot"),
    ("Smut", "EarRot"),
    ("DownyMildew", "Blight"),
    ("RootRot", "FusariumWilt"),
    ("MLND", "MosaicVirus"),
    ("Anthracnose", "GrayLeafSpot"),
    ("StalkRot", "RootRot"),
    ("DiplodiaEarRot", "AspergillusRot"),
    ("Blight", "Rust")
]

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🌽 Maize Disease Expert System")

st.write("Select observed symptoms and environmental conditions:")

selected_symptoms = st.multiselect("Symptoms:", symptoms)
selected_conditions = st.multiselect("Conditions:", conditions)

if st.button("Diagnose Disease"):
    scores = {d: 0 for d in diseases}

    # Match symptoms
    for disease, dsymptoms in has_symptom.items():
        scores[disease] += sum([1 for s in selected_symptoms if s in dsymptoms])

    # Match conditions
    for disease, dconditions in triggered_by.items():
        scores[disease] += sum([1 for c in selected_conditions if c in dconditions])

    # Co-occurrence boost
    for d1, d2 in co_occurs:
        if d1 in scores and d2 in scores:
            if scores[d1] > 0 and scores[d2] > 0:
                scores[d1] += 1
                scores[d2] += 1

    # Recommend disease
    max_score = max(scores.values())
    if max_score == 0:
        st.info("No disease could be determined from selected symptoms/conditions.")
    else:
        probable = [d for d, score in scores.items() if score == max_score]
        st.success(f"Probable disease(s): {', '.join(probable)}")
