"""Seller business logic service."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.seller import SellerCreateRequest, SellerResponse
from app.mappers.mappers import seller_to_dto
from app.models.seller import Seller
from app.repositories.seller_repository import SellerRepository


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.seller_repo = SellerRepository(session)

    async def create_seller(self, req: SellerCreateRequest) -> SellerResponse:
        seller = Seller(
            seller_zip_code_prefix=req.seller_zip_code_prefix,
            seller_city=req.seller_city,
            seller_state=req.seller_state,
            user_id=uuid.UUID(req.user_id) if req.user_id else None,
        )
        created = await self.seller_repo.create(seller)
        return seller_to_dto(created)

    async def get_seller(self, seller_id: uuid.UUID) -> SellerResponse:
        seller = await self.seller_repo.get_by_id(seller_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found",
            )
        return seller_to_dto(seller)

    async def list_sellers(self, skip: int = 0, limit: int = 100) -> list[SellerResponse]:
        sellers = await self.seller_repo.list_all(skip=skip, limit=limit)
        return [seller_to_dto(s) for s in sellers]
