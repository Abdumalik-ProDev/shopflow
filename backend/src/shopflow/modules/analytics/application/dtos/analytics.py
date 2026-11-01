"""Analytics application DTOs."""

from pydantic import BaseModel
from typing import Optional


class KPIOut(BaseModel):
    label: str
    value: float
    delta: Optional[float] = None
    delta_percent: Optional[float] = None


class SalesPointOut(BaseModel):
    date: str
    sales: float
    orders: int


class TopProductOut(BaseModel):
    product_id: str
    name: str
    sales: float
    units: int


__all__ = ["KPIOut", "SalesPointOut", "TopProductOut"]
