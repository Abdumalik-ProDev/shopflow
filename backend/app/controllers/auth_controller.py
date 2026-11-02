"""Authentication controller router."""

from fastapi import APIRouter, status

from app.controllers.deps import CurrentUserDep, SessionDep
from app.dtos.auth import (
    PasswordChangeRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.mappers.mappers import user_to_dto
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegisterRequest, session: SessionDep) -> UserResponse:
    service = AuthService(session)
    user_dto = await service.register(payload)
    await session.commit()
    return user_dto


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLoginRequest, session: SessionDep) -> TokenResponse:
    service = AuthService(session)
    token_dto = await service.login(payload)
    return token_dto


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: CurrentUserDep) -> UserResponse:
    return user_to_dto(current_user)


@router.post("/change-password")
async def change_password(
    payload: PasswordChangeRequest,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> dict[str, str]:
    service = AuthService(session)
    res = await service.change_password(current_user, payload)
    await session.commit()
    return res
