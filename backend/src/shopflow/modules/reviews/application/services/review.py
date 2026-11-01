"""Reviews application service."""

from shopflow.core.exceptions import NotFoundError
from shopflow.modules.reviews.application.dtos.review import ReviewCreate, ReviewOut
from shopflow.modules.reviews.application.mappers.review import domain_to_dto, dto_to_domain
from shopflow.modules.reviews.domain.models.review import Review
from shopflow.modules.reviews.domain.repositories.review import ReviewRepository


class ReviewService:
    def __init__(self, review_repo: ReviewRepository):
        self.review_repo = review_repo

    async def create(self, dto: ReviewCreate) -> ReviewOut:
        review = dto_to_domain(dto)
        await self.review_repo.add(review)
        return domain_to_dto(review)

    async def list_by_order(self, order_id: str) -> list[ReviewOut]:
        reviews = await self.review_repo.list_by_order(order_id)
        return [domain_to_dto(r) for r in reviews]


__all__ = ["ReviewService"]
