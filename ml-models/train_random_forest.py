# [file name]: ml-models/train_random_forest.py
"""Training script for Random Forest PM2.5 model.

Enhancements vs previous version:
 - Uses central config & data prep modules
 - Saves separate metrics & metadata JSON
 - Adds simple K-fold cross validation for robustness (optional)
 - Provides CLI-friendly output
"""

from pathlib import Path
import json
from typing import Tuple, Dict, Any
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import joblib
from dotenv import load_dotenv

from data_prep import build_dataset
from config import (
    MODEL_BUNDLE_PATH,
    METRICS_PATH,
    METADATA_PATH,
)

# Load root .env if present
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


NUMERIC_FEATURES = [
    "lat",
    "lon",
    "temp",
    "humidity",
    "wind_speed",
    "wind_dir",
    "pressure",
    "hour",
    "month",
]
CATEGORICAL_FEATURES = ["location", "city", "country", "unit"]


def build_pipeline(n_estimators: int = 300, max_depth: int | None = None) -> Pipeline:
    pre = ColumnTransformer(
        transformers=[
            ("num", "passthrough", NUMERIC_FEATURES),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES,
            ),
        ]
    )
    rf = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        n_jobs=-1,
        random_state=42,
    )
    return Pipeline(steps=[("pre", pre), ("rf", rf)])


def cross_validate(X: pd.DataFrame, y, n_splits: int = 5) -> Dict[str, float]:
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    maes, rmses, r2s = [], [], []
    for train_idx, test_idx in kf.split(X):
        X_tr, X_te = X.iloc[train_idx], X.iloc[test_idx]
        y_tr, y_te = y[train_idx], y[test_idx]
        pipe = build_pipeline()
        pipe.fit(X_tr, y_tr)
        preds = pipe.predict(X_te)
        maes.append(mean_absolute_error(y_te, preds))
        # FIX: Calculate RMSE manually
        rmses.append(mean_squared_error(y_te, preds) ** 0.5)
        r2s.append(r2_score(y_te, preds))
    return {
        "cv_mae_mean": float(pd.Series(maes).mean()),
        "cv_rmse_mean": float(pd.Series(rmses).mean()),
        "cv_r2_mean": float(pd.Series(r2s).mean()),
    }


def train(save: bool = True, do_cv: bool = True) -> Tuple[Pipeline, Dict[str, Any]]:
    data = build_dataset()
    y = data["pm25"].values
    X = data.drop(columns=["pm25", "timestamp"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    pipe = build_pipeline()
    pipe.fit(X_train, y_train)

    preds = pipe.predict(X_test)
    metrics = {
        "mae": float(mean_absolute_error(y_test, preds)),
        # FIX: Calculate RMSE manually instead of using squared=False
        "rmse": float(mean_squared_error(y_test, preds) ** 0.5),
        "r2": float(r2_score(y_test, preds)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
    }
    if do_cv:
        metrics.update(cross_validate(X, y, n_splits=5))

    metadata = {
        "model_type": "RandomForestRegressor",
        "library": "scikit-learn",
        "version": "1.0",
        "features": list(X.columns),
        "target": "pm25",
    }

    if save:
        joblib.dump(
            {"pipeline": pipe, "feature_columns": list(X.columns)}, MODEL_BUNDLE_PATH
        )
        METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print("Model saved to", MODEL_BUNDLE_PATH)
    print("Metrics:", json.dumps(metrics, indent=2))
    return pipe, metrics


if __name__ == "__main__":
    train()