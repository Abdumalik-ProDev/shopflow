"""Identity application use cases."""

from __future__ import annotations

from shopflow.core.exceptions import ConflictError, NotFoundError
from shopflow.core.security import hash_password
from shopflow.modules.identity.application.dtos.user import (
    UserCreate,
    UserOut,
    UserUpdate,
)
from shopflow.modules.identity.domain.models.user import User
from shopflow.modules.identity.domain.repositories.user import UserRepository


class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, dto: UserCreate) -> UserOut:
        if await self.user_repo.exists_by_email(dto.email):
            raise ConflictError("Email already registered", code="EMAIL_TAKEN")
        if await self.user_repo.exists_by_username(dto.username):
            raise ConflictError("Username already taken", code="USERNAME_TAKEN")

        user = User(
            email=dto.email,
            username=dto.username,
            hashed_password=hash_password(dto.password),
            full_name=dto.full_name,
            role=dto.role,
        )
        await self.user_repo.add(user)
        return UserOut.model_validate(user)


class GetUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, user_id: str) -> UserOut | None:
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            return None
        return UserOut.model_validate(user)


class UpdateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, user_id: str, dto: UserUpdate) -> UserOut | None:
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found", code="USER_NOT_FOUND")
        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        await self.user_repo.update(user)
        return UserOut.model_validate(user)


class DeactivateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, user_id: str) -> bool:
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found", code="USER_NOT_FOUND")
        user.deactivate()
        await self.user_repo.update(user)
        return True


__all__ = [
    "RegisterUserUseCase",
    "GetUserUseCase",
    "UpdateUserUseCase",
    "DeactivateUserUseCase",
]
