"""Seller repository for persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.seller import Seller


class SellerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, seller_id: uuid.UUID) -> Seller | None:
        return await self.session.get(Seller, seller_id)

    async def create(self, seller: Seller) -> Seller:
        self.session.add(seller)
        await self.session.flush()
        return seller

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[Seller]:
        result = await self.session.execute(select(Seller).offset(skip).limit(limit))
        return list(result.scalars().all())
