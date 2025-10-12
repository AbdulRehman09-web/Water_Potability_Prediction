from fastapi import FastAPI
import pickle
import pandas as pd
from data_model import Water

# Initialize FastAPI app
app = FastAPI(
    title="Water Potability Prediction API",
    description="An API that predicts whether water is potable (safe for drinking) based on water quality parameters.",
    version="1.0"
)

# Load the trained Random Forest model
with open(r"C:\Users\HP\Documents\Data Science (Atomcamp)\Python\Mlops_Project\rf_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

@app.get("/")
def index():
    return {"message": "Welcome to the Water Potability Prediction API! Use the /predict endpoint to check water safety."}

@app.post("/predict")
def predict_potability(water: Water):
    """
    Predict whether the given water sample is potable (1) or not (0).
    """

    try:
        # Convert input data into a DataFrame
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

        # Interpret result
        result = "Water is Consumable" if prediction == 1 else "Water is Not Consumable"

        return {
            "prediction": int(prediction),
            "result": result
        }

    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}
