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


class DeliveryEtaRequest(BaseModel):
    item_count: int = 1
    freight_total: float = 15.0
    customer_state: str = "SP"


class DeliveryEtaResponse(BaseModel):
    predicted_eta_days: float
    confidence_interval_days: float
    model_version: str
    delivery_status: str
