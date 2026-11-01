"""Reviews API controllers."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.reviews.api.schemas.review import ReviewCreateRequest, ReviewResponse
from shopflow.modules.reviews.application.services.review import ReviewService
from shopflow.modules.reviews.infrastructure.repositories import SqlAlchemyReviewRepository

router = APIRouter(prefix="/reviews", tags=["reviews"])


def _service(session: AsyncSession = Depends(get_session)) -> ReviewService:
    return ReviewService(SqlAlchemyReviewRepository(session))


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(payload: ReviewCreateRequest, svc: ReviewService = Depends(_service), session: AsyncSession = Depends(get_session)):
    r = await svc.create(payload)
    await session.commit()
    return ReviewResponse.model_validate(r)


@router.get("/order/{order_id}", response_model=list[ReviewResponse])
async def list_reviews_by_order(order_id: str, svc: ReviewService = Depends(_service)):
    return await svc.list_by_order(order_id)


__all__ = ["router"]
