"""Catalog and inventory business logic service."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.category import CategoryCreateRequest, CategoryResponse
from app.dtos.product import ProductCreateRequest, ProductResponse, ProductUpdateRequest
from app.mappers.mappers import category_to_dto, product_to_dto
from app.models.category import Category
from app.models.product import Product
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository


class CatalogService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.category_repo = CategoryRepository(session)
        self.product_repo = ProductRepository(session)

    # Categories
    async def create_category(self, req: CategoryCreateRequest) -> CategoryResponse:
        existing = await self.category_repo.get_by_name(req.name)
        if existing:
            return category_to_dto(existing)
        cat = Category(name=req.name, name_english=req.name_english)
        created = await self.category_repo.create(cat)
        return category_to_dto(created)

    async def list_categories(self, skip: int = 0, limit: int = 100) -> list[CategoryResponse]:
        categories = await self.category_repo.list_all(skip=skip, limit=limit)
        return [category_to_dto(c) for c in categories]

    # Products
    async def create_product(self, req: ProductCreateRequest) -> ProductResponse:
        existing = await self.product_repo.get_by_sku(req.sku)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product SKU '{req.sku}' already exists",
            )
        prod = Product(
            sku=req.sku,
            name=req.name,
            description=req.description,
            price=req.price,
            stock_quantity=req.stock_quantity,
            category_id=uuid.UUID(req.category_id) if req.category_id else None,
            seller_id=uuid.UUID(req.seller_id) if req.seller_id else None,
            is_active=req.is_active,
            weight_g=req.weight_g,
            length_cm=req.length_cm,
            height_cm=req.height_cm,
            width_cm=req.width_cm,
            photos_qty=req.photos_qty,
        )
        created = await self.product_repo.create(prod)
        return product_to_dto(created)

    async def get_product(self, product_id: uuid.UUID) -> ProductResponse:
        prod = await self.product_repo.get_by_id(product_id)
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        return product_to_dto(prod)

    async def list_products(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: str | None = None,
        seller_id: str | None = None,
        is_active: bool | None = True,
    ) -> list[ProductResponse]:
        cat_uuid = uuid.UUID(category_id) if category_id else None
        sell_uuid = uuid.UUID(seller_id) if seller_id else None
        products = await self.product_repo.list_products(
            skip=skip, limit=limit, category_id=cat_uuid, seller_id=sell_uuid, is_active=is_active
        )
        return [product_to_dto(p) for p in products]

    async def update_product(
        self, product_id: uuid.UUID, req: ProductUpdateRequest
    ) -> ProductResponse:
        prod = await self.product_repo.get_by_id(product_id)
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        update_data = req.model_dump(exclude_unset=True)
        for key, raw_val in update_data.items():
            parsed_val = (
                uuid.UUID(raw_val)
                if key in ("category_id", "seller_id") and raw_val is not None
                else raw_val
            )
            setattr(prod, key, parsed_val)
        updated = await self.product_repo.update(prod)
        return product_to_dto(updated)

    async def adjust_stock(self, product_id: uuid.UUID, delta: int) -> ProductResponse:
        prod = await self.product_repo.get_by_id(product_id)
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        try:
            updated = await self.product_repo.adjust_stock(prod, delta)
        except ValueError as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err
        return product_to_dto(updated)
