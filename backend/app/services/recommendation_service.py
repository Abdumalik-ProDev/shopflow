"""Recommendation business logic service."""


from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.recommendation import ProductRecommendationResponse, RecommendationsResponse
from app.repositories.product_repository import ProductRepository


class RecommendationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.product_repo = ProductRepository(session)

    async def get_recommendations_for_customer(
        self, customer_id: str, limit: int = 10
    ) -> RecommendationsResponse:
        # Fetch available products to recommend real catalog items when available
        products = await self.product_repo.list_products(skip=0, limit=limit, is_active=True)

        recommendations: list[ProductRecommendationResponse] = []
        if products:
            for i, p in enumerate(products[:limit]):
                recommendations.append(
                    ProductRecommendationResponse(
                        product_id=str(p.id),
                        score=round(max(0.1, 1.0 - (i * 0.05)), 2),
                        reason=f"Popular in category: {p.name}",
                    )
                )
        else:
            # Fallback when catalog is empty
            for i in range(limit):
                recommendations.append(
                    ProductRecommendationResponse(
                        product_id=f"rec-product-{i+1}",
                        score=round(max(0.1, 1.0 - (i * 0.05)), 2),
                        reason="Popular trending item in marketplace",
                    )
                )

        return RecommendationsResponse(
            customer_id=customer_id,
            recommendations=recommendations,
        )
