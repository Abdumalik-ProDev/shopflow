"""Analytics API controllers."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.analytics.api.schemas.analytics import (
    KPIResponse, SalesPointResponse, AnalyticsSummaryResponse,
)
from shopflow.modules.analytics.application.services.analytics import AnalyticsService
from shopflow.modules.orders.infrastructure.repositories import SqlAlchemyOrderRepository
from shopflow.modules.payments.infrastructure.repositories import SqlAlchemyPaymentRepository
from shopflow.modules.customers.infrastructure.repositories import SqlAlchemyCustomerRepository
from shopflow.modules.sellers.infrastructure.repositories import SqlAlchemySellerRepository
from shopflow.modules.catalog.infrastructure.repositories import SqlAlchemyProductRepository

router = APIRouter(prefix="/analytics", tags=["analytics"])


def _service(session: AsyncSession = Depends(get_session)) -> AnalyticsService:
    return AnalyticsService(
        order_repo=SqlAlchemyOrderRepository(session),
        payment_repo=SqlAlchemyPaymentRepository(session),
        customer_repo=SqlAlchemyCustomerRepository(session),
        seller_repo=SqlAlchemySellerRepository(session),
        product_repo=SqlAlchemyProductRepository(session),
    )


@router.get("/summary", response_model=AnalyticsSummaryResponse)
async def get_summary(svc: AnalyticsService = Depends(_service)):
    kpis = await svc.get_kpis()
    sales_over_time = await svc.get_sales_over_time()
    return AnalyticsSummaryResponse(
        kpis=[KPIResponse.model_validate(k) for k in kpis],
        sales_over_time=[SalesPointResponse.model_validate(s) for s in sales_over_time],
    )


__all__ = ["router"]
