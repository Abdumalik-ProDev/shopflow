"""Payments API controllers."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.payments.api.schemas.payment import PaymentCreateRequest, PaymentResponse
from shopflow.modules.payments.application.services.payment import PaymentService
from shopflow.modules.payments.infrastructure.repositories import SqlAlchemyPaymentRepository

router = APIRouter(prefix="/payments", tags=["payments"])


def _service(session: AsyncSession = Depends(get_session)) -> PaymentService:
    return PaymentService(SqlAlchemyPaymentRepository(session))


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(payload: PaymentCreateRequest, svc: PaymentService = Depends(_service), session: AsyncSession = Depends(get_session)):
    p = await svc.create(payload)
    await session.commit()
    return PaymentResponse.model_validate(p)


@router.get("/order/{order_id}", response_model=list[PaymentResponse])
async def list_payments_by_order(order_id: str, svc: PaymentService = Depends(_service)):
    return await svc.list_by_order(order_id)


__all__ = ["router"]
