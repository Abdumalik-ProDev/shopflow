"""Catalog application service."""

from shopflow.core.exceptions import ConflictError, NotFoundError
from shopflow.modules.catalog.application.dtos.catalog import (
    CategoryCreate, CategoryOut, ProductCreate, ProductOut, ProductUpdate,
)
from shopflow.modules.catalog.application.mappers.catalog import (
    category_domain_to_dto, product_domain_to_dto,
    product_dto_to_domain, product_update_domain_from_dto,
)
from shopflow.modules.catalog.domain.models.product import Category, Product
from shopflow.modules.catalog.domain.repositories.catalog import (
    CategoryRepository, ProductRepository,
)


class CatalogService:
    def __init__(self, category_repo: CategoryRepository, product_repo: ProductRepository):
        self.category_repo = category_repo
        self.product_repo = product_repo

    async def create_category(self, dto: CategoryCreate) -> CategoryOut:
        category = Category(name=dto.name, name_english=dto.name_english)
        await self.category_repo.add(category)
        return category_domain_to_dto(category)

    async def list_categories(self, skip: int = 0, limit: int = 100) -> list[CategoryOut]:
        return [category_domain_to_dto(c) for c in await self.category_repo.list(skip=skip, limit=limit)]

    async def create_product(self, dto: ProductCreate) -> ProductOut:
        if await self.product_repo.get_by_sku(dto.sku):
            raise ConflictError("SKU already exists", code="SKU_EXISTS")
        product = product_dto_to_domain(dto)
        await self.product_repo.add(product)
        return product_domain_to_dto(product)

    async def get_product(self, product_id: str) -> ProductOut | None:
        p = await self.product_repo.get_by_id(product_id)
        return product_domain_to_dto(p) if p else None

    async def list_products(self, skip: int = 0, limit: int = 100,
                            category_id: str | None = None, seller_id: str | None = None,
                            is_active: bool | None = True) -> list[ProductOut]:
        products = await self.product_repo.list(
            skip=skip, limit=limit, category_id=category_id,
            seller_id=seller_id, is_active=is_active,
        )
        return [product_domain_to_dto(p) for p in products]

    async def update_product(self, product_id: str, dto: ProductUpdate) -> ProductOut | None:
        p = await self.product_repo.get_by_id(product_id)
        if p is None:
            raise NotFoundError("Product not found", code="PRODUCT_NOT_FOUND")
        product_update_domain_from_dto(p, dto)
        await self.product_repo.update(p)
        return product_domain_to_dto(p)

    async def adjust_stock(self, product_id: str, delta: int) -> ProductOut | None:
        p = await self.product_repo.get_by_id(product_id)
        if p is None:
            raise NotFoundError("Product not found", code="PRODUCT_NOT_FOUND")
        p.adjust_stock(delta)
        await self.product_repo.update(p)
        return product_domain_to_dto(p)


__all__ = ["CatalogService"]
