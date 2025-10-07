# [file name]: ml-models/fetch_data.py
"""Data pipeline to fetch air quality and weather data from Open-Meteo API."""
import requests
import json
from pathlib import Path
from config import DATA_OUTPUT_DIR

# Delhi coordinates
DELHI_LAT = 28.6139
DELHI_LON = 77.2090

def fetch_air_quality_data():
    """Fetch air quality data from Open-Meteo API."""
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        'latitude': DELHI_LAT,
        'longitude': DELHI_LON,
        'hourly': ['pm2_5', 'pm10', 'nitrogen_dioxide', 'sulphur_dioxide', 'ozone', 'carbon_monoxide'],
        'timezone': 'Asia/Kolkata',
        'past_days': 1,
        'forecast_days': 3
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def fetch_weather_data():
    """Fetch weather data from Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': DELHI_LAT,
        'longitude': DELHI_LON,
        'hourly': ['temperature_2m', 'relative_humidity_2m', 'wind_speed_10m', 
                  'wind_direction_10m', 'surface_pressure'],
        'timezone': 'Asia/Kolkata',
        'past_days': 1,
        'forecast_days': 3
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def run_data_pipeline():
    """Run the complete data pipeline."""
    print("Fetching air quality data...")
    air_data = fetch_air_quality_data()
    
    print("Fetching weather data...")
    weather_data = fetch_weather_data()
    
    # Ensure output directory exists
    DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save data
    air_file = DATA_OUTPUT_DIR / "open_meteo_air_delhi_72h.json"
    weather_file = DATA_OUTPUT_DIR / "open_meteo_delhi_72h.json"
    
    with open(air_file, 'w', encoding='utf-8') as f:
        json.dump(air_data, f, indent=2)
    
    with open(weather_file, 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, indent=2)
    
    print(f"Data saved to:")
    print(f"  - {air_file}")
    print(f"  - {weather_file}")
    print("Data pipeline completed successfully!")

if __name__ == "__main__":
    run_data_pipeline()