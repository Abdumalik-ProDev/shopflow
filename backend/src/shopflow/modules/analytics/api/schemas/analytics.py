"""Analytics API schemas."""

from pydantic import BaseModel
from typing import Optional, List


class KPIResponse(BaseModel):
    label: str
    value: float
    delta: Optional[float] = None
    delta_percent: Optional[float] = None


class SalesPointResponse(BaseModel):
    date: str
    sales: float
    orders: int


class AnalyticsSummaryResponse(BaseModel):
    kpis: List[KPIResponse]
    sales_over_time: List[SalesPointResponse]


__all__ = ["KPIResponse", "SalesPointResponse", "AnalyticsSummaryResponse"]
