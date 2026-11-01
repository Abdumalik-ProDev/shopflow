"""Payments mappers."""

from shopflow.modules.payments.application.dtos.payment import PaymentCreate, PaymentOut
from shopflow.modules.payments.domain.models.payment import Payment


def domain_to_dto(p: Payment) -> PaymentOut:
    return PaymentOut(
        id=str(p.id), order_id=str(p.order_id),
        payment_sequential=p.payment_sequential, payment_type=p.payment_type,
        payment_installments=p.payment_installments, payment_value=p.payment_value,
    )


def dto_to_domain(dto: PaymentCreate) -> Payment:
    return Payment(
        order_id=dto.order_id, payment_sequential=dto.payment_sequential,
        payment_type=dto.payment_type, payment_installments=dto.payment_installments,
        payment_value=dto.payment_value,
    )


__all__ = ["domain_to_dto", "dto_to_domain"]
