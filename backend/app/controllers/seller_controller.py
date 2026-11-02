"""Seller controller router."""

import uuid

from fastapi import APIRouter, Query, status

from app.controllers.deps import CurrentUserDep, SessionDep
from app.dtos.seller import SellerCreateRequest, SellerResponse
from app.services.seller_service import SellerService

router = APIRouter(prefix="/sellers", tags=["Sellers"])


@router.post("", response_model=SellerResponse, status_code=status.HTTP_201_CREATED)
async def create_seller(
    payload: SellerCreateRequest,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> SellerResponse:
    service = SellerService(session)
    seller_dto = await service.create_seller(payload)
    await session.commit()
    return seller_dto


@router.get("", response_model=list[SellerResponse])
async def list_sellers(
    session: SessionDep,
    current_user: CurrentUserDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[SellerResponse]:
    service = SellerService(session)
    return await service.list_sellers(skip=skip, limit=limit)


@router.get("/{seller_id}", response_model=SellerResponse)
async def get_seller(
    seller_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> SellerResponse:
    service = SellerService(session)
    return await service.get_seller(seller_id)
