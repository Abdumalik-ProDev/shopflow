"""Identity domain repository interface."""

from __future__ import annotations

from typing import Optional, List

from shopflow.modules.identity.domain.models.user import User


class UserRepository:
    async def add(self, user: User) -> None:
        raise NotImplementedError

    async def get_by_id(self, user_id: str) -> Optional[User]:
        raise NotImplementedError

    async def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    async def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError

    async def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        raise NotImplementedError

    async def update(self, user: User) -> None:
        raise NotImplementedError

    async def delete(self, user_id: str) -> None:
        raise NotImplementedError

    async def exists_by_email(self, email: str) -> bool:
        raise NotImplementedError

    async def exists_by_username(self, username: str) -> bool:
        raise NotImplementedError

__all__ = ["UserRepository"]
