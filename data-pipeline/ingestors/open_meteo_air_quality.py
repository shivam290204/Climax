import requests
from typing import Dict, Any

AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


def fetch_air_quality(lat: float, lon: float, hours: int = 72) -> Dict[str, Any]:
    """Fetch hourly air quality variables (PM2.5, PM10, gases) from Open-Meteo API.
    https://open-meteo.com/en/docs/air-quality-api
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide,ammonia",  # add more if needed
        "timezone": "UTC",
    }
    r = requests.get(AIR_QUALITY_URL, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    # Optionally trim hours if requested < default
    if hours < len(data.get("hourly", {}).get("time", [])):
        for k, v in data.get("hourly", {}).items():
            data["hourly"][k] = v[:hours]
    return data
