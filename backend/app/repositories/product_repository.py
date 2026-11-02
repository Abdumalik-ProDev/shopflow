"""Product repository for persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        return await self.session.get(Product, product_id)

    async def get_by_sku(self, sku: str) -> Product | None:
        result = await self.session.execute(select(Product).where(Product.sku == sku))
        return result.scalar_one_or_none()

    async def list_products(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: uuid.UUID | None = None,
        seller_id: uuid.UUID | None = None,
        is_active: bool | None = True,
    ) -> list[Product]:
        query = select(Product)
        if category_id:
            query = query.where(Product.category_id == category_id)
        if seller_id:
            query = query.where(Product.seller_id == seller_id)
        if is_active is not None:
            query = query.where(Product.is_active == is_active)
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.flush()
        return product

    async def update(self, product: Product) -> Product:
        await self.session.flush()
        return product

    async def adjust_stock(self, product: Product, delta: int) -> Product:
        product.stock_quantity += delta
        if product.stock_quantity < 0:
            raise ValueError("Stock cannot be negative")
        await self.session.flush()
        return product
