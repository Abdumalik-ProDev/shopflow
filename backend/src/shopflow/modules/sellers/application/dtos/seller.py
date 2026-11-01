"""Sellers application DTOs."""

from pydantic import BaseModel, Field


class SellerCreate(BaseModel):
    seller_zip_code_prefix: str
    seller_city: str
    seller_state: str


class SellerUpdate(BaseModel):
    seller_zip_code_prefix: str | None = None
    seller_city: str | None = None
    seller_state: str | None = None


class SellerOut(BaseModel):
    id: str
    seller_zip_code_prefix: str
    seller_city: str
    seller_state: str
    user_id: str | None = None

    class Config:
        from_attributes = True


__all__ = ["SellerCreate", "SellerUpdate", "SellerOut"]
