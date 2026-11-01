"""Catalog application DTOs."""

from pydantic import BaseModel, Field
from typing import Optional


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)
    name_english: Optional[str] = None


class CategoryOut(BaseModel):
    id: str
    name: str
    name_english: Optional[str] = None

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    sku: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: Optional[str] = None
    price: float = Field(ge=0)
    stock_quantity: int = Field(default=0, ge=0)
    category_id: Optional[str] = None
    seller_id: Optional[str] = None
    is_active: bool = True
    weight_g: Optional[float] = None
    length_cm: Optional[float] = None
    height_cm: Optional[float] = None
    width_cm: Optional[float] = None
    photos_qty: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)
    stock_quantity: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[str] = None
    seller_id: Optional[str] = None
    is_active: Optional[bool] = None


class ProductOut(BaseModel):
    id: str
    sku: str
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int
    category_id: Optional[str]
    seller_id: Optional[str]
    is_active: bool
    weight_g: Optional[float]
    length_cm: Optional[float]
    height_cm: Optional[float]
    width_cm: Optional[float]
    photos_qty: Optional[int]

    class Config:
        from_attributes = True


__all__ = ["CategoryCreate", "CategoryOut", "ProductCreate", "ProductUpdate", "ProductOut"]
