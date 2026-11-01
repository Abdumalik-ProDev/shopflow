"""Catalog application use cases."""

from __future__ import annotations

from shopflow.core.exceptions import NotFoundError, ConflictError
from shopflow.modules.catalog.application.dtos.catalog import (
    CategoryCreate,
    CategoryOut,
    ProductCreate,
    ProductOut,
    ProductUpdate,
)
from shopflow.modules.catalog.domain.models.product import Category, Product
from shopflow.modules.catalog.domain.repositories.catalog import (
    CategoryRepository,
    ProductRepository,
)


class CreateCategoryUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def execute(self, dto: CategoryCreate) -> CategoryOut:
        category = Category(name=dto.name, name_english=dto.name_english)
        await self.category_repo.add(category)
        return CategoryOut.model_validate(category)


class ListCategoriesUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def execute(self, skip: int = 0, limit: int = 100) -> list[CategoryOut]:
        categories = await self.category_repo.list(skip=skip, limit=limit)
        return [CategoryOut.model_validate(c) for c in categories]


class CreateProductUseCase:
    def __init__(self, product_repo: ProductRepository, category_repo: CategoryRepository):
        self.product_repo = product_repo
        self.category_repo = category_repo

    async def execute(self, dto: ProductCreate) -> ProductOut:
        if await self.product_repo.get_by_sku(dto.sku):
            raise ConflictError("SKU already exists", code="SKU_EXISTS")
        product = Product(
            sku=dto.sku,
            name=dto.name,
            description=dto.description,
            price=dto.price,
            stock_quantity=dto.stock_quantity,
            category_id=dto.category_id,
            seller_id=dto.seller_id,
            is_active=dto.is_active,
            weight_g=dto.weight_g,
            length_cm=dto.length_cm,
            height_cm=dto.height_cm,
            width_cm=dto.width_cm,
            photos_qty=dto.photos_qty,
        )
        await self.product_repo.add(product)
        return ProductOut.model_validate(product)


class GetProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def execute(self, product_id: str) -> ProductOut | None:
        product = await self.product_repo.get_by_id(product_id)
        if product is None:
            return None
        return ProductOut.model_validate(product)


class ListProductsUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def execute(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: str | None = None,
        seller_id: str | None = None,
        is_active: bool | None = True,
    ) -> list[ProductOut]:
        products = await self.product_repo.list(
            skip=skip, limit=limit, category_id=category_id, seller_id=seller_id, is_active=is_active
        )
        return [ProductOut.model_validate(p) for p in products]


class UpdateProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def execute(self, product_id: str, dto: ProductUpdate) -> ProductOut | None:
        product = await self.product_repo.get_by_id(product_id)
        if product is None:
            raise NotFoundError("Product not found", code="PRODUCT_NOT_FOUND")
        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        await self.product_repo.update(product)
        return ProductOut.model_validate(product)


class AdjustStockUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def execute(self, product_id: str, delta: int) -> ProductOut | None:
        product = await self.product_repo.get_by_id(product_id)
        if product is None:
            raise NotFoundError("Product not found", code="PRODUCT_NOT_FOUND")
        product.adjust_stock(delta)
        await self.product_repo.update(product)
        return ProductOut.model_validate(product)


__all__ = [
    "CreateCategoryUseCase",
    "ListCategoriesUseCase",
    "CreateProductUseCase",
    "GetProductUseCase",
    "ListProductsUseCase",
    "UpdateProductUseCase",
    "AdjustStockUseCase",
]
