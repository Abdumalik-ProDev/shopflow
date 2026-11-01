"""Inventory domain repository interface."""

from __future__ import annotations

from typing import List

from shopflow.modules.inventory.domain.models.stock import StockMovement


class StockMovementRepository:
    async def add(self, movement: StockMovement) -> None:
        raise NotImplementedError

    async def list_by_product(self, product_id: str) -> List[StockMovement]:
        raise NotImplementedError


__all__ = ["StockMovementRepository"]
