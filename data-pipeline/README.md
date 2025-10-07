# Data Pipeline

This pipeline fetches and validates multi-modal data for Delhi-NCR.

Sources (free/public to get you started):
- OpenAQ (ground monitors; fallback while CPCB API keys/process are arranged)
- NASA FIRMS (fire hotspots)
- Open-Meteo (weather forecasts & reanalysis)
- Open-Meteo Air Quality (PM2.5, PM10, gases) — feeds ML model training

You can later switch to CPCB official APIs/feeds and IMD once credentials/agreements are ready.

## Run locally

- Python 3.11 recommended. Create a venv and install minimal deps (requests, pandas).
- Set environment variables in `.env` at repo root (optional for these public endpoints).

## Quick start

Use the thin runner script to fetch recent data:

- OpenAQ last 24h for Delhi bounding box
- NASA FIRMS last 24h for North India
- Open-Meteo hourly weather for coordinates

The data prints to stdout and writes JSON/CSV under `data-pipeline/output/`.

Runner guarantees an output even on partial failures by generating a synthetic fallback dataset and writing a `run_manifest.json` summarizing successes, durations, and any errors.

## Extend

- Replace OpenAQ with CPCB ingestor: plug your API URL and auth in `ingestors/cpcb.py`.
- Add validation & DB writes: call backend DB via SQLAlchemy or send to backend API.
- Schedule with Celery beat or Windows Task Scheduler.
- Persist to TimescaleDB: adapt runner to open async SQLAlchemy session and insert normalized rows.
- Add quality checks (row counts, null thresholds) -> fail fast on anomalies.
