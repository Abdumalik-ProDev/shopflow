"""Identity infrastructure repository implementation."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.modules.identity.domain.models.user import User
from shopflow.modules.identity.domain.repositories.user import UserRepository
from shopflow.modules.identity.infrastructure.persistence.models import UserRow


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> None:
        row = UserRow(
            id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            role=user.role,
        )
        self.session.add(row)
        await self.session.flush()

    async def get_by_id(self, user_id: str) -> Optional[User]:
        from uuid import UUID

        row = await self.session.get(UserRow, UUID(user_id))
        return self._to_domain(row) if row else None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(UserRow).where(UserRow.email == email))
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(select(UserRow).where(UserRow.username == username))
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def list(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.session.execute(select(UserRow).offset(skip).limit(limit))
        return [self._to_domain(r) for r in result.scalars().all()]

    async def update(self, user: User) -> None:
        row = await self.session.get(UserRow, user.id)
        if not row:
            return
        row.email = user.email
        row.username = user.username
        row.hashed_password = user.hashed_password
        row.full_name = user.full_name
        row.is_active = user.is_active
        row.is_superuser = user.is_superuser
        row.role = user.role
        await self.session.flush()

    async def delete(self, user_id: str) -> None:
        from uuid import UUID

        row = await self.session.get(UserRow, UUID(user_id))
        if row:
            await self.session.delete(row)

    async def exists_by_email(self, email: str) -> bool:
        result = await self.session.execute(select(UserRow.id).where(UserRow.email == email))
        return result.scalar_one_or_none() is not None

    async def exists_by_username(self, username: str) -> bool:
        result = await self.session.execute(select(UserRow.id).where(UserRow.username == username))
        return result.scalar_one_or_none() is not None

    @staticmethod
    def _to_domain(row: UserRow) -> User:
        return User(
            id=str(row.id),
            email=row.email,
            username=row.username,
            hashed_password=row.hashed_password,
            full_name=row.full_name,
            is_active=row.is_active,
            is_superuser=row.is_superuser,
            role=row.role,
        )


__all__ = ["SqlAlchemyUserRepository"]
