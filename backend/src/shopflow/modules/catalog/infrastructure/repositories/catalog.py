"""Catalog infrastructure repository implementation."""

from __future__ import annotations

from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.modules.catalog.domain.models.product import Category, Product
from shopflow.modules.catalog.domain.repositories.catalog import (
    CategoryRepository,
    ProductRepository,
)
from shopflow.modules.catalog.infrastructure.persistence.models import CategoryRow, ProductRow


class SqlAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, category: Category) -> None:
        row = CategoryRow(
            id=category.id,
            name=category.name,
            name_english=category.name_english,
        )
        self.session.add(row)
        await self.session.flush()

    async def get_by_id(self, category_id: str) -> Optional[Category]:
        from uuid import UUID

        row = await self.session.get(CategoryRow, UUID(category_id))
        return self._to_domain(row) if row else None

    async def get_by_name(self, name: str) -> Optional[Category]:
        result = await self.session.execute(select(CategoryRow).where(CategoryRow.name == name))
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def list(self, skip: int = 0, limit: int = 100) -> List[Category]:
        result = await self.session.execute(select(CategoryRow).offset(skip).limit(limit))
        return [self._to_domain(r) for r in result.scalars().all()]


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, product: Product) -> None:
        row = ProductRow(
            id=product.id,
            sku=product.sku,
            name=product.name,
            description=product.description,
            price=product.price,
            stock_quantity=product.stock_quantity,
            category_id=product.category_id,
            seller_id=product.seller_id,
            is_active=product.is_active,
            weight_g=product.weight_g,
            length_cm=product.length_cm,
            height_cm=product.height_cm,
            width_cm=product.width_cm,
            photos_qty=product.photos_qty,
        )
        self.session.add(row)
        await self.session.flush()

    async def get_by_id(self, product_id: str) -> Optional[Product]:
        from uuid import UUID

        row = await self.session.get(ProductRow, UUID(product_id))
        return self._to_domain(row) if row else None

    async def get_by_sku(self, sku: str) -> Optional[Product]:
        result = await self.session.execute(select(ProductRow).where(ProductRow.sku == sku))
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: str | None = None,
        seller_id: str | None = None,
        is_active: bool | None = True,
    ) -> List[Product]:
        query = select(ProductRow)
        if category_id:
            from uuid import UUID
            query = query.where(ProductRow.category_id == UUID(category_id))
        if seller_id:
            from uuid import UUID
            query = query.where(ProductRow.seller_id == UUID(seller_id))
        if is_active is not None:
            query = query.where(ProductRow.is_active == is_active)
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return [self._to_domain(r) for r in result.scalars().all()]

    async def update(self, product: Product) -> None:
        row = await self.session.get(ProductRow, product.id)
        if not row:
            return
        row.sku = product.sku
        row.name = product.name
        row.description = product.description
        row.price = product.price
        row.stock_quantity = product.stock_quantity
        row.category_id = product.category_id
        row.seller_id = product.seller_id
        row.is_active = product.is_active
        row.weight_g = product.weight_g
        row.length_cm = product.length_cm
        row.height_cm = product.height_cm
        row.width_cm = product.width_cm
        row.photos_qty = product.photos_qty
        await self.session.flush()

    async def delete(self, product_id: str) -> None:
        from uuid import UUID

        row = await self.session.get(ProductRow, UUID(product_id))
        if row:
            await self.session.delete(row)

    @staticmethod
    def _to_domain(row: ProductRow) -> Product:
        return Product(
            id=str(row.id),
            sku=row.sku,
            name=row.name,
            description=row.description,
            price=row.price,
            stock_quantity=row.stock_quantity,
            category_id=str(row.category_id) if row.category_id else None,
            seller_id=str(row.seller_id) if row.seller_id else None,
            is_active=row.is_active,
            weight_g=row.weight_g,
            length_cm=row.length_cm,
            height_cm=row.height_cm,
            width_cm=row.width_cm,
            photos_qty=row.photos_qty,
        )

    @staticmethod
    def _to_domain_category(row: CategoryRow) -> Category:
        return Category(
            id=str(row.id),
            name=row.name,
            name_english=row.name_english,
        )


__all__ = ["SqlAlchemyCategoryRepository", "SqlAlchemyProductRepository"]
