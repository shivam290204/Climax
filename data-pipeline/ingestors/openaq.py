import os
from typing import Dict, Any, List, Optional
import requests
from datetime import datetime, timedelta, timezone

# Allow overriding the base URL or disabling OpenAQ ingestion via environment vars.
OPENAQ_BASE = os.getenv("OPENAQ_BASE", "https://api.openaq.org/v2")
OPENAQ_ENABLED = os.getenv("OPENAQ_ENABLED", "true").lower() not in {"0", "false", "no"}

# Delhi bounding box (approx): [min_lon, min_lat, max_lon, max_lat]
DELHI_BBOX = [76.84, 27.60, 77.58, 28.90]

DEFAULT_PARAMETERS = ["pm25", "pm10", "no2", "so2", "o3", "co"]


class OpenAQDisabled(Exception):
    pass


def fetch_measurements(limit: int = 1000, hours: int = 24, bbox: Optional[List[float]] = None,
                       parameters: Optional[List[str]] = None) -> Dict[str, Any]:
    """Fetch recent measurements for a bounding box (fallback for CPCB).

    Returns JSON dict on success. Raises for network/HTTP errors (except 410 which is rephrased).
    If OPENAQ_ENABLED is false, raises OpenAQDisabled.
    """
    if not OPENAQ_ENABLED:
        raise OpenAQDisabled("OpenAQ ingestion disabled via OPENAQ_ENABLED env variable")

    if bbox is None:
        bbox = DELHI_BBOX
    if parameters is None:
        parameters = DEFAULT_PARAMETERS

    date_to = datetime.now(timezone.utc)
    date_from = date_to - timedelta(hours=hours)

    params = {
        "limit": limit,
        "page": 1,
        "offset": 0,
        "sort": "desc",
        "order_by": "datetime",
        "date_from": date_from.replace(microsecond=0).isoformat(),
        "date_to": date_to.replace(microsecond=0).isoformat(),
        "parameter": parameters,
        "bbox": ",".join(map(str, bbox)),
    }
    try:
        r = requests.get(f"{OPENAQ_BASE}/measurements", params=params, timeout=30, headers={"Accept": "application/json"})
        if r.status_code == 410:
            # Provide a structured stub so caller can decide to synthesize.
            return {
                "results": [],
                "warning": "OpenAQ measurements endpoint responded 410 (Gone) - API version or parameters may have changed.",
                "status_code": 410,
                "requested": {
                    "hours": hours,
                    "bbox": bbox,
                    "parameters": parameters
                }
            }
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        # Re-raise so runner can capture and log uniformly.
        raise
