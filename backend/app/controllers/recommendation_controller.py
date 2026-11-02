"""Recommendation controller router."""

from fastapi import APIRouter, Query

from app.controllers.deps import SessionDep
from app.dtos.recommendation import RecommendationsResponse
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/customer/{customer_id}", response_model=RecommendationsResponse)
async def get_recommendations_for_customer(
    customer_id: str,
    session: SessionDep,
    limit: int = Query(10, ge=1, le=50),
) -> RecommendationsResponse:
    service = RecommendationService(session)
    return await service.get_recommendations_for_customer(customer_id=customer_id, limit=limit)
