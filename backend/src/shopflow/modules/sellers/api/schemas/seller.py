"""Sellers API schemas."""

from pydantic import BaseModel, Field


class SellerCreateRequest(BaseModel):
    seller_zip_code_prefix: str
    seller_city: str
    seller_state: str


class SellerUpdateRequest(BaseModel):
    seller_zip_code_prefix: str | None = None
    seller_city: str | None = None
    seller_state: str | None = None


class SellerResponse(BaseModel):
    id: str
    seller_zip_code_prefix: str
    seller_city: str
    seller_state: str
    user_id: str | None = None

    class Config:
        from_attributes = True


__all__ = ["SellerCreateRequest", "SellerUpdateRequest", "SellerResponse"]
