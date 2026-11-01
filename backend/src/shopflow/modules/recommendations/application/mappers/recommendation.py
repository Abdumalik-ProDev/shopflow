"""Recommendations mappers."""

from shopflow.modules.recommendations.application.dtos.recommendation import (
    ProductRecommendationOut, RecommendationsResponse,
)
from shopflow.modules.recommendations.domain.models.recommendation import ProductRecommendation


def domain_to_dto(r: ProductRecommendation) -> ProductRecommendationOut:
    return ProductRecommendationOut(
        product_id=r.product_id, score=r.score, reason=r.reason,
    )


__all__ = ["domain_to_dto"]
