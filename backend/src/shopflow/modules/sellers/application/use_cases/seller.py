"""Sellers application use cases."""

from __future__ import annotations

from shopflow.core.exceptions import NotFoundError
from shopflow.modules.sellers.application.dtos.seller import SellerCreate, SellerOut, SellerUpdate
from shopflow.modules.sellers.domain.models.seller import Seller
from shopflow.modules.sellers.domain.repositories.seller import SellerRepository


class CreateSellerUseCase:
    def __init__(self, seller_repo: SellerRepository):
        self.seller_repo = seller_repo

    async def execute(self, dto: SellerCreate) -> SellerOut:
        seller = Seller(
            seller_zip_code_prefix=dto.seller_zip_code_prefix,
            seller_city=dto.seller_city,
            seller_state=dto.seller_state,
        )
        await self.seller_repo.add(seller)
        return SellerOut.model_validate(seller)


class GetSellerUseCase:
    def __init__(self, seller_repo: SellerRepository):
        self.seller_repo = seller_repo

    async def execute(self, seller_id: str) -> SellerOut | None:
        seller = await self.seller_repo.get_by_id(seller_id)
        if seller is None:
            return None
        return SellerOut.model_validate(seller)


class UpdateSellerUseCase:
    def __init__(self, seller_repo: SellerRepository):
        self.seller_repo = seller_repo

    async def execute(self, seller_id: str, dto: SellerUpdate) -> SellerOut | None:
        seller = await self.seller_repo.get_by_id(seller_id)
        if seller is None:
            raise NotFoundError("Seller not found", code="SELLER_NOT_FOUND")
        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(seller, field, value)
        await self.seller_repo.update(seller)
        return SellerOut.model_validate(seller)


class ListSellersUseCase:
    def __init__(self, seller_repo: SellerRepository):
        self.seller_repo = seller_repo

    async def execute(self, skip: int = 0, limit: int = 100) -> list[SellerOut]:
        sellers = await self.seller_repo.list(skip=skip, limit=limit)
        return [SellerOut.model_validate(s) for s in sellers]


__all__ = [
    "CreateSellerUseCase",
    "GetSellerUseCase",
    "UpdateSellerUseCase",
    "ListSellersUseCase",
]
