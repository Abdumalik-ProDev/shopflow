"""Authentication endpoints tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_and_login_flow(client: AsyncClient):
    # Register
    res = await client.post(
        "/api/auth/register",
        json={
            "email": "alice@example.com",
            "username": "alice",
            "password": "Password123!",
            "full_name": "Alice Wonderland",
            "role": "customer",
        },
    )
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "alice@example.com"
    assert data["username"] == "alice"
    assert "id" in data

    # Duplicate email rejection
    res_dup = await client.post(
        "/api/auth/register",
        json={
            "email": "alice@example.com",
            "username": "alice2",
            "password": "Password123!",
        },
    )
    assert res_dup.status_code == 400

    # Login
    res_login = await client.post(
        "/api/auth/login",
        json={"username": "alice", "password": "Password123!"},
    )
    assert res_login.status_code == 200
    token_data = res_login.json()
    assert "access_token" in token_data

    # Access /api/auth/me
    token = token_data["access_token"]
    res_me = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me.status_code == 200
    me_data = res_me.json()
    assert me_data["username"] == "alice"
    assert me_data["role"] == "customer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    res = await client.post(
        "/api/auth/login",
        json={"username": "nonexistent", "password": "WrongPassword!"},
    )
    assert res.status_code == 401
