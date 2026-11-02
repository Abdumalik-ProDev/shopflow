"""Payment DTOs."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreateRequest(BaseModel):
    order_id: str
    payment_sequential: int = Field(default=1, ge=1)
    payment_type: str = Field(default="credit_card")
    payment_installments: int = Field(default=1, ge=1)
    payment_value: float = Field(ge=0)


class PaymentResponse(BaseModel):
    id: str
    order_id: str
    payment_sequential: int
    payment_type: str
    payment_installments: int
    payment_value: float
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
