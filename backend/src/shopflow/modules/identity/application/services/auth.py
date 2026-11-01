"""Identity application services."""

from __future__ import annotations

from shopflow.core.exceptions import ConflictError, NotFoundError
from shopflow.core.security import create_access_token, decode_token, hash_password, verify_password
from shopflow.modules.identity.application.dtos.user import UserCreate, UserOut
from shopflow.modules.identity.application.interfaces.auth import PasswordHasher, TokenService
from shopflow.modules.identity.domain.models.user import User
from shopflow.modules.identity.domain.repositories.user import UserRepository


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ):
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def register(self, dto: UserCreate) -> UserOut:
        if await self.user_repo.exists_by_email(dto.email):
            raise ConflictError("Email already registered", code="EMAIL_TAKEN")
        if await self.user_repo.exists_by_username(dto.username):
            raise ConflictError("Username already taken", code="USERNAME_TAKEN")

        user = User(
            email=dto.email,
            username=dto.username,
            hashed_password=await self.password_hasher.hash(dto.password),
            full_name=dto.full_name,
            role=dto.role,
        )
        await self.user_repo.add(user)
        return UserOut.model_validate(user)

    async def authenticate(self, username: str, password: str) -> UserOut | None:
        user = await self.user_repo.get_by_username(username)
        if user is None or not await self.password_hasher.verify(password, user.hashed_password):
            return None
        if not user.is_active:
            raise NotFoundError("Account is inactive", code="ACCOUNT_INACTIVE")
        return UserOut.model_validate(user)

    async def get_current_user(self, token: str) -> UserOut | None:
        payload = await self.token_service.decode_token(token)
        if payload is None:
            return None
        user_id = payload.get("sub")
        if not user_id:
            return None
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            return None
        return UserOut.model_validate(user)


__all__ = ["AuthService"]
