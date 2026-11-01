"""Catalog domain repository interface."""

from __future__ import annotations

from typing import Optional, List

from shopflow.modules.catalog.domain.models.product import Product


class ProductRepository:
    async def add(self, product: Product) -> None:
        raise NotImplementedError

    async def get_by_id(self, product_id: str) -> Optional[Product]:
        raise NotImplementedError

    async def list(self, skip: int = 0, limit: int = 100) -> List[Product]:
        raise NotImplementedError

    async def update(self, product: Product) -> None:
        raise NotImplementedError

    async def delete(self, product_id: str) -> None:
        raise NotImplementedError


__all__ = ["ProductRepository"]
