"""Payments infrastructure repository."""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from shopflow.modules.payments.domain.models.payment import Payment
from shopflow.modules.payments.domain.repositories.payment import PaymentRepository
from shopflow.modules.payments.infrastructure.persistence.models import PaymentRow


class SqlAlchemyPaymentRepository(PaymentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, payment: Payment) -> None:
        self.session.add(PaymentRow(
            id=payment.id, order_id=payment.order_id,
            payment_sequential=payment.payment_sequential,
            payment_type=payment.payment_type,
            payment_installments=payment.payment_installments,
            payment_value=payment.payment_value,
        ))
        await self.session.flush()

    async def get_by_id(self, payment_id: str) -> Optional[Payment]:
        row = await self.session.get(PaymentRow, UUID(payment_id))
        return self._to_domain(row) if row else None

    async def list_by_order(self, order_id: str) -> List[Payment]:
        result = await self.session.execute(
            select(PaymentRow).where(PaymentRow.order_id == UUID(order_id))
        )
        return [self._to_domain(r) for r in result.scalars().all()]

    async def update(self, payment: Payment) -> None:
        row = await self.session.get(PaymentRow, payment.id)
        if not row: return
        row.order_id = payment.order_id
        row.payment_sequential = payment.payment_sequential
        row.payment_type = payment.payment_type
        row.payment_installments = payment.payment_installments
        row.payment_value = payment.payment_value
        await self.session.flush()

    @staticmethod
    def _to_domain(row: PaymentRow) -> Payment:
        return Payment(
            id=str(row.id), order_id=str(row.order_id),
            payment_sequential=row.payment_sequential,
            payment_type=row.payment_type,
            payment_installments=row.payment_installments,
            payment_value=row.payment_value,
        )


__all__ = ["SqlAlchemyPaymentRepository"]
