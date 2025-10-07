# [file name]: ml-models/evaluate_random_forest.py
"""Evaluate a previously trained Random Forest model on the latest fused dataset.
Usage:
  python evaluate_random_forest.py
"""

from pathlib import Path
import json
import pandas as pd
from data_prep import build_dataset
from model_utils import load_model_bundle, predict_pm25
from config import METRICS_PATH, MODEL_BUNDLE_PATH


def evaluate():
    bundle = load_model_bundle(MODEL_BUNDLE_PATH)
    data = build_dataset()
    # Build feature rows
    X = data.drop(columns=["pm25", "timestamp"])
    y_true = data["pm25"].values
    preds = []
    for _, row in X.iterrows():
        pred = predict_pm25(bundle, row.to_dict())
        preds.append(pred["pm25"])
    import numpy as np
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    y_true_arr = np.asarray(y_true, dtype="float64")
    preds_arr = np.asarray(preds, dtype="float64")
    mae = mean_absolute_error(y_true_arr, preds_arr)
    # FIX: Calculate RMSE manually
    rmse = mean_squared_error(y_true_arr, preds_arr) ** 0.5
    r2 = r2_score(y_true_arr, preds_arr)
    metrics = {
        "eval_mae": float(mae),
        "eval_rmse": float(rmse),
        "eval_r2": float(r2),
        "n_samples": int(len(y_true)),
    }
    print(json.dumps(metrics, indent=2))
    # Merge with existing metrics file if present
    if METRICS_PATH.exists():
        existing = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
        existing.update(metrics)
        METRICS_PATH.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    return metrics


if __name__ == "__main__":
    evaluate()