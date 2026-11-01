"""Reviews domain repository interface."""

from typing import Optional, List
from shopflow.modules.reviews.domain.models.review import Review


class ReviewRepository:
    async def add(self, review: Review) -> None: raise NotImplementedError
    async def get_by_id(self, review_id: str) -> Optional[Review]: raise NotImplementedError
    async def list_by_order(self, order_id: str) -> List[Review]: raise NotImplementedError
    async def update(self, review: Review) -> None: raise NotImplementedError


__all__ = ["ReviewRepository"]
