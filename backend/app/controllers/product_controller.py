"""Catalog and product controller router."""

import uuid

from fastapi import APIRouter, Query, status

from app.controllers.deps import OptionalUserDep, SessionDep
from app.dtos.category import CategoryCreateRequest, CategoryResponse
from app.dtos.product import (
    ProductCreateRequest,
    ProductResponse,
    ProductUpdateRequest,
    StockAdjustRequest,
)
from app.services.catalog_service import CatalogService

router = APIRouter(prefix="/products", tags=["Catalog"])


# Categories
@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CategoryCreateRequest,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> CategoryResponse:
    service = CatalogService(session)
    category_dto = await service.create_category(payload)
    await session.commit()
    return category_dto


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[CategoryResponse]:
    service = CatalogService(session)
    return await service.list_categories(skip=skip, limit=limit)


# Products
@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreateRequest,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> ProductResponse:
    service = CatalogService(session)
    product_dto = await service.create_product(payload)
    await session.commit()
    return product_dto


@router.get("", response_model=list[ProductResponse])
async def list_products(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    category_id: str | None = Query(None),
    seller_id: str | None = Query(None),
    is_active: bool | None = Query(True),
) -> list[ProductResponse]:
    service = CatalogService(session)
    return await service.list_products(
        skip=skip,
        limit=limit,
        category_id=category_id,
        seller_id=seller_id,
        is_active=is_active,
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: uuid.UUID, session: SessionDep) -> ProductResponse:
    service = CatalogService(session)
    return await service.get_product(product_id)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: uuid.UUID,
    payload: ProductUpdateRequest,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> ProductResponse:
    service = CatalogService(session)
    updated = await service.update_product(product_id, payload)
    await session.commit()
    return updated


@router.post("/{product_id}/stock", response_model=ProductResponse)
async def adjust_product_stock(
    product_id: uuid.UUID,
    session: SessionDep,
    payload: StockAdjustRequest | None = None,
    delta: int | None = Query(None),
    current_user: OptionalUserDep = None,
) -> ProductResponse:
    effective_delta = 0
    if payload is not None and payload.delta != 0:
        effective_delta = payload.delta
    elif delta is not None:
        effective_delta = delta

    service = CatalogService(session)
    updated = await service.adjust_stock(product_id, effective_delta)
    await session.commit()
    return updated
