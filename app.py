from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle

# Initialize FastAPI app
app = FastAPI(
    title="Crop Yield Prediction API",
    description="Predict crop yield (hg/ha) using ML model",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model (pipeline)
with open("crop_yield_model.pkl", "rb") as f:
    model = pickle.load(f)

# Input schema
class CropYieldInput(BaseModel):
    Year: int
    average_rain_fall_mm_per_year: float
    pesticides_tonnes: float
    avg_temp: float
    Area: str
    Item: str

# Root endpoint (health check)
@app.get("/")
def home():
    return {"message": "Crop Yield Prediction API is running"}

# Prediction endpoint
@app.post("/predict")
def predict_yield(data: CropYieldInput):

    input_df = pd.DataFrame([{
        "Year": data.Year,
        "average_rain_fall_mm_per_year": data.average_rain_fall_mm_per_year,
        "pesticides_tonnes": data.pesticides_tonnes,
        "avg_temp": data.avg_temp,
        "Area": data.Area,
        "Item": data.Item
    }])

    prediction = model.predict(input_df)[0]

    return {
        "predicted_yield_hg_per_ha": round(float(prediction), 2)
    }
