import streamlit as st
import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="💧 Water Potability Predictor",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Base API URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


# ----------------- Utility Functions -----------------
def check_api_health() -> bool:
    """Check if the FastAPI backend is healthy."""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False


def predict_potability(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Send input data to the API for prediction."""
    try:
        response = requests.post(f"{API_BASE_URL}/predict", json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


# ----------------- UI Layout -----------------
def main():
    # Title and Description
    st.title("💧 Water Potability Prediction App")
    st.markdown("Use this app to check if a given water sample is potable or not based on its chemical properties.")
    st.markdown("---")

    # Sidebar for API health & info
    with st.sidebar:
        st.header("🔌 API Status")
        if check_api_health():
            st.success("✅ API is Healthy and Reachable")
        else:
            st.error("❌ API not responding")
            st.info("Make sure your FastAPI backend is running.")

        st.markdown("---")
        st.header("ℹ️ About This App")
        st.info("""
        This app uses a trained Random Forest model to predict whether 
        water is **potable (safe to drink)** or **not potable** based 
        on physical and chemical parameters.
        """)

    # Input form for sample parameters
    st.subheader("📋 Enter Water Sample Parameters")

    with st.form("water_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            ph = st.number_input("pH", value=7.0, format="%.2f")
            Hardness = st.number_input("Hardness", value=150.0, format="%.2f")
            Solids = st.number_input("Solids", value=20000.0, format="%.2f")

        with col2:
            Chloramines = st.number_input("Chloramines", value=7.0, format="%.2f")
            Sulfate = st.number_input("Sulfate", value=300.0, format="%.2f")
            Conductivity = st.number_input("Conductivity", value=400.0, format="%.2f")

        with col3:
            Organic_carbon = st.number_input("Organic Carbon", value=10.0, format="%.2f")
            Trihalomethanes = st.number_input("Trihalomethanes", value=60.0, format="%.2f")
            Turbidity = st.number_input("Turbidity", value=4.0, format="%.2f")

        submitted = st.form_submit_button("🔮 Predict Potability")

    if submitted:
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

        with st.spinner("⏳ Sending data to model..."):
            result = predict_potability(payload)

        if result:
            st.markdown("---")
            st.subheader("🔍 Prediction Result")

            pred = result.get("prediction", None)
            if pred == 1:
                st.success("✅ The model predicts this water is **Potable (Safe to Drink)** 💧")
            elif pred == 0:
                st.warning("🚫 The model predicts this water is **Not Potable (Unsafe to Drink)** ⚠️")
            else:
                st.error("Unexpected response from API.")

            st.markdown("### 🧾 Raw API Response")
            st.json(result)


if __name__ == "__main__":
    main()