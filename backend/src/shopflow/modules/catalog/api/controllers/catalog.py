"""Catalog API controllers."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.catalog.api.schemas.catalog import (
    CategoryCreateRequest, CategoryResponse,
    ProductCreateRequest, ProductUpdateRequest, ProductResponse,
)
from shopflow.modules.catalog.application.services.catalog import CatalogService
from shopflow.modules.catalog.infrastructure.repositories import (
    SqlAlchemyCategoryRepository, SqlAlchemyProductRepository,
)

router = APIRouter(prefix="/products", tags=["catalog"])


def _cat_service(session: AsyncSession = Depends(get_session)) -> CatalogService:
    return CatalogService(
        category_repo=SqlAlchemyCategoryRepository(session),
        product_repo=SqlAlchemyProductRepository(session),
    )


def _prod_service(session: AsyncSession = Depends(get_session)) -> CatalogService:
    return CatalogService(
        category_repo=SqlAlchemyCategoryRepository(session),
        product_repo=SqlAlchemyProductRepository(session),
    )


@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(payload: CategoryCreateRequest, svc: CatalogService = Depends(_cat_service), session: AsyncSession = Depends(get_session)):
    c = await svc.create_category(payload)
    await session.commit()
    return CategoryResponse.model_validate(c)


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(skip: int = 0, limit: int = 100, svc: CatalogService = Depends(_cat_service)):
    return await svc.list_categories(skip=skip, limit=limit)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreateRequest, svc: CatalogService = Depends(_prod_service), session: AsyncSession = Depends(get_session)):
    p = await svc.create_product(payload)
    await session.commit()
    return ProductResponse.model_validate(p)


@router.get("", response_model=list[ProductResponse])
async def list_products(
    skip: int = 0, limit: int = 100,
    category_id: str | None = Query(None), seller_id: str | None = Query(None),
    is_active: bool | None = Query(True), svc: CatalogService = Depends(_prod_service),
):
    return await svc.list_products(
        skip=skip, limit=limit, category_id=category_id,
        seller_id=seller_id, is_active=is_active,
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, svc: CatalogService = Depends(_prod_service)):
    p = await svc.get_product(product_id)
    if p is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse.model_validate(p)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, payload: ProductUpdateRequest, svc: CatalogService = Depends(_prod_service), session: AsyncSession = Depends(get_session)):
    p = await svc.update_product(product_id, payload)
    await session.commit()
    return ProductResponse.model_validate(p)


@router.post("/{product_id}/stock", response_model=ProductResponse)
async def adjust_stock(product_id: str, delta: int, svc: CatalogService = Depends(_prod_service), session: AsyncSession = Depends(get_session)):
    p = await svc.adjust_stock(product_id, delta)
    await session.commit()
    return ProductResponse.model_validate(p)


__all__ = ["router"]
