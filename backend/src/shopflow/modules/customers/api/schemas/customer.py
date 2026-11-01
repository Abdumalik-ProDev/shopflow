"""Customers API schemas."""

from pydantic import BaseModel, Field


class CustomerCreateRequest(BaseModel):
    customer_unique_id: str = Field(min_length=1)
    customer_zip_code_prefix: str
    customer_city: str
    customer_state: str


class CustomerUpdateRequest(BaseModel):
    customer_zip_code_prefix: str | None = None
    customer_city: str | None = None
    customer_state: str | None = None


class CustomerResponse(BaseModel):
    id: str
    customer_unique_id: str
    customer_zip_code_prefix: str
    customer_city: str
    customer_state: str
    user_id: str | None = None

    class Config:
        from_attributes = True


__all__ = ["CustomerCreateRequest", "CustomerUpdateRequest", "CustomerResponse"]
