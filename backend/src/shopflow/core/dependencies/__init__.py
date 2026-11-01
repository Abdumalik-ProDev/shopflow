"""Dependency injection providers."""

from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status

from shopflow.core.database.session import get_session
from shopflow.core.security import decode_token
from shopflow.modules.identity.infrastructure.repositories import SqlAlchemyUserRepository


async def get_current_user_id(
    authorization: Optional[str] = None,
) -> str:
    """Extract and validate user_id from Bearer token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
        )
    token = authorization[len("Bearer "):]
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user id",
        )
    return user_id


async def get_current_user(
    user_id: Annotated[str, Depends(get_current_user_id)],
    session=Depends(get_session),
):
    repo = SqlAlchemyUserRepository(session)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

__all__ = ["get_current_user", "get_current_user_id"]
