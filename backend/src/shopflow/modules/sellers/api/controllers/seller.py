"""Sellers API controllers."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.sellers.api.schemas.seller import (
    SellerCreateRequest,
    SellerUpdateRequest,
    SellerResponse,
)
from shopflow.modules.sellers.application.use_cases.seller import (
    CreateSellerUseCase,
    GetSellerUseCase,
    UpdateSellerUseCase,
    ListSellersUseCase,
)
from shopflow.modules.sellers.infrastructure.repositories import SqlAlchemySellerRepository

router = APIRouter(prefix="/sellers", tags=["sellers"])


def _repo(session: AsyncSession = Depends(get_session)):
    return SqlAlchemySellerRepository(session)


@router.post("", response_model=SellerResponse, status_code=status.HTTP_201_CREATED)
async def create_seller(
    payload: SellerCreateRequest, repo=Depends(_repo), session: AsyncSession = Depends(get_session)
):
    use_case = CreateSellerUseCase(repo)
    seller = await use_case.execute(payload)
    await session.commit()
    return SellerResponse.model_validate(seller)


@router.get("", response_model=list[SellerResponse])
async def list_sellers(
    skip: int = 0, limit: int = 100, repo=Depends(_repo)
):
    use_case = ListSellersUseCase(repo)
    return await use_case.execute(skip=skip, limit=limit)


@router.get("/{seller_id}", response_model=SellerResponse)
async def get_seller(seller_id: str, repo=Depends(_repo)):
    use_case = GetSellerUseCase(repo)
    seller = await use_case.execute(seller_id)
    if seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return SellerResponse.model_validate(seller)


@router.patch("/{seller_id}", response_model=SellerResponse)
async def update_seller(
    seller_id: str,
    payload: SellerUpdateRequest,
    repo=Depends(_repo),
    session: AsyncSession = Depends(get_session),
):
    use_case = UpdateSellerUseCase(repo)
    seller = await use_case.execute(seller_id, payload)
    await session.commit()
    return SellerResponse.model_validate(seller)


__all__ = ["router"]
