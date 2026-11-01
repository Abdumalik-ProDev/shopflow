"""Recommendations application DTOs."""

from pydantic import BaseModel
from typing import List


class ProductRecommendationOut(BaseModel):
    product_id: str
    score: float
    reason: str


class RecommendationsResponse(BaseModel):
    customer_id: str
    recommendations: List[ProductRecommendationOut]


__all__ = ["ProductRecommendationOut", "RecommendationsResponse"]
