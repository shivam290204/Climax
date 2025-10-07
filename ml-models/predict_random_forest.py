import sys
from pathlib import Path
import json
import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent / "models" / "rf_pm25_model.joblib"


def predict_one(
    lat: float,
    lon: float,
    temp: float,
    humidity: float,
    wind_speed: float,
    wind_dir: float,
    pressure: float,
    hour: int,
    month: int,
    location: str = "unknown",
    city: str = "Delhi",
    country: str = "IN",
    unit: str = "µg/m³",
):
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}. Train it with train_random_forest.py first."
        )
    bundle = joblib.load(MODEL_PATH)
    pipe = bundle["pipeline"]
    feature_columns = bundle["feature_columns"]

    row = {
        "lat": lat,
        "lon": lon,
        "temp": temp,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "wind_dir": wind_dir,
        "pressure": pressure,
        "hour": hour,
        "month": month,
        "location": location,
        "city": city,
        "country": country,
        "unit": unit,
    }
    X = pd.DataFrame([row])[feature_columns]
    pred = float(pipe.predict(X)[0])
    return {"pm25_prediction": pred}


if __name__ == "__main__":
    # Example CLI usage
    out = predict_one(28.61, 77.21, 25.0, 40.0, 2.5, 90.0, 1008.0, 8, 10)
    print(json.dumps(out, indent=2))
