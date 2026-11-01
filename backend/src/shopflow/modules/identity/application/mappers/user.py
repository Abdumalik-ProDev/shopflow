"""Identity mappers: domain <-> dto <-> orm."""

from __future__ import annotations

from shopflow.modules.identity.application.dtos.user import UserCreate, UserOut, UserUpdate
from shopflow.modules.identity.domain.models.user import User


def domain_to_dto(user: User) -> UserOut:
    return UserOut(
        id=str(user.id),
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        role=user.role,
    )


def dto_to_domain(dto: UserCreate, hashed_password: str) -> User:
    return User(
        email=dto.email,
        username=dto.username,
        hashed_password=hashed_password,
        full_name=dto.full_name,
        role=dto.role,
    )


def update_domain_from_dto(user: User, dto: UserUpdate) -> None:
    for field, value in dto.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    user.touch()

__all__ = ["domain_to_dto", "dto_to_domain", "update_domain_from_dto"]
