"""Sellers domain repository interface."""

from typing import Optional, List
from shopflow.modules.sellers.domain.models.seller import Seller


class SellerRepository:
    async def add(self, seller: Seller) -> None: raise NotImplementedError
    async def get_by_id(self, seller_id: str) -> Optional[Seller]: raise NotImplementedError
    async def list(self, skip: int = 0, limit: int = 100) -> List[Seller]: raise NotImplementedError
    async def update(self, seller: Seller) -> None: raise NotImplementedError
    async def delete(self, seller_id: str) -> None: raise NotImplementedError


__all__ = ["SellerRepository"]
