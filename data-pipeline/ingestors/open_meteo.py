import requests
from typing import Dict, Any

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_hourly_weather(lat: float, lon: float) -> Dict[str, Any]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
            "wind_direction_10m",
            "surface_pressure",
        ],
        "forecast_days": 3,
        "timezone": "UTC",
    }
    r = requests.get(OPEN_METEO_URL, params=params, timeout=30)
    r.raise_for_status()
    return r.json()
