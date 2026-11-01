"""Identity application service (business logic)."""

from __future__ import annotations

from shopflow.core.exceptions import ConflictError, NotFoundError
from shopflow.core.security import hash_password
from shopflow.modules.identity.application.dtos.user import UserCreate, UserOut, UserUpdate
from shopflow.modules.identity.application.mappers.user import (
    domain_to_dto,
    dto_to_domain,
    update_domain_from_dto,
)
from shopflow.modules.identity.domain.models.user import User
from shopflow.modules.identity.domain.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, dto: UserCreate) -> UserOut:
        if await self.user_repo.exists_by_email(dto.email):
            raise ConflictError("Email already registered", code="EMAIL_TAKEN")
        if await self.user_repo.exists_by_username(dto.username):
            raise ConflictError("Username already taken", code="USERNAME_TAKEN")

        user = dto_to_domain(dto, hash_password(dto.password))
        await self.user_repo.add(user)
        return domain_to_dto(user)

    async def get_by_id(self, user_id: str) -> UserOut | None:
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            return None
        return domain_to_dto(user)

    async def update(self, user_id: str, dto: UserUpdate) -> UserOut | None:
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found", code="USER_NOT_FOUND")
        update_domain_from_dto(user, dto)
        await self.user_repo.update(user)
        return domain_to_dto(user)

    async def deactivate(self, user_id: str) -> bool:
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found", code="USER_NOT_FOUND")
        user.deactivate()
        await self.user_repo.update(user)
        return True

    async def list(self, skip: int = 0, limit: int = 100) -> list[UserOut]:
        users = await self.user_repo.list(skip=skip, limit=limit)
        return [domain_to_dto(u) for u in users]


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate(self, username: str, password: str) -> UserOut | None:
        from shopflow.core.security import verify_password

        user = await self.user_repo.get_by_username(username)
        if user is None or not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            raise NotFoundError("Account is inactive", code="ACCOUNT_INACTIVE")
        return domain_to_dto(user)

__all__ = ["UserService", "AuthService"]
