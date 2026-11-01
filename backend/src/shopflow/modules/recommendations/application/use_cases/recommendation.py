"""Recommendations application use cases - integrates ML inference into business workflows."""

from __future__ import annotations

from typing import List

from shopflow.modules.recommendations.application.dtos.recommendation import (
    ProductRecommendationOut,
    RecommendationsResponse,
)
from shopflow.modules.recommendations.domain.models.recommendation import ProductRecommendation
from shopflow.modules.recommendations.domain.repositories.recommendation import (
    RecommendationRepository,
)


class GetRecommendationsUseCase:
    def __init__(self, recommendation_repo: RecommendationRepository):
        self.recommendation_repo = recommendation_repo

    async def execute(self, customer_id: str, limit: int = 10) -> RecommendationsResponse:
        recommendations = await self.recommendation_repo.get_recommendations(
            customer_id, limit=limit
        )
        return RecommendationsResponse(
            customer_id=customer_id,
            recommendations=[
                ProductRecommendationOut(
                    product_id=r.product_id,
                    score=r.score,
                    reason=r.reason,
                )
                for r in recommendations
            ],
        )


__all__ = ["GetRecommendationsUseCase"]
