"""Order and OrderItem DTOs."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreateRequest(BaseModel):
    product_id: str
    seller_id: str
    price: float = Field(ge=0)
    freight_value: float = Field(default=0, ge=0)
    quantity: int = Field(default=1, ge=1)


class OrderCreateRequest(BaseModel):
    customer_id: str
    items: list[OrderItemCreateRequest]
    estimated_delivery_date: datetime | None = None


class OrderItemResponse(BaseModel):
    id: str
    order_id: str
    product_id: str
    seller_id: str
    price: float
    freight_value: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: str
    customer_id: str
    status: str
    purchase_timestamp: datetime | None = None
    approved_at: datetime | None = None
    delivered_carrier_date: datetime | None = None
    delivered_customer_date: datetime | None = None
    estimated_delivery_date: datetime | None = None
    total: float
    items: list[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdateRequest(BaseModel):
    status: str
