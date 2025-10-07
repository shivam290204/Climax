# Notebooks

Place exploratory data analysis and experimentation notebooks here.

Recommended naming:
- `01_exploration_data_quality.ipynb`
- `02_feature_engineering_pm25.ipynb`
- `03_model_rf_baseline.ipynb`
- `10_lstm_sequence_forecast.ipynb`

Guidelines:
- Avoid committing large raw outputs (clear cell outputs or trust only key visualizations).
- Keep environment-light (prefer `%pip install` inside notebook only if absolutely necessary).
- Move production-ready feature code into `data_prep.py` / `model_utils.py`.
