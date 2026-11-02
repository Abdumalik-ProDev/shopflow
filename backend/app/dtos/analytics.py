"""Analytics DTOs."""


from pydantic import BaseModel, ConfigDict


class KPIResponse(BaseModel):
    label: str
    value: float


class SalesPointResponse(BaseModel):
    date: str
    sales: float
    orders: int


class AnalyticsSummaryResponse(BaseModel):
    kpis: list[KPIResponse]
    sales_over_time: list[SalesPointResponse]

    model_config = ConfigDict(from_attributes=True)
