#!/bin/bash


echo "🚰 Water Potability Prediction Frontend"

echo "🤩 Starting Streamlit server"
streamlit run Water_Prediction.py --server.address "${STREAMLIT_SERVER_ADDRESS:-0.0.0.0}" --server.port "${STREAMLIT_SERVER_PORT:-8501}"