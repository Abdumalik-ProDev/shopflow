"""Reviews infrastructure repository."""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from shopflow.modules.reviews.domain.models.review import Review
from shopflow.modules.reviews.domain.repositories.review import ReviewRepository
from shopflow.modules.reviews.infrastructure.persistence.models import ReviewRow


class SqlAlchemyReviewRepository(ReviewRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, review: Review) -> None:
        self.session.add(ReviewRow(
            id=review.id, order_id=review.order_id,
            review_score=review.review_score,
            comment_title=review.comment_title,
            comment_message=review.comment_message,
        ))
        await self.session.flush()

    async def get_by_id(self, review_id: str) -> Optional[Review]:
        row = await self.session.get(ReviewRow, UUID(review_id))
        return self._to_domain(row) if row else None

    async def list_by_order(self, order_id: str) -> List[Review]:
        result = await self.session.execute(
            select(ReviewRow).where(ReviewRow.order_id == UUID(order_id))
        )
        return [self._to_domain(r) for r in result.scalars().all()]

    async def update(self, review: Review) -> None:
        row = await self.session.get(ReviewRow, review.id)
        if not row: return
        row.order_id = review.order_id
        row.review_score = review.review_score
        row.comment_title = review.comment_title
        row.comment_message = review.comment_message
        await self.session.flush()

    @staticmethod
    def _to_domain(row: ReviewRow) -> Review:
        return Review(
            id=str(row.id), order_id=str(row.order_id),
            review_score=row.review_score,
            comment_title=row.comment_title, comment_message=row.comment_message,
        )


__all__ = ["SqlAlchemyReviewRepository"]
