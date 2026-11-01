"""Orders domain models."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from shopflow.shared.domain.base_entity import BaseEntity


class OrderStatus(str):
    PENDING = "pending"
    APPROVED = "approved"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(BaseEntity):
    def __init__(
        self,
        id: str | None = None,
        customer_id: str = "",
        status: str = OrderStatus.PENDING,
        purchase_timestamp: Optional[datetime] = None,
        approved_at: Optional[datetime] = None,
        delivered_carrier_date: Optional[datetime] = None,
        delivered_customer_date: Optional[datetime] = None,
        estimated_delivery_date: Optional[datetime] = None,
        total: float = 0.0,
    ):
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
        self.approved_at = datetime.now()
        self.touch()

    def mark_delivered(self) -> None:
        self.status = OrderStatus.DELIVERED
        self.delivered_customer_date = datetime.now()
        self.touch()

    def cancel(self) -> None:
        if self.status in (OrderStatus.DELIVERED, OrderStatus.CANCELLED):
            raise ValueError("Order cannot be cancelled")
        self.status = OrderStatus.CANCELLED
        self.touch()


class OrderItem(BaseEntity):
    def __init__(
        self,
        id: str | None = None,
        order_id: str = "",
        product_id: str = "",
        seller_id: str = "",
        price: float = 0.0,
        freight_value: float = 0.0,
        quantity: int = 1,
    ):
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
