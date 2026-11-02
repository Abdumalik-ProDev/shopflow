"""Recommendation DTOs."""


from pydantic import BaseModel, ConfigDict


class ProductRecommendationResponse(BaseModel):
    product_id: str
    score: float
    reason: str


class RecommendationsResponse(BaseModel):
    customer_id: str
    recommendations: list[ProductRecommendationResponse]

    model_config = ConfigDict(from_attributes=True)
