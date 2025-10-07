from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        # Placeholder: Fetch from DB
        return {
            "id": user_id,
            "age_group": "adult",
            "health_conditions": ["asthma"],
            "activity_level": "moderate",
        }

    async def get_user_with_locations(self, user_id: str, days: int) -> Dict[str, Any]:
        return {"user": await self.get_user_profile(user_id), "locations": []}
