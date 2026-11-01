"""Reviews API controllers."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.reviews.api.schemas.review import ReviewCreateRequest, ReviewResponse
from shopflow.modules.reviews.application.use_cases.review import (
    CreateReviewUseCase,
    ListReviewsByOrderUseCase,
)
from shopflow.modules.reviews.infrastructure.repositories import SqlAlchemyReviewRepository

router = APIRouter(prefix="/reviews", tags=["reviews"])


def _repo(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyReviewRepository(session)


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    payload: ReviewCreateRequest, repo=Depends(_repo), session: AsyncSession = Depends(get_session)
):
    use_case = CreateReviewUseCase(repo)
    review = await use_case.execute(payload)
    await session.commit()
    return ReviewResponse.model_validate(review)


@router.get("/order/{order_id}", response_model=list[ReviewResponse])
async def list_reviews_by_order(order_id: str, repo=Depends(_repo)):
    use_case = ListReviewsByOrderUseCase(repo)
    return await use_case.execute(order_id)


__all__ = ["router"]
