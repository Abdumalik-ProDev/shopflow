"""Authentication business logic service."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.auth import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse
from app.mappers.mappers import user_to_dto
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.security.security import create_access_token, hash_password, verify_password


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def register(self, req: UserRegisterRequest) -> UserResponse:
        existing_email = await self.user_repo.get_by_email(req.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        existing_username = await self.user_repo.get_by_username(req.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        user = User(
            email=req.email,
            username=req.username,
            hashed_password=hash_password(req.password),
            full_name=req.full_name,
            role=req.role,
        )
        created_user = await self.user_repo.create(user)
        return user_to_dto(created_user)

    async def login(self, req: UserLoginRequest) -> TokenResponse:
        user = await self.user_repo.get_by_username(req.username)
        if not user or not verify_password(req.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account inactive",
            )
        token = create_access_token({"sub": str(user.id), "role": user.role})
        return TokenResponse(access_token=token)

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        return await self.user_repo.get_by_id(user_id)
