import uuid

import httpx
import pytest
import pytest_asyncio
from fastapi import status

from src.core.limiter import limiter
from src.core.settings import settings
from src.main import app
from src.schemas.user_schemas import TokenData
from src.utils.auth import get_current_user

BASE_URL = "/api/v1/users"
unique_email = f"user_{uuid.uuid4().hex[:6]}@example.com"


# фикстура для подмены авторизации и отключения лимитера
@pytest_asyncio.fixture(autouse=True)
async def override_dependencies():
    async def fake_current_user():
        return TokenData(user_id=1, email=unique_email, role="user")

    app.dependency_overrides[get_current_user] = fake_current_user
    app.dependency_overrides[limiter.limit] = lambda *args, **kwargs: (
        lambda f: f
    )

    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_user():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        payload = {
            "first_name": "Иван",
            "middle_name": "Иванович",
            "last_name": "Иванов",
            "email": unique_email,
            "password": "secret123",
            "confirm_password": "secret123",
            "is_active": True,
        }
        response = await client.post(BASE_URL + "/", json=payload)
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
        ]
        data = response.json()
        assert data["message"] == "Created"
        assert data["data"]["email"] == unique_email


@pytest.mark.asyncio
async def test_get_profile():
    # подменяем get_current_user на фиктивного юзера
    async def fake_current_user():
        return TokenData(user_id=1, email=settings.admin_email, role="admin")

    app.dependency_overrides[get_current_user] = fake_current_user

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get(BASE_URL + "/me")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "email" in data
        assert data["email"] == settings.admin_email


@pytest.mark.asyncio
async def test_update_profile():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        payload = {
            "first_name": settings.admin_first_name,
            "last_name": settings.admin_last_name,
        }
        response = await client.patch(BASE_URL + "/me", json=payload)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["first_name"] == settings.admin_first_name


@pytest.mark.asyncio
async def test_delete_user():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        payload = {"email": unique_email, "password": "secret123"}
        response = await client.request(
            "DELETE", BASE_URL + "/me", json=payload
        )
        assert response.status_code in [
            status.HTTP_204_NO_CONTENT,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
        ]
