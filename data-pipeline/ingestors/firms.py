import requests
import datetime as dt
from typing import Dict, Any

# NASA FIRMS: CSV download endpoints (no key for recent data) docs:
# https://firms.modaps.eosdis.nasa.gov/api/

FIRMS_URL = "https://firms.modaps.eosdis.nasa.gov/api/country/csv/MODIS/24h/IND"


def fetch_fires_24h(country_code: str = "IND") -> str:
    """Fetch last 24h fire hotspots CSV for country (default India). Returns CSV text."""
    url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/VIIRS_SNPP_NRT/24h/{country_code}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text
