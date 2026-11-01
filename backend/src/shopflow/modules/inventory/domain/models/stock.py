"""Inventory domain models."""

from __future__ import annotations

from shopflow.shared.domain.base_entity import BaseEntity


class StockMovement(BaseEntity):
    class Type(str):
        IN = "in"
        OUT = "out"
        ADJUSTMENT = "adjustment"

    def __init__(
        self,
        id: str | None = None,
        product_id: str = "",
        type: str = Type.IN,
        quantity: int = 0,
        reason: str = "",
    ):
        super().__init__()
        self.id = id or self.id
        self.product_id = product_id
        self.type = type
        self.quantity = quantity
        self.reason = reason


__all__ = ["StockMovement"]
