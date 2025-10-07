from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, timedelta
import structlog
from pydantic import BaseModel, Field

from app.database import get_db
from app.services.source_attribution_service import SourceAttributionService

logger = structlog.get_logger()

router = APIRouter()


class SourceContribution(BaseModel):
    source_type: str
    contribution_percentage: float
    confidence_score: float
    description: str


class SourceAttributionResponse(BaseModel):
    timestamp: datetime
    location: dict
    total_pollution_level: dict
    source_breakdown: List[SourceContribution]
    dominant_source: str
    pollution_trend: str
    model_confidence: float
    recommendations: List[str]


class SourceTrendResponse(BaseModel):
    location: dict
    time_period: str
    trend_data: List[dict]
    seasonal_patterns: dict
    anomalies: List[dict]


@router.get("/current", response_model=SourceAttributionResponse)
async def get_current_source_attribution(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude coordinate"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude coordinate"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get real-time pollution source attribution for a specific location

    Uses AI models to identify pollution sources:
    - Stubble burning detection
    - Vehicular emissions analysis
    - Industrial source identification
    - Construction dust assessment
    - Biomass burning detection
    """
    try:
        logger.info(
            "Fetching source attribution", latitude=latitude, longitude=longitude
        )

        source_service = SourceAttributionService(db)

        # Get current pollution levels
        current_pollution = await source_service.get_current_pollution_data(
            latitude, longitude
        )

        # Perform source attribution analysis
        source_analysis = await source_service.analyze_pollution_sources(
            latitude, longitude, current_pollution
        )

        # Get trend information
        trend_analysis = await source_service.get_pollution_trend(
            latitude, longitude, hours=24
        )

        # Generate recommendations
        recommendations = await source_service.generate_source_recommendations(
            source_analysis, current_pollution
        )

        return SourceAttributionResponse(
            timestamp=datetime.utcnow(),
            location={"latitude": latitude, "longitude": longitude},
            total_pollution_level={
                "aqi": current_pollution["aqi"],
                "pm2_5": current_pollution["pm2_5"],
                "pm10": current_pollution["pm10"],
                "category": current_pollution["category"],
            },
            source_breakdown=source_analysis["sources"],
            dominant_source=source_analysis["dominant_source"],
            pollution_trend=trend_analysis["trend_direction"],
            model_confidence=source_analysis["confidence"],
            recommendations=recommendations,
        )

    except Exception as e:
        logger.error("Error fetching source attribution", error=str(e))
        raise HTTPException(
            status_code=500, detail="Failed to fetch source attribution"
        )


@router.get("/regional")
async def get_regional_source_map(
    center_lat: float = Query(..., description="Center latitude"),
    center_lon: float = Query(..., description="Center longitude"),
    radius_km: float = Query(20, ge=5, le=100, description="Analysis radius in km"),
    resolution_km: float = Query(2, ge=1, le=10, description="Grid resolution in km"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get regional source attribution map for Delhi-NCR area

    Provides:
    - Spatial distribution of pollution sources
    - Hotspot identification
    - Source-specific heat maps
    - Cross-boundary pollution analysis
    """
    try:
        logger.info(
            "Fetching regional source map",
            center_lat=center_lat,
            center_lon=center_lon,
            radius_km=radius_km,
        )

        source_service = SourceAttributionService(db)

        # Generate analysis grid
        grid_analysis = await source_service.generate_regional_source_map(
            center_lat, center_lon, radius_km, resolution_km
        )

        return {
            "center_location": {"latitude": center_lat, "longitude": center_lon},
            "analysis_radius_km": radius_km,
            "grid_resolution_km": resolution_km,
            "source_map": grid_analysis["source_grid"],
            "hotspots": grid_analysis["hotspots"],
            "dominant_sources_by_area": grid_analysis["area_sources"],
            "cross_boundary_analysis": grid_analysis["boundary_analysis"],
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error fetching regional source map", error=str(e))
        raise HTTPException(
            status_code=500, detail="Failed to fetch regional source map"
        )


@router.get("/trends", response_model=SourceTrendResponse)
async def get_source_trends(
    latitude: float = Query(..., description="Latitude coordinate"),
    longitude: float = Query(..., description="Longitude coordinate"),
    period: str = Query("7d", description="Analysis period: 1d, 7d, 30d, 1y"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get historical trends in pollution source contributions

    Provides:
    - Time-series analysis of source contributions
    - Seasonal variation patterns
    - Anomaly detection
    - Source evolution trends
    """
    try:
        logger.info(
            "Fetching source trends",
            latitude=latitude,
            longitude=longitude,
            period=period,
        )

        source_service = SourceAttributionService(db)

        # Parse time period
        period_mapping = {
            "1d": timedelta(days=1),
            "7d": timedelta(days=7),
            "30d": timedelta(days=30),
            "1y": timedelta(days=365),
        }

        time_delta = period_mapping.get(period, timedelta(days=7))

        # Get trend analysis
        trend_data = await source_service.analyze_source_trends(
            latitude, longitude, time_delta
        )

        return SourceTrendResponse(
            location={"latitude": latitude, "longitude": longitude},
            time_period=period,
            trend_data=trend_data["time_series"],
            seasonal_patterns=trend_data["seasonal"],
            anomalies=trend_data["anomalies"],
        )

    except Exception as e:
        logger.error("Error fetching source trends", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch source trends")


@router.get("/fires")
async def get_fire_impact_analysis(
    latitude: float = Query(..., description="Latitude coordinate"),
    longitude: float = Query(..., description="Longitude coordinate"),
    radius_km: float = Query(50, ge=10, le=200, description="Analysis radius in km"),
    days: int = Query(7, ge=1, le=30, description="Number of days to analyze"),
    db: AsyncSession = Depends(get_db),
):
    """
    Analyze fire hotspot impact on local pollution levels

    Uses NASA FIRMS fire data to:
    - Identify nearby fire hotspots
    - Calculate fire impact on AQI
    - Predict stubble burning contribution
    - Assess wind-driven pollution transport
    """
    try:
        logger.info(
            "Fetching fire impact analysis",
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            days=days,
        )

        source_service = SourceAttributionService(db)

        # Get fire hotspot data
        fire_analysis = await source_service.analyze_fire_impact(
            latitude, longitude, radius_km, days
        )

        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "analysis_radius_km": radius_km,
            "analysis_period_days": days,
            "active_fires": fire_analysis["active_fires"],
            "fire_impact_score": fire_analysis["impact_score"],
            "pollution_correlation": fire_analysis["correlation"],
            "wind_transport_analysis": fire_analysis["wind_analysis"],
            "stubble_burning_contribution": fire_analysis["stubble_contribution"],
            "recommendations": fire_analysis["recommendations"],
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error fetching fire impact analysis", error=str(e))
        raise HTTPException(
            status_code=500, detail="Failed to fetch fire impact analysis"
        )


@router.get("/validation")
async def get_source_model_validation(
    region: str = Query("delhi-ncr", description="Region for validation"),
    model_version: Optional[str] = Query(None, description="Specific model version"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get source attribution model validation metrics

    Provides:
    - Model accuracy statistics
    - Validation against ground truth data
    - Performance by source type
    - Model improvement recommendations
    """
    try:
        logger.info(
            "Fetching model validation", region=region, model_version=model_version
        )

        source_service = SourceAttributionService(db)

        validation_results = await source_service.get_model_validation(
            region, model_version
        )

        return {
            "region": region,
            "model_version": validation_results["model_version"],
            "validation_metrics": validation_results["metrics"],
            "accuracy_by_source": validation_results["source_accuracy"],
            "performance_trends": validation_results["trends"],
            "recommendations": validation_results["recommendations"],
            "last_validation": validation_results["last_validation"],
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error fetching model validation", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch model validation")
