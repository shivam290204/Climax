from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
import structlog
from pydantic import BaseModel, Field

from app.database import get_db
from app.services.policy_service import PolicyService

logger = structlog.get_logger()

router = APIRouter()


class PolicyIntervention(BaseModel):
    intervention_type: str = Field(..., description="Type of intervention")
    parameters: dict = Field(..., description="Intervention parameters")
    affected_areas: List[dict] = Field(..., description="Geographic areas affected")
    duration_days: int = Field(..., description="Duration in days")


class PolicyImpactResponse(BaseModel):
    intervention: PolicyIntervention
    predicted_impact: dict
    cost_benefit_analysis: dict
    implementation_timeline: dict
    success_probability: float
    recommendations: List[str]


@router.post("/simulate", response_model=PolicyImpactResponse)
async def simulate_policy_impact(
    intervention: PolicyIntervention, db: AsyncSession = Depends(get_db)
):
    """
    Simulate the impact of pollution control policy interventions

    Supported interventions:
    - Odd-even vehicle restrictions
    - Construction activity bans
    - Industrial emission controls
    - Emergency response measures
    - Stubble burning prevention
    """
    try:
        logger.info(
            "Simulating policy impact", intervention_type=intervention.intervention_type
        )

        policy_service = PolicyService(db)

        # Validate intervention parameters
        validation_result = await policy_service.validate_intervention(
            intervention.dict()
        )
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["errors"])

        # Run Monte Carlo simulation
        impact_simulation = await policy_service.simulate_intervention_impact(
            intervention.dict()
        )

        # Calculate cost-benefit analysis
        cost_benefit = await policy_service.calculate_cost_benefit(
            intervention.dict(), impact_simulation
        )

        # Generate implementation timeline
        timeline = await policy_service.generate_implementation_timeline(
            intervention.dict()
        )

        # Calculate success probability
        success_prob = await policy_service.calculate_success_probability(
            intervention.dict(), impact_simulation
        )

        return PolicyImpactResponse(
            intervention=intervention,
            predicted_impact=impact_simulation,
            cost_benefit_analysis=cost_benefit,
            implementation_timeline=timeline,
            success_probability=success_prob,
            recommendations=impact_simulation.get("recommendations", []),
        )

    except Exception as e:
        logger.error("Error simulating policy impact", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to simulate policy impact")


@router.get("/historical-effectiveness")
async def get_historical_policy_effectiveness(
    intervention_type: Optional[str] = Query(
        None, description="Filter by intervention type"
    ),
    region: str = Query("delhi-ncr", description="Geographic region"),
    years: int = Query(5, ge=1, le=10, description="Years of historical data"),
    db: AsyncSession = Depends(get_db),
):
    """
    Analyze historical effectiveness of pollution control policies

    Provides:
    - Past intervention performance data
    - Success rate analysis
    - Effectiveness by intervention type
    - Lessons learned and recommendations
    """
    try:
        logger.info(
            "Fetching historical effectiveness",
            intervention_type=intervention_type,
            region=region,
        )

        policy_service = PolicyService(db)

        effectiveness_analysis = await policy_service.analyze_historical_effectiveness(
            intervention_type, region, years
        )

        return {
            "region": region,
            "analysis_period_years": years,
            "intervention_filter": intervention_type,
            "overall_statistics": effectiveness_analysis["overall"],
            "by_intervention_type": effectiveness_analysis["by_type"],
            "success_factors": effectiveness_analysis["success_factors"],
            "failure_factors": effectiveness_analysis["failure_factors"],
            "recommendations": effectiveness_analysis["recommendations"],
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error fetching historical effectiveness", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch historical data")


@router.get("/recommendations")
async def get_policy_recommendations(
    current_aqi: int = Query(..., ge=0, le=500, description="Current AQI level"),
    forecast_days: int = Query(3, ge=1, le=7, description="Forecast period"),
    priority: str = Query("health", description="Priority: health, economy, balanced"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get AI-powered policy recommendations based on current and forecasted pollution

    Provides:
    - Proactive intervention suggestions
    - Priority-based recommendations
    - Evidence-based policy options
    - Implementation urgency assessment
    """
    try:
        logger.info(
            "Generating policy recommendations",
            current_aqi=current_aqi,
            priority=priority,
        )

        policy_service = PolicyService(db)

        # Get current pollution context
        pollution_context = await policy_service.get_pollution_context(
            current_aqi, forecast_days
        )

        # Generate recommendations
        recommendations = await policy_service.generate_recommendations(
            pollution_context, priority
        )

        return {
            "current_aqi": current_aqi,
            "forecast_period_days": forecast_days,
            "priority_focus": priority,
            "urgency_level": recommendations["urgency"],
            "recommended_interventions": recommendations["interventions"],
            "implementation_order": recommendations["sequence"],
            "expected_outcomes": recommendations["outcomes"],
            "resource_requirements": recommendations["resources"],
            "timeline": recommendations["timeline"],
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error generating recommendations", error=str(e))
        raise HTTPException(
            status_code=500, detail="Failed to generate recommendations"
        )


@router.get("/ongoing-interventions")
async def get_ongoing_interventions(
    region: str = Query("delhi-ncr", description="Geographic region"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get status of currently active pollution control interventions

    Provides:
    - Active intervention monitoring
    - Real-time effectiveness tracking
    - Performance metrics
    - Adjustment recommendations
    """
    try:
        logger.info("Fetching ongoing interventions", region=region)

        policy_service = PolicyService(db)

        ongoing_analysis = await policy_service.monitor_ongoing_interventions(region)

        return {
            "region": region,
            "active_interventions": ongoing_analysis["active"],
            "performance_metrics": ongoing_analysis["metrics"],
            "effectiveness_scores": ongoing_analysis["effectiveness"],
            "adjustment_recommendations": ongoing_analysis["adjustments"],
            "early_termination_candidates": ongoing_analysis["termination_candidates"],
            "extension_recommendations": ongoing_analysis["extensions"],
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error fetching ongoing interventions", error=str(e))
        raise HTTPException(
            status_code=500, detail="Failed to fetch ongoing interventions"
        )


@router.post("/emergency-response")
async def trigger_emergency_response(
    aqi_level: int = Query(..., description="Current AQI triggering emergency"),
    affected_areas: List[str] = Query(..., description="List of affected area codes"),
    duration_hours: int = Query(
        24, description="Expected duration of emergency measures"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Generate emergency response plan for severe pollution events

    Provides:
    - Immediate action recommendations
    - Emergency intervention protocols
    - Public health measures
    - Communication strategies
    """
    try:
        logger.info(
            "Generating emergency response",
            aqi_level=aqi_level,
            affected_areas=affected_areas,
        )

        policy_service = PolicyService(db)

        # Generate emergency response plan
        emergency_plan = await policy_service.generate_emergency_response(
            aqi_level, affected_areas, duration_hours
        )

        return {
            "emergency_level": emergency_plan["level"],
            "trigger_aqi": aqi_level,
            "affected_areas": affected_areas,
            "immediate_actions": emergency_plan["immediate"],
            "short_term_measures": emergency_plan["short_term"],
            "long_term_strategies": emergency_plan["long_term"],
            "public_health_advisories": emergency_plan["health"],
            "communication_plan": emergency_plan["communication"],
            "resource_mobilization": emergency_plan["resources"],
            "success_metrics": emergency_plan["metrics"],
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error generating emergency response", error=str(e))
        raise HTTPException(
            status_code=500, detail="Failed to generate emergency response"
        )


@router.get("/cost-benefit-analysis")
async def get_comprehensive_cost_benefit_analysis(
    intervention_types: List[str] = Query(
        ..., description="List of intervention types to compare"
    ),
    budget_limit: Optional[float] = Query(
        None, description="Budget constraint in crores"
    ),
    time_horizon_years: int = Query(5, description="Analysis time horizon"),
    db: AsyncSession = Depends(get_db),
):
    """
    Comprehensive cost-benefit analysis for multiple policy options

    Provides:
    - Multi-intervention comparison
    - Budget optimization
    - ROI analysis
    - Long-term impact assessment
    """
    try:
        logger.info(
            "Performing cost-benefit analysis",
            interventions=intervention_types,
            budget=budget_limit,
        )

        policy_service = PolicyService(db)

        # Perform comprehensive analysis
        analysis = await policy_service.comprehensive_cost_benefit_analysis(
            intervention_types, budget_limit, time_horizon_years
        )

        return {
            "intervention_types": intervention_types,
            "budget_limit_crores": budget_limit,
            "time_horizon_years": time_horizon_years,
            "cost_analysis": analysis["costs"],
            "benefit_analysis": analysis["benefits"],
            "roi_comparison": analysis["roi"],
            "optimal_portfolio": analysis["optimal"],
            "sensitivity_analysis": analysis["sensitivity"],
            "risk_assessment": analysis["risks"],
            "recommendations": analysis["recommendations"],
            "timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error("Error performing cost-benefit analysis", error=str(e))
        raise HTTPException(
            status_code=500, detail="Failed to perform cost-benefit analysis"
        )
