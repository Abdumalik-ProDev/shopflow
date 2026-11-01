"""Payments API controllers."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.payments.api.schemas.payment import PaymentCreateRequest, PaymentResponse
from shopflow.modules.payments.application.use_cases.payment import (
    CreatePaymentUseCase,
    ListPaymentsByOrderUseCase,
)
from shopflow.modules.payments.infrastructure.repositories import SqlAlchemyPaymentRepository

router = APIRouter(prefix="/payments", tags=["payments"])


def _repo(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyPaymentRepository(session)


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payload: PaymentCreateRequest, repo=Depends(_repo), session: AsyncSession = Depends(get_session)
):
    use_case = CreatePaymentUseCase(repo)
    payment = await use_case.execute(payload)
    await session.commit()
    return PaymentResponse.model_validate(payment)


@router.get("/order/{order_id}", response_model=list[PaymentResponse])
async def list_payments_by_order(order_id: str, repo=Depends(_repo)):
    use_case = ListPaymentsByOrderUseCase(repo)
    return await use_case.execute(order_id)


__all__ = ["router"]
