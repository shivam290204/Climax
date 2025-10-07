from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, timedelta
import structlog
from pydantic import BaseModel, Field

from app.database import get_db
from app.services.forecasting_service import ForecastingService
from app.services.spatial_service import SpatialService

logger = structlog.get_logger()

router = APIRouter()


class LocationInput(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")


class ForecastResponse(BaseModel):
    timestamp: datetime
    location: LocationInput
    current_aqi: int
    current_category: str
    hourly_forecast: List[dict]
    daily_forecast: List[dict]
    source_attribution: dict
    confidence_score: float
    model_version: str


class HyperLocalForecastResponse(BaseModel):
    center_location: LocationInput
    grid_size_km: float
    grid_forecasts: List[List[dict]]
    timestamp: datetime
    forecast_horizon_hours: int


@router.get("/current", response_model=ForecastResponse)
async def get_current_forecast(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude coordinate"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude coordinate"),
    hours: int = Query(24, ge=1, le=72, description="Forecast horizon in hours"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get current AQI and forecast for a specific location

    Provides:
    - Current AQI and pollutant levels
    - Hourly forecast for next 24-72 hours
    - Daily forecast summary
    - Source attribution analysis
    - Confidence intervals
    """
    try:
        logger.info(
            "Fetching forecast", latitude=latitude, longitude=longitude, hours=hours
        )

        forecasting_service = ForecastingService(db)

        # Get current AQI
        current_data = await forecasting_service.get_current_aqi(latitude, longitude)

        # Get hourly forecast
        hourly_forecast = await forecasting_service.get_hourly_forecast(
            latitude, longitude, hours
        )

        # Get daily forecast summary
        daily_forecast = await forecasting_service.get_daily_forecast(
            latitude, longitude, min(hours // 24, 3)
        )

        # Get source attribution
        source_attribution = await forecasting_service.get_source_attribution(
            latitude, longitude
        )

        return ForecastResponse(
            timestamp=datetime.utcnow(),
            location=LocationInput(latitude=latitude, longitude=longitude),
            current_aqi=current_data["aqi"],
            current_category=current_data["category"],
            hourly_forecast=hourly_forecast,
            daily_forecast=daily_forecast,
            source_attribution=source_attribution,
            confidence_score=current_data["confidence"],
            model_version=current_data["model_version"],
        )

    except Exception as e:
        logger.error("Error fetching forecast", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch forecast data")


@router.get("/hyperlocal", response_model=HyperLocalForecastResponse)
async def get_hyperlocal_forecast(
    center_lat: float = Query(..., ge=-90, le=90, description="Center latitude"),
    center_lon: float = Query(..., ge=-180, le=180, description="Center longitude"),
    radius_km: float = Query(5, ge=1, le=50, description="Radius in kilometers"),
    resolution_km: float = Query(1, ge=0.5, le=5, description="Grid resolution in km"),
    hours: int = Query(24, ge=1, le=72, description="Forecast horizon in hours"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get hyperlocal forecasting grid at 1km x 1km resolution

    Provides:
    - Spatial grid of AQI forecasts
    - 1km x 1km resolution predictions
    - Kriging spatial interpolation
    - Wind dispersion modeling
    """
    try:
        logger.info(
            "Fetching hyperlocal forecast",
            center_lat=center_lat,
            center_lon=center_lon,
            radius_km=radius_km,
            resolution_km=resolution_km,
        )

        spatial_service = SpatialService(db)
        forecasting_service = ForecastingService(db)

        # Generate spatial grid
        grid_points = spatial_service.generate_grid(
            center_lat, center_lon, radius_km, resolution_km
        )

        # Get forecasts for each grid point
        grid_forecasts = []
        for row in grid_points:
            row_forecasts = []
            for point in row:
                forecast = await forecasting_service.get_point_forecast(
                    point["lat"], point["lon"], hours
                )
                row_forecasts.append(forecast)
            grid_forecasts.append(row_forecasts)

        return HyperLocalForecastResponse(
            center_location=LocationInput(latitude=center_lat, longitude=center_lon),
            grid_size_km=resolution_km,
            grid_forecasts=grid_forecasts,
            timestamp=datetime.utcnow(),
            forecast_horizon_hours=hours,
        )

    except Exception as e:
        logger.error("Error fetching hyperlocal forecast", error=str(e))
        raise HTTPException(
            status_code=500, detail="Failed to fetch hyperlocal forecast"
        )


@router.get("/route")
async def get_route_forecast(
    start_lat: float = Query(..., description="Start latitude"),
    start_lon: float = Query(..., description="Start longitude"),
    end_lat: float = Query(..., description="End latitude"),
    end_lon: float = Query(..., description="End longitude"),
    transport_mode: str = Query(
        "walking", description="Transport mode: walking, cycling, driving"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Get pollution forecast along a specific route

    Provides:
    - Route-specific AQI predictions
    - Transport mode optimization
    - Alternative route suggestions
    - Exposure time calculations
    """
    try:
        logger.info(
            "Fetching route forecast",
            start_lat=start_lat,
            start_lon=start_lon,
            end_lat=end_lat,
            end_lon=end_lon,
            mode=transport_mode,
        )

        spatial_service = SpatialService(db)
        forecasting_service = ForecastingService(db)

        # Get route points
        route_points = await spatial_service.get_route_points(
            start_lat, start_lon, end_lat, end_lon, transport_mode
        )

        # Calculate pollution exposure along route
        route_forecast = await forecasting_service.calculate_route_exposure(
            route_points, transport_mode
        )

        return {
            "route": route_points,
            "pollution_exposure": route_forecast,
            "recommendations": route_forecast.get("recommendations", []),
            "alternative_routes": route_forecast.get("alternatives", []),
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error fetching route forecast", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch route forecast")


@router.get("/historical")
async def get_historical_forecast_accuracy(
    latitude: float = Query(..., description="Latitude coordinate"),
    longitude: float = Query(..., description="Longitude coordinate"),
    days: int = Query(7, ge=1, le=30, description="Number of days to analyze"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get historical forecast accuracy metrics

    Provides:
    - Model performance statistics
    - Prediction vs actual comparisons
    - Accuracy trends over time
    - Model confidence analysis
    """
    try:
        forecasting_service = ForecastingService(db)

        accuracy_metrics = await forecasting_service.get_forecast_accuracy(
            latitude, longitude, days
        )

        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "analysis_period_days": days,
            "accuracy_metrics": accuracy_metrics,
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error fetching forecast accuracy", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch accuracy metrics")
