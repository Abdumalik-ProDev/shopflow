"""Sellers API controllers."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.sellers.api.schemas.seller import (
    SellerCreateRequest, SellerUpdateRequest, SellerResponse,
)
from shopflow.modules.sellers.application.services.seller import SellerService
from shopflow.modules.sellers.infrastructure.repositories import SqlAlchemySellerRepository

router = APIRouter(prefix="/sellers", tags=["sellers"])


def _service(session: AsyncSession = Depends(get_session)) -> SellerService:
    return SellerService(SqlAlchemySellerRepository(session))


@router.post("", response_model=SellerResponse, status_code=status.HTTP_201_CREATED)
async def create_seller(payload: SellerCreateRequest, svc: SellerService = Depends(_service), session: AsyncSession = Depends(get_session)):
    s = await svc.create(payload)
    await session.commit()
    return SellerResponse.model_validate(s)


@router.get("", response_model=list[SellerResponse])
async def list_sellers(skip: int = 0, limit: int = 100, svc: SellerService = Depends(_service)):
    return await svc.list(skip=skip, limit=limit)


@router.get("/{seller_id}", response_model=SellerResponse)
async def get_seller(seller_id: str, svc: SellerService = Depends(_service)):
    s = await svc.get_by_id(seller_id)
    if s is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return SellerResponse.model_validate(s)


@router.patch("/{seller_id}", response_model=SellerResponse)
async def update_seller(seller_id: str, payload: SellerUpdateRequest, svc: SellerService = Depends(_service), session: AsyncSession = Depends(get_session)):
    s = await svc.update(seller_id, payload)
    await session.commit()
    return SellerResponse.model_validate(s)


__all__ = ["router"]
