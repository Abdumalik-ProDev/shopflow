"""Identity API controllers (thin - delegate to service)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.core.security import create_access_token
from shopflow.core.dependencies import get_current_user
from shopflow.modules.identity.api.schemas.auth import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from shopflow.modules.identity.application.services.user import AuthService, UserService
from shopflow.modules.identity.infrastructure.repositories import SqlAlchemyUserRepository

router = APIRouter(prefix="/auth", tags=["auth"])


def _user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(SqlAlchemyUserRepository(session))


def _auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(SqlAlchemyUserRepository(session))


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserRegisterRequest,
    service: UserService = Depends(_user_service),
    session: AsyncSession = Depends(get_session),
):
    user = await service.register(payload)
    await session.commit()
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: UserLoginRequest,
    service: AuthService = Depends(_auth_service),
):
    user = await service.authenticate(payload.username, payload.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.id})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
async def me(current_user=Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


__all__ = ["router"]
