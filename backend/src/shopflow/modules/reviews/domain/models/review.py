"""Reviews domain models."""

from __future__ import annotations

from shopflow.shared.domain.base_entity import BaseEntity


class Review(BaseEntity):
    def __init__(
        self,
        id: str | None = None,
        order_id: str = "",
        review_score: int = 0,
        comment_title: str | None = None,
        comment_message: str | None = None,
    ):
        super().__init__()
        self.id = id or self.id
        self.order_id = order_id
        self.review_score = review_score
        self.comment_title = comment_title
        self.comment_message = comment_message


__all__ = ["Review"]
