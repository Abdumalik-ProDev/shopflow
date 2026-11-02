"""Authentication business logic service."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.auth import (
    PasswordChangeRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.mappers.mappers import user_to_dto
from app.models.customer import Customer
from app.models.seller import Seller
from app.models.user import User
from app.repositories.customer_repository import CustomerRepository
from app.repositories.seller_repository import SellerRepository
from app.repositories.user_repository import UserRepository
from app.security.security import create_access_token, hash_password, verify_password


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.customer_repo = CustomerRepository(session)
        self.seller_repo = SellerRepository(session)

    async def register(self, req: UserRegisterRequest) -> UserResponse:
        clean_email = req.email.strip().lower()
        clean_username = req.username.strip()
        existing_email = await self.user_repo.get_by_email(clean_email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        existing_username = await self.user_repo.get_by_username(clean_username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        role_val = (req.role or "customer").strip().lower()
        user = User(
            email=clean_email,
            username=clean_username,
            hashed_password=hash_password(req.password),
            full_name=req.full_name,
            role=role_val,
        )
        created_user = await self.user_repo.create(user)

        # Auto-provision corresponding Customer or Seller profile
        if role_val == "seller":
            await self.seller_repo.create(
                Seller(
                    seller_zip_code_prefix="01310",
                    seller_city="São Paulo",
                    seller_state="SP",
                    user_id=created_user.id,
                )
            )
        else:
            await self.customer_repo.create(
                Customer(
                    customer_unique_id=clean_username,
                    customer_zip_code_prefix="01310",
                    customer_city="São Paulo",
                    customer_state="SP",
                    user_id=created_user.id,
                )
            )

        return user_to_dto(created_user)

    async def login(self, req: UserLoginRequest) -> TokenResponse:
        identifier = req.username.strip()
        user = await self.user_repo.get_by_username(identifier)
        if not user:
            user = await self.user_repo.get_by_email(identifier)
        if not user and identifier != identifier.lower():
            user = await self.user_repo.get_by_email(identifier.lower())

        if not user or not verify_password(req.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username/email or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account inactive",
            )
        token = create_access_token({"sub": str(user.id), "role": user.role})
        return TokenResponse(access_token=token, user=user_to_dto(user))

    async def change_password(self, user: User, req: PasswordChangeRequest) -> dict[str, str]:
        if not verify_password(req.current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )
        user.hashed_password = hash_password(req.new_password)
        await self.session.flush()
        return {"message": "Password updated successfully"}

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        return await self.user_repo.get_by_id(user_id)
