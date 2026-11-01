"""Reviews application use cases."""

from __future__ import annotations

from shopflow.core.exceptions import NotFoundError
from shopflow.modules.reviews.application.dtos.review import ReviewCreate, ReviewOut
from shopflow.modules.reviews.domain.models.review import Review
from shopflow.modules.reviews.domain.repositories.review import ReviewRepository


class CreateReviewUseCase:
    def __init__(self, review_repo: ReviewRepository):
        self.review_repo = review_repo

    async def execute(self, dto: ReviewCreate) -> ReviewOut:
        review = Review(
            order_id=dto.order_id,
            review_score=dto.review_score,
            comment_title=dto.comment_title,
            comment_message=dto.comment_message,
        )
        await self.review_repo.add(review)
        return ReviewOut.model_validate(review)


class ListReviewsByOrderUseCase:
    def __init__(self, review_repo: ReviewRepository):
        self.review_repo = review_repo

    async def execute(self, order_id: str) -> list[ReviewOut]:
        reviews = await self.review_repo.list_by_order(order_id)
        return [ReviewOut.model_validate(r) for r in reviews]


__all__ = ["CreateReviewUseCase", "ListReviewsByOrderUseCase"]
