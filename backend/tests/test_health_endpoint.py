import pytest
from httpx import AsyncClient
from fastapi import status

import os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.append(str(ROOT / "backend"))

from app.main import app  # noqa: E402


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(base_url="http://test") as ac:
        resp = await ac.get("/health")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data.get("status") == "ok"
