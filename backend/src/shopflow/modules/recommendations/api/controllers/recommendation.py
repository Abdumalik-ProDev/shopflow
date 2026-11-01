"""Recommendations API controllers."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.recommendations.api.schemas.recommendation import (
    ProductRecommendationResponse,
    RecommendationsResponse,
)
from shopflow.modules.recommendations.application.use_cases.recommendation import (
    GetRecommendationsUseCase,
)
from shopflow.modules.recommendations.infrastructure.repositories.recommendation import (
    MLRecommendationRepository,
)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def _repo(session: AsyncSession = Depends(get_session)):
    return MLRecommendationRepository()


@router.get("/customer/{customer_id}", response_model=RecommendationsResponse)
async def get_recommendations(
    customer_id: str,
    limit: int = Query(10, ge=1, le=50),
    repo=Depends(_repo),
):
    use_case = GetRecommendationsUseCase(repo)
    return await use_case.execute(customer_id, limit=limit)


__all__ = ["router"]
