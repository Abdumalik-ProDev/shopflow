"""Recommendations API controllers."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.recommendations.api.schemas.recommendation import (
    ProductRecommendationResponse, RecommendationsResponse,
)
from shopflow.modules.recommendations.application.services.recommendation import RecommendationService
from shopflow.modules.recommendations.infrastructure.repositories.recommendation import MLRecommendationRepository

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def _service() -> RecommendationService:
    return RecommendationService(MLRecommendationRepository())


@router.get("/customer/{customer_id}", response_model=RecommendationsResponse)
async def get_recommendations(
    customer_id: str,
    limit: int = Query(10, ge=1, le=50),
    svc: RecommendationService = Depends(_service),
):
    return await svc.get_for_customer(customer_id, limit=limit)


__all__ = ["router"]
