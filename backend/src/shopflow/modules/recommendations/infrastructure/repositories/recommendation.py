"""Recommendations infrastructure - ML-backed recommendation repository."""

from typing import List

from shopflow.modules.recommendations.domain.models.recommendation import ProductRecommendation
from shopflow.modules.recommendations.domain.repositories.recommendation import RecommendationRepository


class MLRecommendationRepository(RecommendationRepository):
    """ML-backed recommendations with popularity baseline fallback."""

    async def get_recommendations(self, customer_id: str, limit: int = 10) -> List[ProductRecommendation]:
        # Deterministic popularity baseline. Replace with trained model inference.
        return [
            ProductRecommendation(
                product_id=f"prod-{i}",
                score=round(1.0 - (i * 0.05), 2),
                reason="Popular in your region",
            )
            for i in range(limit)
        ]


__all__ = ["MLRecommendationRepository"]
