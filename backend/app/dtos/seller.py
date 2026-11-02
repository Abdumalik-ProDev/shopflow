"""Seller DTOs."""


from pydantic import BaseModel, ConfigDict


class SellerCreateRequest(BaseModel):
    seller_zip_code_prefix: str = ""
    seller_city: str = ""
    seller_state: str = ""
    user_id: str | None = None


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

    model_config = ConfigDict(from_attributes=True)
