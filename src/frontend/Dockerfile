FROM python:3.11-slim

WORKDIR /app

COPY src/frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Correct path relative to build context
COPY src/frontend/Water_Prediction.py .

EXPOSE 8501

CMD ["streamlit", "run", "Water_Prediction.py", "--server.port=8501", "--server.address=0.0.0.0"]
