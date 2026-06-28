import sys
import os


import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.schemas.user_schemas import TokenData
from src.utils.require_admin import require_admin


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(
        app=app,
    )

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac


@pytest_asyncio.fixture(autouse=True)
async def override_require_admin():
    # Подменяем зависимость на фиктивный токен
    async def fake_require_admin():
        return TokenData(user_id=1, role="admin", email="admin@admin.com")

    app.dependency_overrides[require_admin] = fake_require_admin
    yield
    app.dependency_overrides.clear()
