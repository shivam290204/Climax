# [file name]: ml-models/data_prep.py
from __future__ import annotations
from pathlib import Path
import json
import pandas as pd
from typing import Tuple
from config import DATA_OUTPUT_DIR, DEFAULT_CITY, DEFAULT_COUNTRY

AIR_FILE = DATA_OUTPUT_DIR / "open_meteo_air_delhi_72h.json"
WEATHER_FILE = DATA_OUTPUT_DIR / "open_meteo_delhi_72h.json"

REQUIRED_AIR_KEYS = [
    "pm2_5",
    "pm10",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone",
    "carbon_monoxide",
]
REQUIRED_WEATHER_KEYS = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "wind_direction_10m",
    "surface_pressure",
]


def load_raw() -> Tuple[dict, dict]:
    if not AIR_FILE.exists() or not WEATHER_FILE.exists():
        raise FileNotFoundError(
            "Required air/weather JSON not found. Run data pipeline first."
        )
    air = json.loads(AIR_FILE.read_text(encoding="utf-8"))
    weather = json.loads(WEATHER_FILE.read_text(encoding="utf-8"))
    return air, weather


def build_dataset() -> pd.DataFrame:
    air, weather = load_raw()
    ah = air.get("hourly", {})
    wh = weather.get("hourly", {})

    a_df = pd.DataFrame(
        {
            "timestamp": ah.get("time", []),
            "pm25": ah.get("pm2_5", []),
            "pm10": ah.get("pm10", []),
            "no2": ah.get("nitrogen_dioxide", []),
            "so2": ah.get("sulphur_dioxide", []),
            "o3": ah.get("ozone", []),
            "co": ah.get("carbon_monoxide", []),
        }
    )
    a_df["lat"] = 28.6139
    a_df["lon"] = 77.2090
    a_df["location"] = "delhi_center"
    a_df["city"] = DEFAULT_CITY
    a_df["country"] = DEFAULT_COUNTRY
    a_df["unit"] = "µg/m³"

    w_df = pd.DataFrame(
        {
            "timestamp": wh.get("time", []),
            "temp": wh.get("temperature_2m", []),
            "humidity": wh.get("relative_humidity_2m", []),
            "wind_speed": wh.get("wind_speed_10m", []),
            "wind_dir": wh.get("wind_direction_10m", []),
            "pressure": wh.get("surface_pressure", []),
        }
    )

    # FIX: Use 'h' instead of 'H' for hour
    a_df["timestamp"] = pd.to_datetime(a_df["timestamp"]).dt.floor("h")
    w_df["timestamp"] = pd.to_datetime(w_df["timestamp"]).dt.floor("h")

    fused = pd.merge_asof(
        a_df.sort_values("timestamp"),
        w_df.sort_values("timestamp"),
        on="timestamp",
        direction="nearest",
        # FIX: Use 'h' instead of 'H'
        tolerance=pd.Timedelta("1h"),
    )

    fused["hour"] = fused["timestamp"].dt.hour
    fused["month"] = fused["timestamp"].dt.month

    fused = fused.dropna(subset=["pm25", "temp", "humidity", "wind_speed"])
    return fused