from importlib import reload
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import pickle
import logging

# -------------------------------
# Logging setup
# -------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# Initialize FastAPI app
# -------------------------------
app = FastAPI(
    title="Water Potability Prediction API",
    version="1.0",
    description="An API that predicts whether water is potable (safe for drinking) based on quality parameters."
)

# -------------------------------
# Enable CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Pydantic models
# -------------------------------
class Water(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float

class PredictionResponse(BaseModel):
    prediction: int
    result: str

# -------------------------------
# Model loading
# -------------------------------
model = None
model_info = {}

def load_model():
    global model, model_info
    try:
<<<<<<< HEAD
        model_path = Path("rf_model.pkl")
=======
        # Base directory of this file (src/backend/)
        base_dir = Path(__file__).resolve().parent

        # Go two levels up to reach project root -> models/rf_model.pkl
        model_path = base_dir.parent.parent / "models" / "rf_model.pkl"

        # Log the resolved path for debugging
        logger.info(f"Looking for model at: {model_path}")
>>>>>>> 7fb0573292fc99580be0c68f8b490d32727221b4

        if not model_path.exists():
            raise FileNotFoundError(f"Model file '{model_path}' not found.")

        with open(model_path, "rb") as model_file:
            model = pickle.load(model_file)

        model_info = {
            "model_path": str(model_path),
            "model_type": "Random Forest Classifier",
            "target": "Water Potability"
        }

        logger.info(f"✅ Model loaded successfully from {model_path}")
        return True

    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")
        return False

# -------------------------------
# Startup event
# -------------------------------
@app.on_event("startup")
async def startup_event():
    success = load_model()
    if not success:
        logger.error("Failed to load model on startup.")
    else:
        logger.info("Model loaded and ready for predictions.")

# -------------------------------
# API routes
# -------------------------------
@app.get("/")
async def root():
    return {
        "message": "🚰 Water Potability Prediction API is running.",
        "model_info": model_info,
        "model_loaded": model is not None
    }

@app.get("/health")
async def health_check():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse)
async def predict_potability(water: Water):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Prepare input data as a DataFrame
        sample = pd.DataFrame([{
            'ph': water.ph,
            'Hardness': water.Hardness,
            'Solids': water.Solids,
            'Chloramines': water.Chloramines,
            'Sulfate': water.Sulfate,
            'Conductivity': water.Conductivity,
            'Organic_carbon': water.Organic_carbon,
            'Trihalomethanes': water.Trihalomethanes,
            'Turbidity': water.Turbidity
        }])

        # Make prediction
        prediction = model.predict(sample)[0]
        result = "Water is Consumable" if prediction == 1 else "Water is Not Consumable"

        return PredictionResponse(
            prediction=int(prediction),
            result=result
        )

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# -------------------------------
# Run with Uvicorn
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
