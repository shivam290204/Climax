"""Database configuration and ORM model declarations.

Improvements applied:
 - Safe construction of DATABASE_URL with validation.
 - Updated import path for declarative_base (SQLAlchemy 2.x recommendation).
 - Added naming convention metadata for future migrations.
 - Added sensible defaults for created_at / updated_at style columns.
 - Added pool_pre_ping for more robust long-lived connections.
 - Centralized environment variable access with fallback and explicit error if required parts missing.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    Boolean,
    JSON,
    MetaData,
    event,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import os
from dotenv import load_dotenv
from typing import AsyncGenerator
import asyncio
import logging

load_dotenv()


def _build_database_url() -> str:
    user = os.getenv("DB_USER") or ""
    password = os.getenv("DB_PASSWORD") or ""
    host = os.getenv("DB_HOST") or "localhost"
    port = os.getenv("DB_PORT") or "5432"
    name = os.getenv("DB_NAME") or ""
    missing = [
        k
        for k, v in {"DB_USER": user, "DB_PASSWORD": password, "DB_NAME": name}.items()
        if not v
    ]
    if missing:
        # Provide clear early failure instead of cryptic asyncpg errors
        raise RuntimeError(
            f"Missing required database environment variables: {', '.join(missing)}"
        )
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"


DATABASE_URL = _build_database_url()

ECHO_SQL = os.getenv("SQL_ECHO", "false").lower() == "true"
engine = create_async_engine(
    DATABASE_URL,
    echo=ECHO_SQL,
    pool_pre_ping=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async DB session."""
    async with AsyncSessionLocal() as session:  # type: ignore[call-arg]
        yield session


async def init_db():
    """Create tables if they do not exist with retry logic.

    Environment variables to control behavior:
      SKIP_DB_INIT=1          -> Skip initialization entirely (useful for tests without DB)
      DB_INIT_MAX_RETRIES=10  -> Number of connection attempts (default 10)
      DB_INIT_SLEEP_SECONDS=2 -> Seconds to wait between attempts (default 2)
      ALLOW_DB_FAILURE=1      -> Continue startup even if DB never became available
    """
    if os.getenv("SKIP_DB_INIT") == "1":
        print("[DB] SKIP_DB_INIT=1 set – skipping database initialization")
        return

    retries = int(os.getenv("DB_INIT_MAX_RETRIES", "10"))
    sleep_seconds = float(os.getenv("DB_INIT_SLEEP_SECONDS", "2"))
    allow_failure = os.getenv("ALLOW_DB_FAILURE") == "1"

    last_exc: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print(f"[DB] Initialization successful on attempt {attempt}")
            return
        except Exception as e:  # Broad by design: connectivity / DDL errors
            last_exc = e
            print(
                f"[DB] Attempt {attempt}/{retries} failed: {e.__class__.__name__}: {e}"
            )
            if attempt < retries:
                await asyncio.sleep(sleep_seconds)

    # Exhausted retries
    if allow_failure:
        print(
            f"[DB] WARNING: ALLOW_DB_FAILURE=1 set – proceeding without DB after failure: {last_exc}"
        )
        return
    # Re-raise last exception to fail fast
    assert last_exc is not None
    raise last_exc


# Database Models
class AQIReading(Base):
    """Model for AQI readings from monitoring stations"""

    __tablename__ = "aqi_readings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Pollutant measurements
    pm2_5 = Column(Float)
    pm10 = Column(Float)
    no2 = Column(Float)
    so2 = Column(Float)
    o3 = Column(Float)
    co = Column(Float)

    # Calculated AQI
    aqi = Column(Integer)
    aqi_category = Column(String)

    # Weather data
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(Float)
    pressure = Column(Float)

    # Additional metadata
    data_source = Column(String, default="CPCB")
    quality_flag = Column(String, default="valid")


class SourceAttribution(Base):
    """Model for pollution source attribution data"""

    __tablename__ = "source_attribution"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Source contributions (percentages)
    stubble_burning = Column(Float, default=0.0)
    vehicular = Column(Float, default=0.0)
    industrial = Column(Float, default=0.0)
    dust_and_construction = Column(Float, default=0.0)
    biomass_burning = Column(Float, default=0.0)
    other = Column(Float, default=0.0)

    # Model confidence
    confidence_score = Column(Float)
    model_version = Column(String)


class AQIForecast(Base):
    """Model for AQI forecast data"""

    __tablename__ = "aqi_forecasts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_timestamp = Column(DateTime, nullable=False, index=True)
    target_timestamp = Column(DateTime, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Forecast values
    predicted_aqi = Column(Integer)
    predicted_pm2_5 = Column(Float)
    predicted_pm10 = Column(Float)

    # Confidence intervals
    aqi_lower = Column(Integer)
    aqi_upper = Column(Integer)
    confidence_level = Column(Float, default=0.95)

    # Model metadata
    model_name = Column(String)
    model_version = Column(String)
    forecast_horizon_hours = Column(Integer)


class User(Base):
    """Model for app users"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # User preferences
    home_latitude = Column(Float)
    home_longitude = Column(Float)
    work_latitude = Column(Float)
    work_longitude = Column(Float)

    # Health profile
    age_group = Column(String)  # child, adult, senior
    health_conditions = Column(JSON)  # [asthma, heart_disease, etc.]
    activity_level = Column(String)  # low, moderate, high

    # Notification preferences
    alert_threshold = Column(Integer, default=150)  # AQI threshold for alerts
    notification_enabled = Column(Boolean, default=True)
    notification_channels = Column(JSON)  # [email, push, sms]

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class HealthRecommendation(Base):
    """Model for personalized health recommendations"""

    __tablename__ = "health_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False)

    # Location and AQI context
    latitude = Column(Float)
    longitude = Column(Float)
    current_aqi = Column(Integer)

    # Recommendations
    activity_advice = Column(String)
    outdoor_duration = Column(String)
    mask_recommendation = Column(String)
    route_suggestion = Column(String)

    # Risk assessment
    health_risk_level = Column(String)  # low, moderate, high, severe
    risk_factors = Column(JSON)

    # Engagement tracking
    viewed = Column(Boolean, default=False)
    followed = Column(Boolean, default=False)
    feedback_rating = Column(Integer)  # 1-5 stars


class PolicyIntervention(Base):
    """Model for policy interventions and their impacts"""

    __tablename__ = "policy_interventions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    intervention_name = Column(String, nullable=False)
    intervention_type = Column(
        String, nullable=False
    )  # odd_even, construction_ban, etc.
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)

    # Geographic coverage
    affected_areas = Column(JSON)  # List of polygon coordinates

    # Impact metrics
    baseline_aqi = Column(Float)
    post_intervention_aqi = Column(Float)
    effectiveness_percentage = Column(Float)

    # Cost-benefit analysis
    implementation_cost = Column(Float)
    health_benefits = Column(Float)
    economic_impact = Column(Float)

    # Status
    status = Column(String, default="planned")  # planned, active, completed, cancelled
    created_by = Column(String)


class FireHotspot(Base):
    """Model for fire hotspot data from NASA FIRMS"""

    __tablename__ = "fire_hotspots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Fire characteristics
    brightness = Column(Float)
    confidence = Column(Float)
    fire_radiative_power = Column(Float)

    # Satellite info
    satellite = Column(String)
    instrument = Column(String)

    # Processing flags
    track = Column(String)
    acquisition_date = Column(DateTime)
    acquisition_time = Column(String)
