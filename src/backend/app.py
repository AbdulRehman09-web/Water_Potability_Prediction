from importlib import reload
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import pickle
import logging

# ==============================================================
# Logging Setup
# ==============================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================================================
# FastAPI Initialization
# ==============================================================
app = FastAPI(
    title="Water Potability Prediction API",
    version="1.0",
    description=(
        "An API that predicts whether water is potable "
        "(safe for drinking) based on quality parameters."
    ),
)

# ==============================================================
# Enable CORS
# ==============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================
# Pydantic Models
# ==============================================================
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


# ==============================================================
# Model Loading
# ==============================================================
model = None
model_info = {}


def load_model() -> bool:
    """Load the trained model from a pickle file."""
    global model, model_info

    try:
        model_path = Path("rf_model.pkl")

        if not model_path.exists():
            raise FileNotFoundError(f"Model file '{model_path}' not found.")

        with open(model_path, "rb") as file:
            model = pickle.load(file)

        model_info = {
            "model_path": str(model_path),
            "model_type": "Random Forest Classifier",
            "target": "Water Potability",
        }

        logger.info(f"✅ Model loaded successfully from {model_path}")
        return True

    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")
        return False


# ==============================================================
# Startup Event
# ==============================================================
@app.on_event("startup")
async def startup_event():
    """Load model when the server starts."""
    success = load_model()
    if not success:
        logger.error("Failed to load model on startup.")
    else:
        logger.info("Model loaded and ready for predictions.")


# ==============================================================
# API Routes
# ==============================================================
@app.get("/")
async def root():
    """Root endpoint with model info."""
    return {
        "message": "🚰 Water Potability Prediction API is running.",
        "model_info": model_info,
        "model_loaded": model is not None,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}


@app.post("/predict", response_model=PredictionResponse)
async def predict_potability(water: Water):
    """Predict whether water is potable or not."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Prepare input data
        sample = pd.DataFrame([{
            "ph": water.ph,
            "Hardness": water.Hardness,
            "Solids": water.Solids,
            "Chloramines": water.Chloramines,
            "Sulfate": water.Sulfate,
            "Conductivity": water.Conductivity,
            "Organic_carbon": water.Organic_carbon,
            "Trihalomethanes": water.Trihalomethanes,
            "Turbidity": water.Turbidity,
        }])

        # Make prediction
        prediction = model.predict(sample)[0]
        result = "Water is Consumable" if prediction == 1 else "Water is Not Consumable"

        return PredictionResponse(prediction=int(prediction), result=result)

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


# ==============================================================
# Run the Application
# ==============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
