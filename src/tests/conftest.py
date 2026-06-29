import sys
import os

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.schemas.user_schemas import TokenData
from src.utils.require_admin import require_admin
from src.utils.auth import get_current_user

from src.core.limiter import limiter
from src.tests.test_user_handlers import unique_email


app.dependency_overrides[get_current_user] = lambda: TokenData(
    user_id=1, email="test_user@example.com", role="user"
)


@pytest_asyncio.fixture(autouse=True)
async def disable_rate_limit():
    # подменяем limiter.limit на пустой декоратор
    def fake_limit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper

    limiter.limit = fake_limit
    yield
    # можно вернуть обратно, если нужно


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
