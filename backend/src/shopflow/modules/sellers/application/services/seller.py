"""Sellers application service."""

from shopflow.core.exceptions import NotFoundError
from shopflow.modules.sellers.application.dtos.seller import SellerCreate, SellerOut, SellerUpdate
from shopflow.modules.sellers.application.mappers.seller import (
    domain_to_dto, dto_to_domain, update_domain_from_dto,
)
from shopflow.modules.sellers.domain.models.seller import Seller
from shopflow.modules.sellers.domain.repositories.seller import SellerRepository


class SellerService:
    def __init__(self, seller_repo: SellerRepository):
        self.seller_repo = seller_repo

    async def create(self, dto: SellerCreate) -> SellerOut:
        seller = dto_to_domain(dto)
        await self.seller_repo.add(seller)
        return domain_to_dto(seller)

    async def get_by_id(self, seller_id: str) -> SellerOut | None:
        s = await self.seller_repo.get_by_id(seller_id)
        return domain_to_dto(s) if s else None

    async def update(self, seller_id: str, dto: SellerUpdate) -> SellerOut | None:
        s = await self.seller_repo.get_by_id(seller_id)
        if s is None:
            raise NotFoundError("Seller not found", code="SELLER_NOT_FOUND")
        update_domain_from_dto(s, dto)
        await self.seller_repo.update(s)
        return domain_to_dto(s)

    async def list(self, skip: int = 0, limit: int = 100) -> list[SellerOut]:
        return [domain_to_dto(s) for s in await self.seller_repo.list(skip=skip, limit=limit)]


__all__ = ["SellerService"]
