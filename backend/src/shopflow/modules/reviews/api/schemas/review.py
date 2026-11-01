"""Reviews API schemas."""

from pydantic import BaseModel, Field
from typing import Optional


class ReviewCreateRequest(BaseModel):
    order_id: str
    review_score: int = Field(ge=1, le=5)
    comment_title: Optional[str] = None
    comment_message: Optional[str] = None


class ReviewResponse(BaseModel):
    id: str
    order_id: str
    review_score: int
    comment_title: Optional[str]
    comment_message: Optional[str]

    class Config:
        from_attributes = True


__all__ = ["ReviewCreateRequest", "ReviewResponse"]
