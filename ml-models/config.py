from pathlib import Path
import os

# Root of repository inferred from this file location
ROOT = Path(__file__).resolve().parents[1]
DATA_OUTPUT_DIR = ROOT / "data-pipeline" / "output"
MODEL_DIR = Path(os.getenv("ML_MODEL_DIR", Path(__file__).resolve().parent / "models"))
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_BUNDLE_PATH = MODEL_DIR / "rf_pm25_model.joblib"
METRICS_PATH = MODEL_DIR / "rf_pm25_metrics.json"
METADATA_PATH = MODEL_DIR / "rf_pm25_metadata.json"

DEFAULT_CITY = "Delhi"
DEFAULT_COUNTRY = "IN"

AQI_BREAKPOINTS_PM25 = [
    (0.0, 30.0, 0, 50),
    (30.0, 60.0, 51, 100),
    (60.0, 90.0, 101, 200),
    (90.0, 120.0, 201, 300),
    (120.0, 250.0, 301, 400),
    (250.0, 500.0, 401, 500),
]

CATEGORY_LABELS = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
