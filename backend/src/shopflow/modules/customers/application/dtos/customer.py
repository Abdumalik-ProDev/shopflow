"""Customers application DTOs."""

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    customer_unique_id: str = Field(min_length=1)
    customer_zip_code_prefix: str
    customer_city: str
    customer_state: str


class CustomerUpdate(BaseModel):
    customer_zip_code_prefix: str | None = None
    customer_city: str | None = None
    customer_state: str | None = None


class CustomerOut(BaseModel):
    id: str
    customer_unique_id: str
    customer_zip_code_prefix: str
    customer_city: str
    customer_state: str
    user_id: str | None = None

    class Config:
        from_attributes = True


__all__ = ["CustomerCreate", "CustomerUpdate", "CustomerOut"]
