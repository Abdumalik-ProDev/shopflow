"""Dependency injection providers."""

from typing import AsyncGenerator

from fastapi import Depends

from shopflow.core.database.session import get_session
from shopflow.core.security import decode_token
from shopflow.modules.identity.infrastructure.repositories import SqlAlchemyUserRepository


async def get_current_user(
    token: str,
    session=Depends(get_session),
):
    payload = decode_token(token)
    if payload is None:
        raise ValueError("Invalid or expired token")
    user_id = payload.get("sub")
    repo = SqlAlchemyUserRepository(session)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise ValueError("User not found")
    return user
