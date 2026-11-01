"""Payments domain repository interface."""

from __future__ import annotations

from typing import Optional, List

from shopflow.modules.payments.domain.models.payment import Payment


class PaymentRepository:
    async def add(self, payment: Payment) -> None:
        raise NotImplementedError

    async def get_by_id(self, payment_id: str) -> Optional[Payment]:
        raise NotImplementedError

    async def list_by_order(self, order_id: str) -> List[Payment]:
        raise NotImplementedError

    async def update(self, payment: Payment) -> None:
        raise NotImplementedError


__all__ = ["PaymentRepository"]
