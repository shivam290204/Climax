from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List


class AlertService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_user_preferences(
        self, preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        return preferences

    async def get_active_alerts(
        self, lat: float, lon: float, radius_km: float
    ) -> List[Dict[str, Any]]:
        return []

    async def get_user_alerts(self, user_id: str, limit: int) -> List[Dict[str, Any]]:
        return []
