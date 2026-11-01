"""Reviews mappers."""

from shopflow.modules.reviews.application.dtos.review import ReviewCreate, ReviewOut
from shopflow.modules.reviews.domain.models.review import Review


def domain_to_dto(r: Review) -> ReviewOut:
    return ReviewOut(
        id=str(r.id), order_id=str(r.order_id),
        review_score=r.review_score,
        comment_title=r.comment_title, comment_message=r.comment_message,
    )


def dto_to_domain(dto: ReviewCreate) -> Review:
    return Review(
        order_id=dto.order_id, review_score=dto.review_score,
        comment_title=dto.comment_title, comment_message=dto.comment_message,
    )


__all__ = ["domain_to_dto", "dto_to_domain"]
