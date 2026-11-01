"""Sellers infrastructure repository."""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from shopflow.modules.sellers.domain.models.seller import Seller
from shopflow.modules.sellers.domain.repositories.seller import SellerRepository
from shopflow.modules.sellers.infrastructure.persistence.models import SellerRow


class SqlAlchemySellerRepository(SellerRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, seller: Seller) -> None:
        self.session.add(SellerRow(
            id=seller.id, seller_zip_code_prefix=seller.seller_zip_code_prefix,
            seller_city=seller.seller_city, seller_state=seller.seller_state,
        ))
        await self.session.flush()

    async def get_by_id(self, seller_id: str) -> Optional[Seller]:
        row = await self.session.get(SellerRow, UUID(seller_id))
        return self._to_domain(row) if row else None

    async def list(self, skip: int = 0, limit: int = 100) -> List[Seller]:
        result = await self.session.execute(select(SellerRow).offset(skip).limit(limit))
        return [self._to_domain(r) for r in result.scalars().all()]

    async def update(self, seller: Seller) -> None:
        row = await self.session.get(SellerRow, seller.id)
        if not row: return
        row.seller_zip_code_prefix = seller.seller_zip_code_prefix
        row.seller_city = seller.seller_city
        row.seller_state = seller.seller_state
        await self.session.flush()

    async def delete(self, seller_id: str) -> None:
        row = await self.session.get(SellerRow, UUID(seller_id))
        if row: await self.session.delete(row)

    @staticmethod
    def _to_domain(row: SellerRow) -> Seller:
        return Seller(
            id=str(row.id), seller_zip_code_prefix=row.seller_zip_code_prefix,
            seller_city=row.seller_city, seller_state=row.seller_state,
        )


__all__ = ["SqlAlchemySellerRepository"]
