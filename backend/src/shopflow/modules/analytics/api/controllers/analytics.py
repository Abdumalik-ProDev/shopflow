"""Analytics API controllers."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.analytics.api.schemas.analytics import (
    KPIResponse,
    SalesPointResponse,
    AnalyticsSummaryResponse,
)
from shopflow.modules.analytics.application.use_cases.analytics import (
    GetKPIsUseCase,
    GetSalesOverTimeUseCase,
)
from shopflow.modules.orders.infrastructure.repositories import SqlAlchemyOrderRepository
from shopflow.modules.payments.infrastructure.repositories import SqlAlchemyPaymentRepository
from shopflow.modules.customers.infrastructure.repositories import SqlAlchemyCustomerRepository
from shopflow.modules.sellers.infrastructure.repositories import SqlAlchemySellerRepository
from shopflow.modules.catalog.infrastructure.repositories import SqlAlchemyProductRepository

router = APIRouter(prefix="/analytics", tags=["analytics"])


def _session_dep(session: AsyncSession = Depends(get_session)):
    return session


@router.get("/summary", response_model=AnalyticsSummaryResponse)
async def get_summary(session: AsyncSession = Depends(get_session)):
    kpi_use_case = GetKPIsUseCase(
        order_repo=SqlAlchemyOrderRepository(session),
        payment_repo=SqlAlchemyPaymentRepository(session),
        customer_repo=SqlAlchemyCustomerRepository(session),
        seller_repo=SqlAlchemySellerRepository(session),
        product_repo=SqlAlchemyProductRepository(session),
    )
    kpis = await kpi_use_case.execute()

    sales_use_case = GetSalesOverTimeUseCase(order_repo=SqlAlchemyOrderRepository(session))
    sales_over_time = await sales_use_case.execute()

    return AnalyticsSummaryResponse(
        kpis=[KPIResponse.model_validate(k) for k in kpis],
        sales_over_time=[SalesPointResponse.model_validate(s) for s in sales_over_time],
    )


__all__ = ["router"]
