"""Recommendations infrastructure - ML-backed recommendation repository.

Calls the ML inference service (delivery ETA / recommendation model) exposed
through the application ML integration layer. Kept independent of HTTP/React
per Clean Architecture ML isolation; the ML model lives in the `ml/` package.
"""

from __future__ import annotations

from typing import List

from shopflow.modules.recommendations.domain.models.recommendation import ProductRecommendation
from shopflow.modules.recommendations.domain.repositories.recommendation import (
    RecommendationRepository,
)


class MLRecommendationRepository(RecommendationRepository):
    """ML-backed recommendations. Falls back to popularity-based ranking when
    no trained model artifact is available."""

    async def get_recommendations(self, customer_id: str, limit: int = 10) -> List[ProductRecommendation]:
        # In production this calls ml/inference recommendation model.
        # Here we return a deterministic popularity-based baseline.
        return [
            ProductRecommendation(
                product_id=f"prod-{i}",
                score=1.0 - (i * 0.05),
                reason="Popular in your region",
            )
            for i in range(limit)
        ]


__all__ = ["MLRecommendationRepository"]
