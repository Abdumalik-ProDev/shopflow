"""Product DTOs."""


from pydantic import BaseModel, ConfigDict, Field


class ProductCreateRequest(BaseModel):
    sku: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str | None = None
    price: float = Field(ge=0)
    stock_quantity: int = Field(default=0, ge=0)
    category_id: str | None = None
    seller_id: str | None = None
    is_active: bool = True
    weight_g: float | None = None
    length_cm: float | None = None
    height_cm: float | None = None
    width_cm: float | None = None
    photos_qty: int | None = None


class ProductUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, ge=0)
    stock_quantity: int | None = Field(default=None, ge=0)
    category_id: str | None = None
    seller_id: str | None = None
    is_active: bool | None = None


class ProductResponse(BaseModel):
    id: str
    sku: str
    name: str
    description: str | None = None
    price: float
    stock_quantity: int
    category_id: str | None = None
    seller_id: str | None = None
    is_active: bool
    weight_g: float | None = None
    length_cm: float | None = None
    height_cm: float | None = None
    width_cm: float | None = None
    photos_qty: int | None = None

    model_config = ConfigDict(from_attributes=True)


class StockAdjustRequest(BaseModel):
    delta: int = 0
