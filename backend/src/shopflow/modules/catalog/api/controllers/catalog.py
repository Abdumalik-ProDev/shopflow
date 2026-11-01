"""Catalog API controllers."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.catalog.api.schemas.catalog import (
    CategoryCreateRequest,
    CategoryResponse,
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductResponse,
)
from shopflow.modules.catalog.application.use_cases.catalog import (
    CreateCategoryUseCase,
    ListCategoriesUseCase,
    CreateProductUseCase,
    GetProductUseCase,
    ListProductsUseCase,
    UpdateProductUseCase,
    AdjustStockUseCase,
)
from shopflow.modules.catalog.infrastructure.repositories import (
    SqlAlchemyCategoryRepository,
    SqlAlchemyProductRepository,
)

router = APIRouter(prefix="/products", tags=["catalog"])


def _cat_repo(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyCategoryRepository(session)


def _prod_repo(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyProductRepository(session)


# Categories
@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CategoryCreateRequest, repo=Depends(_cat_repo), session: AsyncSession = Depends(get_session)
):
    use_case = CreateCategoryUseCase(repo)
    category = await use_case.execute(payload)
    await session.commit()
    return CategoryResponse.model_validate(category)


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(
    skip: int = 0, limit: int = 100, repo=Depends(_cat_repo)
):
    use_case = ListCategoriesUseCase(repo)
    return await use_case.execute(skip=skip, limit=limit)


# Products
@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreateRequest, repo=Depends(_prod_repo), session: AsyncSession = Depends(get_session)
):
    cat_repo = SqlAlchemyCategoryRepository(repo.session if hasattr(repo, "session") else session)
    use_case = CreateProductUseCase(repo, cat_repo)
    product = await use_case.execute(payload)
    await session.commit()
    return ProductResponse.model_validate(product)


@router.get("", response_model=list[ProductResponse])
async def list_products(
    skip: int = 0,
    limit: int = 100,
    category_id: str | None = Query(None),
    seller_id: str | None = Query(None),
    is_active: bool | None = Query(True),
    repo=Depends(_prod_repo),
):
    use_case = ListProductsUseCase(repo)
    return await use_case.execute(
        skip=skip, limit=limit, category_id=category_id, seller_id=seller_id, is_active=is_active
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, repo=Depends(_prod_repo)):
    use_case = GetProductUseCase(repo)
    product = await use_case.execute(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse.model_validate(product)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    payload: ProductUpdateRequest,
    repo=Depends(_prod_repo),
    session: AsyncSession = Depends(get_session),
):
    use_case = UpdateProductUseCase(repo)
    product = await use_case.execute(product_id, payload)
    await session.commit()
    return ProductResponse.model_validate(product)


@router.post("/{product_id}/stock", response_model=ProductResponse)
async def adjust_stock(
    product_id: str,
    delta: int,
    repo=Depends(_prod_repo),
    session: AsyncSession = Depends(get_session),
):
    use_case = AdjustStockUseCase(repo)
    product = await use_case.execute(product_id, delta)
    await session.commit()
    return ProductResponse.model_validate(product)


__all__ = ["router"]
