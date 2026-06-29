import uuid
import pytest
import httpx
from fastapi import status
from src.main import app
from src.core.settings import settings

BASE_URL = "/api/v1/profiles"

@pytest.mark.asyncio
async def test_login_success():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        login_payload = {"email": settings.admin_email, "password": settings.admin_password}
        resp_login = await client.post(BASE_URL + "/", json=login_payload)
        assert resp_login.status_code == status.HTTP_200_OK
        data = resp_login.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_password():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "email": settings.admin_email,
            "password": "secret123",
        }
        await client.post("/api/v1/users/", json=payload)

        # пробуем неправильный пароль
        login_payload = {"email": settings.admin_email, "password": "wrongpass"}
        resp_login = await client.post(BASE_URL + "/", json=login_payload)
        assert resp_login.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_logout():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # делаем логаут
        resp_logout = await client.delete(BASE_URL + "/")
        assert resp_logout.status_code == status.HTTP_204_NO_CONTENT
        # проверяем что cookie удалено
        assert "jwt" not in resp_logout.cookies
