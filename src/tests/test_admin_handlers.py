import random
import pytest
import httpx
from fastapi import status
from src.main import app

"""
Тесты e2e
"""

BASE_URL = "/api/v1/admin/users"
user_count = 0
email = random.randint(100000, 999999) # для уникального email

@pytest.mark.asyncio
async def test_create_user():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "first_name": "Иван",
            "middle_name": "Иванович",
            "last_name": "Иванов",
            "email": f"{email}@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
            "role": "user",
        }

        response = await client.post(BASE_URL + "/", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["message"] == "create success"
        assert data["data"]["email"] == f"{email}@example.com"


@pytest.mark.asyncio
async def test_get_users():
    transport = httpx.ASGITransport(app=app)
    global user_count
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(BASE_URL + "/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        user_count = len(data)
        print("user count", user_count)
        assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_user_by_id():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(BASE_URL + "/1")
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert "email" in data
        else:
            assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_user():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "user_id": 1,
            "first_name": "Петр",
            "last_name": "Петров",
            "role": "admin",
            "is_active": True
        }
        response = await client.patch(BASE_URL + "/", json=payload)
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert data["message"] == "update success"
            assert data["data"]["first_name"] == "Петр"
        else:
            assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]


@pytest.mark.asyncio
async def test_delete_user():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete(BASE_URL + f"/{user_count}")
        assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND]
