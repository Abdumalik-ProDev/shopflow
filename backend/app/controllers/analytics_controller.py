"""Analytics controller router."""

from fastapi import APIRouter

from app.controllers.deps import CurrentUserDep, SessionDep
from app.dtos.analytics import AnalyticsSummaryResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary(
    session: SessionDep,
    current_user: CurrentUserDep,
) -> AnalyticsSummaryResponse:
    service = AnalyticsService(session)
    return await service.get_summary()
