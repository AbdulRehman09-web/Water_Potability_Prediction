import streamlit as st
import requests

st.set_page_config(page_title="Water Potability Demo", layout="centered")

st.title("Water Potability Predictor")

st.markdown("Fill in the water sample features and click Predict.")

# Input fields (match the backend Features model)
ph = st.number_input("pH", value=7.0, format="%.3f")
Hardness = st.number_input("Hardness", value=100.0, format="%.3f")
Solids = st.number_input("Solids", value=20000.0, format="%.3f")
Chloramines = st.number_input("Chloramines", value=3.0, format="%.3f")
Sulfate = st.number_input("Sulfate", value=300.0, format="%.3f")
Conductivity = st.number_input("Conductivity", value=400.0, format="%.3f")
Organic_carbon = st.number_input("Organic_carbon", value=5.0, format="%.3f")
Trihalomethanes = st.number_input("Trihalomethanes", value=3.0, format="%.3f")
Turbidity = st.number_input("Turbidity", value=1.0, format="%.3f")

col1, col2 = st.columns(2)

backend_url = st.text_input("Backend URL", value="http://backend:8000")  # In docker-compose network use service name 'backend'

if st.button("Predict"):
    payload = {
        "ph": ph,
        "Hardness": Hardness,
        "Solids": Solids,
        "Chloramines": Chloramines,
        "Sulfate": Sulfate,
        "Conductivity": Conductivity,
        "Organic_carbon": Organic_carbon,
        "Trihalomethanes": Trihalomethanes,
        "Turbidity": Turbidity
    }
    try:
        r = requests.post(f"{backend_url}/predict", json=payload, timeout=10)
        r.raise_for_status()
        pred = r.json().get("prediction")
        if pred == 1:
            st.success("Model predicts: Potable (1)")
        else:
            st.info("Model predicts: Not Potable (0)")
        st.json(r.json())
    except Exception as e:
        st.error(f"Request failed: {e}")
