"""Inventory infrastructure repository implementation."""

from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.modules.inventory.domain.models.stock import StockMovement
from shopflow.modules.inventory.domain.repositories.stock import StockMovementRepository
from shopflow.modules.inventory.infrastructure.persistence.models import StockMovementRow


class SqlAlchemyStockMovementRepository(StockMovementRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, movement: StockMovement) -> None:
        row = StockMovementRow(
            id=movement.id,
            product_id=movement.product_id,
            type=movement.type,
            quantity=movement.quantity,
            reason=movement.reason,
        )
        self.session.add(row)
        await self.session.flush()

    async def list_by_product(self, product_id: str) -> List[StockMovement]:
        result = await self.session.execute(
            select(StockMovementRow).where(StockMovementRow.product_id == product_id)
        )
        return [self._to_domain(r) for r in result.scalars().all()]

    @staticmethod
    def _to_domain(row: StockMovementRow) -> StockMovement:
        return StockMovement(
            id=str(row.id),
            product_id=row.product_id,
            type=row.type,
            quantity=row.quantity,
            reason=row.reason,
        )


__all__ = ["SqlAlchemyStockMovementRepository"]
