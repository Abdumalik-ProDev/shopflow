"""Payments domain models."""

from shopflow.shared.domain.base_entity import BaseEntity


class PaymentType:
    CREDIT_CARD = "credit_card"
    BOLETO = "boleto"
    DEBIT_CARD = "debit_card"
    VOUCHER = "voucher"


class Payment(BaseEntity):
    def __init__(self, id=None, order_id="", payment_sequential=1,
                 payment_type=PaymentType.CREDIT_CARD,
                 payment_installments=1, payment_value=0.0):
        super().__init__()
        self.id = id or self.id
        self.order_id = order_id
        self.payment_sequential = payment_sequential
        self.payment_type = payment_type
        self.payment_installments = payment_installments
        self.payment_value = payment_value


__all__ = ["PaymentType", "Payment"]
