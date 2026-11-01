"""Identity API controllers."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from shopflow.core.database.session import get_session
from shopflow.core.security import create_access_token, hash_password, verify_password
from shopflow.modules.identity.api.schemas.auth import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from shopflow.modules.identity.domain.models.user import User
from shopflow.modules.identity.infrastructure.repositories import SqlAlchemyUserRepository
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserRegisterRequest,
    session: AsyncSession = Depends(get_session),
):
    repo = SqlAlchemyUserRepository(session)
    if await repo.exists_by_email(payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if await repo.exists_by_username(payload.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(
        email=payload.email,
        username=payload.username,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
    )
    await repo.add(user)
    await session.commit()
    await session.refresh_user(user) if hasattr(session, "refresh_user") else None
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: UserLoginRequest,
    session: AsyncSession = Depends(get_session),
):
    repo = SqlAlchemyUserRepository(session)
    user = await repo.get_by_username(payload.username)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account inactive")
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)


__all__ = ["router"]
