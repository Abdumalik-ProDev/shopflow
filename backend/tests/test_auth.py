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

    # Login by username
    res_login = await client.post(
        "/api/auth/login",
        json={"username": "alice", "password": "Password123!"},
    )
    assert res_login.status_code == 200
    token_data = res_login.json()
    assert "access_token" in token_data
    assert token_data["user"]["username"] == "alice"

    # Login by email address
    res_email_login = await client.post(
        "/api/auth/login",
        json={"username": "alice@example.com", "password": "Password123!"},
    )
    assert res_email_login.status_code == 200
    assert "access_token" in res_email_login.json()

    # Access /api/auth/me
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    res_me = await client.get("/api/auth/me", headers=headers)
    assert res_me.status_code == 200
    me_data = res_me.json()
    assert me_data["username"] == "alice"
    assert me_data["role"] == "customer"

    # Auto-provisioned customer profile lookup by user_id
    res_cust = await client.get(f"/api/customers/{me_data['id']}", headers=headers)
    assert res_cust.status_code == 200
    assert res_cust.json()["customer_unique_id"] == "alice"

    # Change password
    res_pw = await client.post(
        "/api/auth/change-password",
        headers=headers,
        json={"current_password": "Password123!", "new_password": "NewPassword456!"},
    )
    assert res_pw.status_code == 200

    # Login with new password
    res_new_login = await client.post(
        "/api/auth/login",
        json={"username": "alice@example.com", "password": "NewPassword456!"},
    )
    assert res_new_login.status_code == 200


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    res = await client.post(
        "/api/auth/login",
        json={"username": "nonexistent", "password": "WrongPassword!"},
    )
    assert res.status_code == 401
