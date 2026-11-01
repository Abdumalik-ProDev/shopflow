"""Recommendations domain repository interface."""

from typing import List
from shopflow.modules.recommendations.domain.models.recommendation import ProductRecommendation


class RecommendationRepository:
    async def get_recommendations(self, customer_id: str, limit: int = 10) -> List[ProductRecommendation]:
        raise NotImplementedError


__all__ = ["RecommendationRepository"]
