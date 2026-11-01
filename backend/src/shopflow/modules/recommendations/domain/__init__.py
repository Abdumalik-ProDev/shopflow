"""Recommendations domain __init__."""

from shopflow.modules.recommendations.domain.models.recommendation import ProductRecommendation
from shopflow.modules.recommendations.domain.repositories.recommendation import RecommendationRepository

__all__ = ["ProductRecommendation", "RecommendationRepository"]
