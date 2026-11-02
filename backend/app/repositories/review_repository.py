"""Review repository for persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review


class ReviewRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, review: Review) -> Review:
        self.session.add(review)
        await self.session.flush()
        return review

    async def list_by_order(self, order_id: uuid.UUID) -> list[Review]:
        result = await self.session.execute(
            select(Review).where(Review.order_id == order_id)
        )
        return list(result.scalars().all())
