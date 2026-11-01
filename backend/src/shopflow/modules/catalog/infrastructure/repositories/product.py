"""Catalog infrastructure repository stub."""

from __future__ import annotations

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.modules.catalog.domain.models.product import Product
from shopflow.modules.catalog.domain.repositories.product import ProductRepository


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, product: Product) -> None:
        raise NotImplementedError

    async def get_by_id(self, product_id: str) -> Optional[Product]:
        raise NotImplementedError

    async def list(self, skip: int = 0, limit: int = 100):
        return []

    async def update(self, product: Product) -> None:
        raise NotImplementedError

    async def delete(self, product_id: str) -> None:
        raise NotImplementedError


__all__ = ["SqlAlchemyProductRepository"]
