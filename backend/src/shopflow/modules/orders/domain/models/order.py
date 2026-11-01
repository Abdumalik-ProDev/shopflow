"""Orders domain models."""

from datetime import datetime, timezone
from typing import Optional
from shopflow.shared.domain.base_entity import BaseEntity


class OrderStatus:
    PENDING = "pending"
    APPROVED = "approved"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(BaseEntity):
    def __init__(self, id=None, customer_id="", status=OrderStatus.PENDING,
                 purchase_timestamp=None, approved_at=None,
                 delivered_carrier_date=None, delivered_customer_date=None,
                 estimated_delivery_date=None, total=0.0):
        super().__init__()
        self.id = id or self.id
        self.customer_id = customer_id
        self.status = status
        self.purchase_timestamp = purchase_timestamp
        self.approved_at = approved_at
        self.delivered_carrier_date = delivered_carrier_date
        self.delivered_customer_date = delivered_customer_date
        self.estimated_delivery_date = estimated_delivery_date
        self.total = total

    def approve(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise ValueError("Only pending orders can be approved")
        self.status = OrderStatus.APPROVED
        self.approved_at = datetime.now(timezone.utc)
        self.touch()

    def mark_delivered(self) -> None:
        self.status = OrderStatus.DELIVERED
        self.delivered_customer_date = datetime.now(timezone.utc)
        self.touch()

    def cancel(self) -> None:
        if self.status in (OrderStatus.DELIVERED, OrderStatus.CANCELLED):
            raise ValueError("Order cannot be cancelled")
        self.status = OrderStatus.CANCELLED
        self.touch()


class OrderItem(BaseEntity):
    def __init__(self, id=None, order_id="", product_id="", seller_id="",
                 price=0.0, freight_value=0.0, quantity=1):
        super().__init__()
        self.id = id or self.id
        self.order_id = order_id
        self.product_id = product_id
        self.seller_id = seller_id
        self.price = price
        self.freight_value = freight_value
        self.quantity = quantity

    @property
    def subtotal(self) -> float:
        return self.price * self.quantity


__all__ = ["OrderStatus", "Order", "OrderItem"]
