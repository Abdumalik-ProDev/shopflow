"""Seller controller router."""

from fastapi import APIRouter, Query, status

from app.controllers.deps import OptionalUserDep, SessionDep
from app.dtos.seller import SellerCreateRequest, SellerResponse, SellerUpdateRequest
from app.services.seller_service import SellerService

router = APIRouter(prefix="/sellers", tags=["Sellers"])


@router.post("", response_model=SellerResponse, status_code=status.HTTP_201_CREATED)
async def create_seller(
    payload: SellerCreateRequest,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> SellerResponse:
    service = SellerService(session)
    seller_dto = await service.create_seller(payload)
    await session.commit()
    return seller_dto


@router.get("", response_model=list[SellerResponse])
async def list_sellers(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: OptionalUserDep = None,
) -> list[SellerResponse]:
    service = SellerService(session)
    return await service.list_sellers(skip=skip, limit=limit)


@router.get("/{seller_id}", response_model=SellerResponse)
async def get_seller(
    seller_id: str,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> SellerResponse:
    service = SellerService(session)
    return await service.get_seller(seller_id)


@router.patch("/{seller_id}", response_model=SellerResponse)
async def update_seller(
    seller_id: str,
    payload: SellerUpdateRequest,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> SellerResponse:
    service = SellerService(session)
    updated = await service.update_seller(seller_id, payload)
    await session.commit()
    return updated
