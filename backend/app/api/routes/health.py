from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
import structlog
from pydantic import BaseModel, Field

from app.database import get_db
from app.services.health_service import HealthService
from app.services.user_service import UserService

logger = structlog.get_logger()

router = APIRouter()


class UserProfile(BaseModel):
    age_group: str = Field(..., description="Age group: child, adult, senior")
    health_conditions: List[str] = Field(default=[], description="Health conditions")
    activity_level: str = Field(..., description="Activity level: low, moderate, high")
    sensitivity_level: str = Field(
        default="normal", description="Pollution sensitivity"
    )


class HealthRecommendationResponse(BaseModel):
    timestamp: datetime
    location: dict
    current_aqi: int
    health_risk_level: str
    personalized_recommendations: List[str]
    activity_guidance: dict
    protective_measures: List[str]
    optimal_times: dict
    route_suggestions: List[str]


class HealthAlert(BaseModel):
    alert_type: str
    severity: str
    message: str
    recommendations: List[str]
    valid_until: datetime


@router.post("/recommendations", response_model=HealthRecommendationResponse)
async def get_personalized_health_recommendations(
    user_profile: UserProfile,
    latitude: float = Query(..., description="Current latitude"),
    longitude: float = Query(..., description="Current longitude"),
    activity_type: Optional[str] = Query(None, description="Planned activity type"),
    duration_hours: Optional[float] = Query(
        None, description="Planned activity duration"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Get personalized health recommendations based on user profile and current pollution

    Provides:
    - Personalized health risk assessment
    - Activity-specific guidance
    - Protective measure recommendations
    - Optimal timing suggestions
    - Route optimization for health
    """
    try:
        logger.info(
            "Generating health recommendations",
            latitude=latitude,
            longitude=longitude,
            age_group=user_profile.age_group,
        )

        health_service = HealthService(db)

        # Get current pollution data
        current_pollution = await health_service.get_current_pollution(
            latitude, longitude
        )

        # Calculate health risk
        health_risk = await health_service.calculate_health_risk(
            user_profile.dict(), current_pollution
        )

        # Generate personalized recommendations
        recommendations = await health_service.generate_recommendations(
            user_profile.dict(), current_pollution, activity_type, duration_hours
        )

        # Get activity guidance
        activity_guidance = await health_service.get_activity_guidance(
            user_profile.dict(), current_pollution, activity_type
        )

        # Get optimal timing
        optimal_times = await health_service.get_optimal_times(
            latitude, longitude, user_profile.dict()
        )

        return HealthRecommendationResponse(
            timestamp=datetime.utcnow(),
            location={"latitude": latitude, "longitude": longitude},
            current_aqi=current_pollution["aqi"],
            health_risk_level=health_risk["level"],
            personalized_recommendations=recommendations["general"],
            activity_guidance=activity_guidance,
            protective_measures=recommendations["protective"],
            optimal_times=optimal_times,
            route_suggestions=recommendations["routes"],
        )

    except Exception as e:
        logger.error("Error generating health recommendations", error=str(e))
        raise HTTPException(
            status_code=500, detail="Failed to generate health recommendations"
        )


@router.get("/risk-assessment")
async def get_health_risk_assessment(
    latitude: float = Query(..., description="Latitude coordinate"),
    longitude: float = Query(..., description="Longitude coordinate"),
    age_group: str = Query(..., description="Age group: child, adult, senior"),
    health_conditions: Optional[str] = Query(
        None, description="Comma-separated health conditions"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Get health risk assessment for current pollution levels

    Provides:
    - Real-time health risk scoring
    - Vulnerable population alerts
    - Exposure time calculations
    - Health impact predictions
    """
    try:
        logger.info(
            "Calculating health risk",
            latitude=latitude,
            longitude=longitude,
            age_group=age_group,
        )

        health_service = HealthService(db)

        # Parse health conditions
        conditions = []
        if health_conditions:
            conditions = [c.strip() for c in health_conditions.split(",")]

        user_profile = {
            "age_group": age_group,
            "health_conditions": conditions,
            "activity_level": "moderate",
        }

        # Get current pollution
        current_pollution = await health_service.get_current_pollution(
            latitude, longitude
        )

        # Calculate detailed risk assessment
        risk_assessment = await health_service.detailed_risk_assessment(
            user_profile, current_pollution
        )

        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "current_pollution": current_pollution,
            "risk_assessment": risk_assessment,
            "vulnerability_factors": risk_assessment["factors"],
            "exposure_limits": risk_assessment["limits"],
            "health_impacts": risk_assessment["impacts"],
            "recommendations": risk_assessment["recommendations"],
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error calculating health risk", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to calculate health risk")


@router.get("/alerts")
async def get_health_alerts(
    latitude: float = Query(..., description="Latitude coordinate"),
    longitude: float = Query(..., description="Longitude coordinate"),
    radius_km: float = Query(10, description="Alert radius in km"),
    user_id: Optional[str] = Query(None, description="User ID for personalized alerts"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get health alerts for current and forecasted pollution levels

    Provides:
    - Emergency health alerts
    - Vulnerable population warnings
    - Proactive health notifications
    - Personalized alert thresholds
    """
    try:
        logger.info(
            "Fetching health alerts",
            latitude=latitude,
            longitude=longitude,
            user_id=user_id,
        )

        health_service = HealthService(db)
        user_service = UserService(db)

        # Get user profile if provided
        user_profile = None
        if user_id:
            user_profile = await user_service.get_user_profile(user_id)

        # Get current and forecasted pollution
        pollution_data = await health_service.get_pollution_forecast(
            latitude, longitude, 24  # 24-hour forecast
        )

        # Generate health alerts
        alerts = await health_service.generate_health_alerts(
            pollution_data, user_profile, radius_km
        )

        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "alert_radius_km": radius_km,
            "active_alerts": alerts["active"],
            "upcoming_alerts": alerts["upcoming"],
            "severity_levels": alerts["severity_breakdown"],
            "affected_areas": alerts["affected_areas"],
            "recommendations": alerts["recommendations"],
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error fetching health alerts", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch health alerts")


@router.get("/exposure-tracking")
async def get_exposure_tracking(
    user_id: str = Query(..., description="User ID"),
    days: int = Query(7, ge=1, le=30, description="Number of days to analyze"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get pollution exposure tracking and health impact analysis

    Provides:
    - Daily exposure summaries
    - Cumulative health impact
    - Exposure pattern analysis
    - Health improvement suggestions
    """
    try:
        logger.info("Fetching exposure tracking", user_id=user_id, days=days)

        health_service = HealthService(db)
        user_service = UserService(db)

        # Get user profile and location history
        user_data = await user_service.get_user_with_locations(user_id, days)

        # Calculate exposure tracking
        exposure_analysis = await health_service.calculate_exposure_tracking(
            user_data, days
        )

        return {
            "user_id": user_id,
            "analysis_period_days": days,
            "daily_exposures": exposure_analysis["daily"],
            "cumulative_exposure": exposure_analysis["cumulative"],
            "health_impact_score": exposure_analysis["impact_score"],
            "exposure_patterns": exposure_analysis["patterns"],
            "recommendations": exposure_analysis["recommendations"],
            "improvement_suggestions": exposure_analysis["improvements"],
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error fetching exposure tracking", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch exposure tracking")


@router.get("/safe-routes")
async def get_safe_routes(
    start_lat: float = Query(..., description="Start latitude"),
    start_lon: float = Query(..., description="Start longitude"),
    end_lat: float = Query(..., description="End latitude"),
    end_lon: float = Query(..., description="End longitude"),
    transport_mode: str = Query("walking", description="Transport mode"),
    health_priority: str = Query(
        "medium", description="Health priority: low, medium, high"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Get health-optimized route recommendations

    Provides:
    - Pollution-aware route planning
    - Health-optimized path selection
    - Exposure minimization
    - Alternative route comparisons
    """
    try:
        logger.info(
            "Generating safe routes",
            start_lat=start_lat,
            start_lon=start_lon,
            end_lat=end_lat,
            end_lon=end_lon,
        )

        health_service = HealthService(db)

        # Generate health-optimized routes
        safe_routes = await health_service.generate_safe_routes(
            start_lat, start_lon, end_lat, end_lon, transport_mode, health_priority
        )

        return {
            "start_location": {"latitude": start_lat, "longitude": start_lon},
            "end_location": {"latitude": end_lat, "longitude": end_lon},
            "transport_mode": transport_mode,
            "health_priority": health_priority,
            "recommended_routes": safe_routes["routes"],
            "exposure_comparison": safe_routes["exposure_analysis"],
            "health_scores": safe_routes["health_scores"],
            "timing_recommendations": safe_routes["timing"],
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error generating safe routes", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate safe routes")
