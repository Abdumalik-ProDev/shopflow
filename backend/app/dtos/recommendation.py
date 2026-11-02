"""Recommendation DTOs."""


from pydantic import BaseModel, ConfigDict


class ProductRecommendationResponse(BaseModel):
    product_id: str
    product_name: str | None = None
    price: float = 0.0
    category_name: str | None = None
    score: float
    reason: str


class RecommendationsResponse(BaseModel):
    customer_id: str
    recommendations: list[ProductRecommendationResponse]

    model_config = ConfigDict(from_attributes=True)
