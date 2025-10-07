from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
import random
from datetime import datetime


class SourceAttributionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_current_pollution_data(
        self, lat: float, lon: float
    ) -> Dict[str, Any]:
        aqi = random.randint(60, 280)
        return {
            "aqi": aqi,
            "pm2_5": round(random.uniform(25, 180), 1),
            "pm10": round(random.uniform(60, 300), 1),
            "category": (
                "Good"
                if aqi <= 50
                else (
                    "Satisfactory"
                    if aqi <= 100
                    else (
                        "Moderate"
                        if aqi <= 200
                        else (
                            "Poor"
                            if aqi <= 300
                            else "Very Poor" if aqi <= 400 else "Severe"
                        )
                    )
                )
            ),
        }

    async def analyze_pollution_sources(
        self, lat: float, lon: float, pollution: Dict[str, Any]
    ) -> Dict[str, Any]:
        sources = [
            {
                "source_type": "stubble_burning",
                "contribution_percentage": round(random.uniform(10, 50), 2),
                "confidence_score": 0.8,
                "description": "Agricultural residue burning",
            },
            {
                "source_type": "vehicular",
                "contribution_percentage": round(random.uniform(15, 40), 2),
                "confidence_score": 0.85,
                "description": "Traffic emissions",
            },
            {
                "source_type": "industrial",
                "contribution_percentage": round(random.uniform(5, 30), 2),
                "confidence_score": 0.75,
                "description": "Industrial activities",
            },
            {
                "source_type": "dust_and_construction",
                "contribution_percentage": round(random.uniform(5, 30), 2),
                "confidence_score": 0.7,
                "description": "Construction and road dust",
            },
            {
                "source_type": "biomass_burning",
                "contribution_percentage": round(random.uniform(0, 15), 2),
                "confidence_score": 0.65,
                "description": "Biomass burning",
            },
        ]
        sources.sort(key=lambda s: s["contribution_percentage"], reverse=True)
        dominant = sources[0]["source_type"]
        return {"sources": sources, "dominant_source": dominant, "confidence": 0.82}

    async def get_pollution_trend(
        self, lat: float, lon: float, hours: int
    ) -> Dict[str, Any]:
        return {
            "trend_direction": random.choice(["increasing", "decreasing", "stable"])
        }

    async def generate_source_recommendations(
        self, source_analysis: Dict[str, Any], pollution: Dict[str, Any]
    ):
        return [
            "Avoid burning of waste and residues",
            "Use public transport or carpool",
            "Water sprinkling in construction areas",
        ]

    async def generate_regional_source_map(
        self,
        center_lat: float,
        center_lon: float,
        radius_km: float,
        resolution_km: float,
    ) -> Dict[str, Any]:
        # Placeholder structure
        return {
            "source_grid": [],
            "hotspots": [],
            "area_sources": {},
            "boundary_analysis": {},
        }

    async def analyze_fire_impact(
        self, lat: float, lon: float, radius_km: float, days: int
    ) -> Dict[str, Any]:
        return {
            "active_fires": random.randint(0, 50),
            "impact_score": round(random.uniform(0, 1), 2),
            "correlation": round(random.uniform(0.2, 0.8), 2),
            "wind_analysis": {},
            "stubble_contribution": round(random.uniform(0, 0.5), 2),
            "recommendations": ["Increase monitoring during harvest season"],
        }

    async def get_model_validation(
        self, region: str, model_version: str | None
    ) -> Dict[str, Any]:
        return {
            "model_version": model_version or "rf-gmm-0.1",
            "metrics": {"accuracy": 0.82, "precision": 0.8, "recall": 0.78},
            "source_accuracy": {"stubble_burning": 0.85, "vehicular": 0.8},
            "trends": {},
            "recommendations": ["Collect more labeled data for industrial sources"],
            "last_validation": datetime.utcnow().isoformat() + "Z",
        }

    async def analyze_source_trends(
        self, lat: float, lon: float, time_delta
    ) -> Dict[str, Any]:
        """Placeholder trend analysis producing synthetic time series and seasonal pattern stubs."""
        import math

        points = 24 if time_delta.days <= 1 else min(time_delta.days * 8, 200)
        base_time = datetime.utcnow()
        time_series = []
        for i in range(points):
            ts = base_time - (time_delta / points) * i
            time_series.append(
                {
                    "timestamp": ts.isoformat() + "Z",
                    "stubble_burning": round(random.uniform(5, 40), 2),
                    "vehicular": round(random.uniform(10, 45), 2),
                    "industrial": round(random.uniform(5, 30), 2),
                    "dust_and_construction": round(random.uniform(5, 25), 2),
                    "biomass_burning": round(random.uniform(0, 15), 2),
                }
            )
        seasonal = {
            "monthly": {str(m): random.uniform(10, 40) for m in range(1, 13)},
            "weekly_pattern": [random.uniform(10, 35) for _ in range(7)],
        }
        anomalies = []
        if random.random() > 0.7:
            anomalies.append(
                {
                    "timestamp": (base_time - time_delta / 3).isoformat() + "Z",
                    "source": "stubble_burning",
                    "deviation_pct": 65.0,
                    "severity": "high",
                }
            )
        return {
            "time_series": list(reversed(time_series)),
            "seasonal": seasonal,
            "anomalies": anomalies,
        }
