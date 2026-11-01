"""Payments application use cases."""

from __future__ import annotations

from shopflow.core.exceptions import NotFoundError
from shopflow.modules.payments.application.dtos.payment import PaymentCreate, PaymentOut
from shopflow.modules.payments.domain.models.payment import Payment
from shopflow.modules.payments.domain.repositories.payment import PaymentRepository


class CreatePaymentUseCase:
    def __init__(self, payment_repo: PaymentRepository):
        self.payment_repo = payment_repo

    async def execute(self, dto: PaymentCreate) -> PaymentOut:
        payment = Payment(
            order_id=dto.order_id,
            payment_sequential=dto.payment_sequential,
            payment_type=dto.payment_type,
            payment_installments=dto.payment_installments,
            payment_value=dto.payment_value,
        )
        await self.payment_repo.add(payment)
        return PaymentOut.model_validate(payment)


class ListPaymentsByOrderUseCase:
    def __init__(self, payment_repo: PaymentRepository):
        self.payment_repo = payment_repo

    async def execute(self, order_id: str) -> list[PaymentOut]:
        payments = await self.payment_repo.list_by_order(order_id)
        return [PaymentOut.model_validate(p) for p in payments]


__all__ = ["CreatePaymentUseCase", "ListPaymentsByOrderUseCase"]
