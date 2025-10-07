import os
from dotenv import load_dotenv
from ingestors.openaq import fetch_measurements
from ingestors.firms import fetch_fires_24h
from ingestors.open_meteo import fetch_hourly_weather
from ingestors.open_meteo_air_quality import fetch_air_quality
from utils.io import write_json, write_csv, OUTPUT_DIR
import traceback
import json
from datetime import datetime, timezone

# Load root .env if present
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    artifacts = {}

    # Helper to wrap fetches
    def attempt(name, func, writer, filename):
        print(f"[START] {name}")
        try:
            data = func()
            # Special handling: OpenAQ may return structured 410 stub (empty results but not exception)
            if name == "openaq" and isinstance(data, dict) and data.get("status_code") == 410:
                print("[WARN] OpenAQ returned 410 (Gone); will synthesize surrogate dataset.")
                artifacts[name] = {"status": "gone", "message": data.get("warning", "410 Gone"), "file": None}
            else:
                path = writer(data, filename)
                print(f"[OK] {name} -> {path}")
                artifacts[name] = {"status": "ok", "file": path}
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            traceback.print_exc()
            # Write a diagnostic stub so downstream steps still find something
            stub = {"error": str(e), "name": name, "timestamp": datetime.now(timezone.utc).isoformat()}
            path = write_json(stub, f"failed_{filename.replace('.json','')}.json") if filename.endswith('.json') else write_csv(str(stub), f"failed_{filename}")
            artifacts[name] = {"status": "error", "file": path, "message": str(e)}

    # OpenAQ (fallback; if fails we will synthesize minimal dataset for training)
    def fetch_openaq():
        return fetch_measurements(limit=1000, hours=24)
    attempt("openaq", fetch_openaq, write_json, "openaq_delhi_24h.json")

    # NASA FIRMS
    def fetch_firms():
        return fetch_fires_24h("IND")
    attempt("firms", fetch_firms, write_csv, "firms_india_24h.csv")

    # Weather (Open-Meteo)
    def fetch_weather():
        return fetch_hourly_weather(28.6139, 77.2090)
    attempt("weather", fetch_weather, write_json, "open_meteo_delhi_72h.json")

    # Air Quality (Open-Meteo)
    def fetch_airq():
        return fetch_air_quality(28.6139, 77.2090, hours=72)
    attempt("air_quality", fetch_airq, write_json, "open_meteo_air_quality_72h.json")

    # If OpenAQ failed, synthesize a simple surrogate dataset compatible with training script
    if artifacts.get("openaq", {}).get("status") in {"gone", "error"}:
        print("[INFO] Generating synthetic OpenAQ-like dataset for continuity…")
        synthetic = {
            "results": [
                {
                    "date": {"utc": datetime.now(timezone.utc).isoformat()},
                    "parameter": "pm25",
                    "value": 90.0,
                    "unit": "µg/m³",
                    "location": "synthetic_station",
                    "city": "Delhi",
                    "country": "IN",
                    "coordinates": {"latitude": 28.61, "longitude": 77.21}
                }
                for _ in range(24)
            ]
        }
        synth_path = write_json(synthetic, "openaq_delhi_24h.json")
        artifacts["openaq"] = {"status": "synthetic", "file": synth_path}
        print(f"[OK] Synthetic OpenAQ dataset -> {synth_path}")

    # Summary manifest
    manifest_path = write_json(artifacts, "run_manifest.json")
    print(f"Run manifest: {manifest_path}")
    print("Done.")

    print("Done.")


if __name__ == "__main__":
    main()
