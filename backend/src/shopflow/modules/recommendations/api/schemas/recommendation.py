"""Recommendations API schemas."""

from pydantic import BaseModel
from typing import List


class ProductRecommendationResponse(BaseModel):
    product_id: str
    score: float
    reason: str


class RecommendationsResponse(BaseModel):
    customer_id: str
    recommendations: List[ProductRecommendationResponse]


__all__ = ["ProductRecommendationResponse", "RecommendationsResponse"]
