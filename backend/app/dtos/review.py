"""Review DTOs."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewCreateRequest(BaseModel):
    order_id: str
    review_score: int = Field(ge=1, le=5)
    comment_title: str | None = None
    comment_message: str | None = None


class ReviewResponse(BaseModel):
    id: str
    order_id: str
    review_score: int
    comment_title: str | None = None
    comment_message: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
