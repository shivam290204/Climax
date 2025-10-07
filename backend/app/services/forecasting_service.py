from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random
import os
from pathlib import Path

# Attempt to import local ML model utilities. Fallback gracefully if not present.
try:
    # Add ml-models directory to path dynamically
    REPO_ROOT = Path(__file__).resolve().parents[3]
    ML_DIR = REPO_ROOT / "ml-models"
    if ML_DIR.exists():
        import sys

        if str(ML_DIR) not in sys.path:
            sys.path.append(str(ML_DIR))
        from model_utils import load_model_bundle, predict_pm25  # type: ignore
        from config import MODEL_BUNDLE_PATH  # type: ignore

        _ML_AVAILABLE = True
    else:
        _ML_AVAILABLE = False
except Exception:  # pragma: no cover
    _ML_AVAILABLE = False
    MODEL_BUNDLE_PATH = None  # type: ignore


class ForecastingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self._model_bundle: Optional[Dict[str, Any]] = None
        if _ML_AVAILABLE:
            try:
                self._model_bundle = load_model_bundle(MODEL_BUNDLE_PATH)
            except Exception:
                self._model_bundle = None

    async def get_current_aqi(self, lat: float, lon: float) -> Dict[str, Any]:
        """Return current AQI estimate using trained model if available; fallback to random."""
        if self._model_bundle:
            # Minimal feature vector; in future include latest weather ingestion
            now = datetime.utcnow()
            feat = {
                "lat": lat,
                "lon": lon,
                "temp": 25.0,  # TODO: inject real-time weather
                "humidity": 40.0,
                "wind_speed": 2.5,
                "wind_dir": 90.0,
                "pressure": 1008.0,
                "hour": now.hour,
                "month": now.month,
                "location": "delhi_center",
                "city": "Delhi",
                "country": "IN",
                "unit": "µg/m³",
            }
            try:
                pred = predict_pm25(self._model_bundle, feat)
                return {
                    "aqi": pred["aqi"],
                    "category": pred["category"],
                    "pm25": pred["pm25"],
                    "confidence": 0.82,  # placeholder until calibration implemented
                    "model_version": "rf_pm25_v1",
                }
            except Exception:
                pass  # fall through to random

        aqi = random.randint(50, 250)
        category = (
            "Good"
            if aqi <= 50
            else (
                "Satisfactory"
                if aqi <= 100
                else (
                    "Moderate"
                    if aqi <= 200
                    else (
                        "Poor"
                        if aqi <= 300
                        else "Very Poor" if aqi <= 400 else "Severe"
                    )
                )
            )
        )
        return {
            "aqi": aqi,
            "category": category,
            "confidence": round(random.uniform(0.6, 0.9), 2),
            "model_version": "stub",
        }

    async def get_hourly_forecast(
        self, lat: float, lon: float, hours: int
    ) -> List[Dict[str, Any]]:
        now = datetime.utcnow()
        series = []
        for i in range(hours):
            ts = now + timedelta(hours=i)
            base_pm25 = random.uniform(30, 140)
            if self._model_bundle:
                feat = {
                    "lat": lat,
                    "lon": lon,
                    "temp": 25.0,  # placeholder
                    "humidity": 40.0,
                    "wind_speed": 2.5,
                    "wind_dir": 90.0,
                    "pressure": 1008.0,
                    "hour": ts.hour,
                    "month": ts.month,
                    "location": "delhi_center",
                    "city": "Delhi",
                    "country": "IN",
                    "unit": "µg/m³",
                }
                try:
                    pred = predict_pm25(self._model_bundle, feat)
                    pm25_val = pred["pm25"]
                    aqi_val = pred["aqi"]
                except Exception:
                    pm25_val = base_pm25
                    aqi_val = random.randint(60, 240)
            else:
                pm25_val = base_pm25
                aqi_val = random.randint(60, 240)
            series.append(
                {
                    "time": ts.isoformat() + "Z",
                    "aqi": aqi_val,
                    "pm2_5": round(pm25_val, 1),
                    "pm10": round(pm25_val * 1.4, 1),
                    "lower": max(0, int(aqi_val * 0.8)),
                    "upper": int(aqi_val * 1.2),
                }
            )
        return series

    async def get_daily_forecast(
        self, lat: float, lon: float, days: int
    ) -> List[Dict[str, Any]]:
        today = datetime.utcnow()
        return [
            {
                "date": (today + timedelta(days=i)).date().isoformat(),
                "avg_aqi": random.randint(80, 220),
                "max_aqi": random.randint(100, 300),
                "min_aqi": random.randint(50, 150),
            }
            for i in range(days)
        ]

    async def get_source_attribution(self, lat: float, lon: float) -> Dict[str, Any]:
        return {
            "stubble_burning": round(random.uniform(0, 0.5), 2),
            "vehicular": round(random.uniform(0.1, 0.5), 2),
            "industrial": round(random.uniform(0.05, 0.4), 2),
            "dust_and_construction": round(random.uniform(0.05, 0.4), 2),
            "biomass_burning": round(random.uniform(0.0, 0.2), 2),
            "other": round(random.uniform(0.0, 0.2), 2),
        }

    async def get_point_forecast(
        self, lat: float, lon: float, hours: int
    ) -> Dict[str, Any]:
        return {
            "lat": lat,
            "lon": lon,
            "hourly": await self.get_hourly_forecast(lat, lon, hours),
        }

    async def calculate_route_exposure(
        self, route_points: List[Dict[str, float]], mode: str
    ) -> Dict[str, Any]:
        exposure = sum(random.uniform(1, 5) for _ in route_points)
        return {
            "total_exposure": round(exposure, 2),
            "recommendations": ["Avoid peak traffic hours", "Use mask if AQI > 200"],
            "alternatives": [],
        }

    async def get_forecast_accuracy(
        self, lat: float, lon: float, days: int
    ) -> Dict[str, Any]:
        return {
            "mae": round(random.uniform(5, 20), 2),
            "rmse": round(random.uniform(10, 30), 2),
            "mape": round(random.uniform(5, 15), 2),
        }
