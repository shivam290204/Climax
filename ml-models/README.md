# ML Models

Current implemented pipeline: Random Forest regression model predicting PM2.5 which is mapped to AQI (Indian scale) and served via the FastAPI backend (`ForecastingService`).

## Implemented
- Data fusion: Open-Meteo air quality + meteorological hourly JSON (produced by `data-pipeline/runner.py`).
- Feature engineering: temporal (hour, month), meteorology, geolocation categorical dummies.
- Model: `RandomForestRegressor` with cross‑validation metrics.
- Artifacts saved to `ml-models/models/`:
  - `rf_pm25_model.joblib` (bundle with pipeline + feature column order)
  - `rf_pm25_metrics.json` (train/test + CV metrics, later evaluation updates)
  - `rf_pm25_metadata.json` (model descriptor)

## Directory Layout
- `config.py` – central paths & constants
- `data_prep.py` – dataset construction & feature engineering
- `model_utils.py` – model loading, PM2.5→AQI mapping utilities
- `train_random_forest.py` – training script with optional cross‑validation
- `evaluate_random_forest.py` – re-evaluates model on latest fused dataset
- `predict_random_forest.py` – simple CLI prediction example (legacy; kept for convenience)

## Environment Variables
| Variable | Purpose | Default |
|----------|---------|---------|
| `ML_MODEL_DIR` | Directory where model artifacts are stored/loaded | `ml-models/models` |

Backend attempts to load the bundle at startup; if missing it falls back to synthetic random values until a model is trained.

## Workflow
1. Run data pipeline to populate raw JSON outputs:
	```bash
	python data-pipeline/runner.py
	```
2. Train model:
	```bash
	python ml-models/train_random_forest.py
	```
3. (Optional) Evaluate on latest data snapshot:
	```bash
	python ml-models/evaluate_random_forest.py
	```
4. Start backend (it will load `rf_pm25_model.joblib` if present):
	```bash
	uvicorn backend.app.main:app --reload
	```

## Metrics Captured
`rf_pm25_metrics.json` contains:
```json
{
  "mae": <float>,
  "rmse": <float>,
  "r2": <float>,
  "cv_mae_mean": <float>,
  "cv_rmse_mean": <float>,
  "cv_r2_mean": <float>
}
```

## AQI Mapping
PM2.5 is translated to Indian AQI scale using breakpoint linear interpolation defined in `config.py`.

## Next Planned Enhancements
- Add temporal lag features and rolling statistics (24h mean, yesterday same hour).
- Add geospatial context (distance to fires, traffic density proxy, population-weighted centroids).
- Introduce LSTM or Temporal Fusion Transformer for sequence forecasting.
- Kriging or Gaussian Process spatial interpolation for hyperlocal grid.
- Ensemble layer combining RF + deep temporal + spatial models.
- MLflow experiment tracking & model registry integration.
- Automated retraining workflow (daily cron with data freshness checks).

## Notebooks
Exploratory data analysis and prototype modeling notebooks live in `notebooks/` (add as needed). Avoid committing large outputs.

## Reproducibility Notes
- Dependencies are currently unpinned in backend; for stable ML training create a dedicated `ml-models/requirements.txt` (present) and consider freezing versions with a lock file.
- Random seeds fixed where relevant, but parallelism in Random Forest can introduce minor nondeterminism.

---
Questions or requests for additional model types? Extend `model_utils.py` and add a sibling training script following the same artifact pattern.