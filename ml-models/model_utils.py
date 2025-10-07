from __future__ import annotations
from pathlib import Path
import json
import joblib
import pandas as pd
from typing import Dict, Any
from config import MODEL_BUNDLE_PATH, AQI_BREAKPOINTS_PM25, CATEGORY_LABELS


def pm25_to_aqi(pm25: float) -> int:
    for low_c, high_c, low_i, high_i in AQI_BREAKPOINTS_PM25:
        if low_c <= pm25 <= high_c:
            # Linear interpolation within the breakpoint range
            return int((high_i - low_i) / (high_c - low_c) * (pm25 - low_c) + low_i)
    # Above highest range -> cap 500
    return 500


def aqi_category(aqi: int) -> str:
    idx = 0
    if aqi <= 50:
        idx = 0
    elif aqi <= 100:
        idx = 1
    elif aqi <= 200:
        idx = 2
    elif aqi <= 300:
        idx = 3
    elif aqi <= 400:
        idx = 4
    else:
        idx = 5
    return CATEGORY_LABELS[idx]


def load_model_bundle(path: Path | None = None) -> Dict[str, Any]:
    p = path or MODEL_BUNDLE_PATH
    if not p.exists():
        raise FileNotFoundError(
            f"Model bundle not found at {p}. Train the model first."
        )
    return joblib.load(p)


def predict_pm25(bundle: Dict[str, Any], row: Dict[str, Any]) -> Dict[str, Any]:
    pipe = bundle["pipeline"]
    feature_columns = bundle["feature_columns"]
    df = pd.DataFrame([row])[feature_columns]
    pm25 = float(pipe.predict(df)[0])
    aqi = pm25_to_aqi(pm25)
    return {"pm25": pm25, "aqi": aqi, "category": aqi_category(aqi)}
