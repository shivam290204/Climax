-- NOTE: The current container image (timescale/timescaledb:latest-pg14) does NOT bundle PostGIS.
-- The previous attempt failed on: could not open extension control file "postgis.control".
-- If you need PostGIS later, either:
--   1. Switch image to one with PostGIS (e.g. timescale/timescaledb-ha:pg14 or build a custom image adding postgis)
--   2. Install PostGIS packages inside a custom Dockerfile.
-- For now we comment out PostGIS to allow DB initialization to succeed.
-- CREATE EXTENSION IF NOT EXISTS postgis;  -- (disabled)
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Example hypertable for AQI readings
CREATE TABLE IF NOT EXISTS core.aqi_readings (
    id UUID PRIMARY KEY,
    station_id TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    pm2_5 DOUBLE PRECISION,
    pm10 DOUBLE PRECISION,
    no2 DOUBLE PRECISION,
    so2 DOUBLE PRECISION,
    o3 DOUBLE PRECISION,
    co DOUBLE PRECISION,
    aqi INTEGER,
    aqi_category TEXT,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    wind_speed DOUBLE PRECISION,
    wind_direction DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    data_source TEXT DEFAULT 'CPCB',
    quality_flag TEXT DEFAULT 'valid'
);

SELECT create_hypertable('core.aqi_readings', 'timestamp', if_not_exists => TRUE);

-- PostGIS related geometry column & index disabled until PostGIS is available
-- SELECT AddGeometryColumn('core', 'aqi_readings', 'geom', 4326, 'POINT', 2);
-- CREATE INDEX IF NOT EXISTS idx_aqi_geom ON core.aqi_readings USING GIST (geom);

-- Additional tables can be created later via migrations