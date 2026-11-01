"""Catalog domain repository interfaces."""

from typing import Optional, List
from shopflow.modules.catalog.domain.models.product import Category, Product


class CategoryRepository:
    async def add(self, category: Category) -> None: raise NotImplementedError
    async def get_by_id(self, category_id: str) -> Optional[Category]: raise NotImplementedError
    async def get_by_name(self, name: str) -> Optional[Category]: raise NotImplementedError
    async def list(self, skip: int = 0, limit: int = 100) -> List[Category]: raise NotImplementedError


class ProductRepository:
    async def add(self, product: Product) -> None: raise NotImplementedError
    async def get_by_id(self, product_id: str) -> Optional[Product]: raise NotImplementedError
    async def get_by_sku(self, sku: str) -> Optional[Product]: raise NotImplementedError
    async def list(self, skip: int = 0, limit: int = 100, category_id: str | None = None,
                   seller_id: str | None = None, is_active: bool | None = True) -> List[Product]: raise NotImplementedError
    async def update(self, product: Product) -> None: raise NotImplementedError
    async def delete(self, product_id: str) -> None: raise NotImplementedError


__all__ = ["CategoryRepository", "ProductRepository"]
