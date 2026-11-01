"""Payments application service."""

from shopflow.core.exceptions import NotFoundError
from shopflow.modules.payments.application.dtos.payment import PaymentCreate, PaymentOut
from shopflow.modules.payments.application.mappers.payment import domain_to_dto, dto_to_domain
from shopflow.modules.payments.domain.models.payment import Payment
from shopflow.modules.payments.domain.repositories.payment import PaymentRepository


class PaymentService:
    def __init__(self, payment_repo: PaymentRepository):
        self.payment_repo = payment_repo

    async def create(self, dto: PaymentCreate) -> PaymentOut:
        payment = dto_to_domain(dto)
        await self.payment_repo.add(payment)
        return domain_to_dto(payment)

    async def list_by_order(self, order_id: str) -> list[PaymentOut]:
        payments = await self.payment_repo.list_by_order(order_id)
        return [domain_to_dto(p) for p in payments]


__all__ = ["PaymentService"]
