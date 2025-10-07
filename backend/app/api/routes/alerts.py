from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
import structlog
from pydantic import BaseModel

from app.database import get_db
from app.services.alert_service import AlertService

logger = structlog.get_logger()

router = APIRouter()


class AlertPreferences(BaseModel):
    user_id: str
    alert_threshold: int = 150  # AQI threshold
    notification_channels: List[str] = ["push", "email"]
    location_based: bool = True
    health_alerts: bool = True
    forecast_alerts: bool = True


@router.post("/preferences")
async def set_alert_preferences(
    preferences: AlertPreferences, db: AsyncSession = Depends(get_db)
):
    """Set user alert preferences and notification settings"""
    try:
        alert_service = AlertService(db)

        result = await alert_service.update_user_preferences(preferences.dict())

        return {
            "status": "success",
            "message": "Alert preferences updated successfully",
            "preferences": result,
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error updating alert preferences", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to update preferences")


@router.get("/active")
async def get_active_alerts(
    latitude: float = Query(..., description="Latitude coordinate"),
    longitude: float = Query(..., description="Longitude coordinate"),
    radius_km: float = Query(10, description="Alert radius in km"),
    db: AsyncSession = Depends(get_db),
):
    """Get all active pollution alerts for a specific area"""
    try:
        alert_service = AlertService(db)

        alerts = await alert_service.get_active_alerts(latitude, longitude, radius_km)

        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "radius_km": radius_km,
            "active_alerts": alerts,
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error fetching active alerts", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch alerts")


@router.get("/user/{user_id}")
async def get_user_alerts(
    user_id: str,
    limit: int = Query(50, description="Maximum number of alerts"),
    db: AsyncSession = Depends(get_db),
):
    """Get personalized alerts for a specific user"""
    try:
        alert_service = AlertService(db)

        user_alerts = await alert_service.get_user_alerts(user_id, limit)

        return {
            "user_id": user_id,
            "alerts": user_alerts,
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error fetching user alerts", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch user alerts")


# Create empty route files for other endpoints
router_content = """from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def placeholder():
    return {"message": "Endpoint under development"}
"""
