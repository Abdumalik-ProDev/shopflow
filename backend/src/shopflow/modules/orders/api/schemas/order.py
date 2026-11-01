"""Orders API schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class OrderItemCreateRequest(BaseModel):
    product_id: str
    seller_id: str
    price: float = Field(ge=0)
    freight_value: float = Field(default=0, ge=0)
    quantity: int = Field(default=1, ge=1)


class OrderCreateRequest(BaseModel):
    customer_id: str
    items: List[OrderItemCreateRequest]
    estimated_delivery_date: Optional[datetime] = None


class OrderItemResponse(BaseModel):
    id: str
    order_id: str
    product_id: str
    seller_id: str
    price: float
    freight_value: float
    quantity: int

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: str
    customer_id: str
    status: str
    purchase_timestamp: Optional[datetime]
    approved_at: Optional[datetime]
    delivered_customer_date: Optional[datetime]
    estimated_delivery_date: Optional[datetime]
    total: float
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


class OrderStatusUpdateRequest(BaseModel):
    status: str


__all__ = [
    "OrderItemCreateRequest",
    "OrderCreateRequest",
    "OrderItemResponse",
    "OrderResponse",
    "OrderStatusUpdateRequest",
]
