"""Recommendations module."""

from shopflow.modules.recommendations.domain.models.recommendation import ProductRecommendation
from shopflow.modules.recommendations.domain.repositories.recommendation import RecommendationRepository
from shopflow.modules.recommendations.application.services.recommendation import RecommendationService
from shopflow.modules.recommendations.infrastructure.repositories.recommendation import MLRecommendationRepository
from shopflow.modules.recommendations.api.controllers.recommendation import router as recommendations_router

__all__ = [
    "ProductRecommendation", "RecommendationRepository",
    "RecommendationService", "MLRecommendationRepository",
    "recommendations_router",
]
