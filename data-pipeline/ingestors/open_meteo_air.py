import requests
from typing import Dict, Any

OPEN_METEO_AIR_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


def fetch_hourly_air_quality(lat: float, lon: float) -> Dict[str, Any]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "pm2_5",
            "pm10",
            "nitrogen_dioxide",
            "sulphur_dioxide",
            "ozone",
            "carbon_monoxide",
        ],
        "forecast_days": 3,
        "timezone": "UTC",
    }
    r = requests.get(OPEN_METEO_AIR_URL, params=params, timeout=30)
    r.raise_for_status()
    return r.json()
