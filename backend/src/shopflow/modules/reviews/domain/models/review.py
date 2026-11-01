"""Reviews domain models."""

from shopflow.shared.domain.base_entity import BaseEntity


class Review(BaseEntity):
    def __init__(self, id=None, order_id="", review_score=0,
                 comment_title=None, comment_message=None):
        super().__init__()
        self.id = id or self.id
        self.order_id = order_id
        self.review_score = review_score
        self.comment_title = comment_title
        self.comment_message = comment_message


__all__ = ["Review"]
