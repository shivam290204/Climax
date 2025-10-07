from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List
import random


class HealthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_current_pollution(self, lat: float, lon: float) -> Dict[str, Any]:
        aqi = random.randint(60, 280)
        return {
            "aqi": aqi,
            "pm2_5": random.uniform(25, 180),
            "pm10": random.uniform(60, 300),
        }

    async def calculate_health_risk(
        self, user_profile: Dict[str, Any], pollution: Dict[str, Any]
    ) -> Dict[str, Any]:
        level = "moderate" if pollution["aqi"] < 200 else "high"
        return {"level": level}

    async def generate_recommendations(
        self,
        user_profile: Dict[str, Any],
        pollution: Dict[str, Any],
        activity_type: str | None,
        duration_hours: float | None,
    ) -> Dict[str, List[str]]:
        general = ["Limit outdoor activity if AQI > 200", "Use N95 mask outdoors"]
        routes = ["Take park road to reduce exposure"]
        protective = ["Carry inhaler if asthmatic"]
        return {"general": general, "routes": routes, "protective": protective}

    async def get_activity_guidance(
        self,
        user_profile: Dict[str, Any],
        pollution: Dict[str, Any],
        activity_type: str | None,
    ) -> Dict[str, Any]:
        return {
            "activity": activity_type or "general",
            "advice": "Prefer indoor activities if AQI > 200",
        }

    async def get_optimal_times(
        self, lat: float, lon: float, user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {"best": ["6-8 AM"], "avoid": ["5-9 PM"]}

    async def get_pollution_forecast(
        self, lat: float, lon: float, hours: int
    ) -> Dict[str, Any]:
        return {"hourly": [random.randint(50, 250) for _ in range(hours)]}

    async def generate_health_alerts(
        self,
        pollution_data: Dict[str, Any],
        user_profile: Dict[str, Any] | None,
        radius_km: float,
    ) -> Dict[str, Any]:
        return {
            "active": [],
            "upcoming": [],
            "severity_breakdown": {},
            "affected_areas": [],
            "recommendations": [],
        }

    async def detailed_risk_assessment(
        self, user_profile: Dict[str, Any], pollution: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Return a structured risk assessment matching fields expected by /health/risk-assessment route.

        Placeholder logic:
        - Factors: derive simple vulnerability indicators
        - Limits: mock safe exposure windows
        - Impacts: simplistic mapping from AQI level
        - Recommendations: reuse some from general guidance
        """
        aqi = pollution.get("aqi", 150)
        level = "low"
        if aqi >= 200:
            level = "high"
        elif aqi >= 150:
            level = "moderate"
        factors = []
        if "asthma" in (user_profile.get("health_conditions") or []):
            factors.append("asthma_sensitivity")
        if user_profile.get("age_group") == "senior":
            factors.append("age_related_vulnerability")
        impacts = [
            {
                "type": "respiratory",
                "likelihood": "elevated" if aqi > 180 else "baseline",
            },
            {"type": "cardio", "likelihood": "moderate" if aqi > 200 else "low"},
        ]
        limits = {
            "outdoor_activity_minutes": 30 if aqi > 200 else 120,
            "intense_exercise_minutes": 10 if aqi > 200 else 45,
        }
        recommendations = [
            "Monitor symptoms",
            "Use N95 mask outdoors if AQI > 200",
            "Prefer early morning outdoor tasks",
        ]
        return {
            "level": level,
            "factors": factors,
            "limits": limits,
            "impacts": impacts,
            "recommendations": recommendations,
        }

    async def calculate_exposure_tracking(
        self, user_data: Dict[str, Any], days: int
    ) -> Dict[str, Any]:
        return {
            "daily": [],
            "cumulative": 0,
            "impact_score": 0.5,
            "patterns": {},
            "recommendations": [],
            "improvements": [],
        }

    async def generate_safe_routes(
        self,
        start_lat: float,
        start_lon: float,
        end_lat: float,
        end_lon: float,
        mode: str,
        priority: str,
    ) -> Dict[str, Any]:
        return {
            "routes": [],
            "exposure_analysis": {},
            "health_scores": {},
            "timing": {},
        }
