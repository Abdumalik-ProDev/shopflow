"""Order, Payment, and Review controller router."""

import uuid

from fastapi import APIRouter, Query, status

from app.controllers.deps import OptionalUserDep, SessionDep
from app.dtos.order import (
    OrderCreateRequest,
    OrderResponse,
    OrderStatusUpdateRequest,
)
from app.dtos.payment import PaymentCreateRequest, PaymentResponse
from app.dtos.review import ReviewCreateRequest, ReviewResponse
from app.services.order_service import OrderService

router = APIRouter(tags=["Orders & Checkout"])


# Orders
@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: OrderCreateRequest,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> OrderResponse:
    service = OrderService(session)
    order_dto = await service.create_order(payload)
    await session.commit()
    return order_dto


@router.get("/orders", response_model=list[OrderResponse])
async def list_orders(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    customer_id: str | None = Query(None),
    status_filter: str | None = Query(None, alias="status"),
    current_user: OptionalUserDep = None,
) -> list[OrderResponse]:
    service = OrderService(session)
    return await service.list_orders(
        skip=skip, limit=limit, customer_id=customer_id, status_filter=status_filter
    )


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: uuid.UUID,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> OrderResponse:
    service = OrderService(session)
    return await service.get_order(order_id)


@router.patch("/orders/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: uuid.UUID,
    payload: OrderStatusUpdateRequest,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> OrderResponse:
    service = OrderService(session)
    order_dto = await service.update_status(order_id, payload)
    await session.commit()
    return order_dto


# Payments
@router.post("/payments", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payload: PaymentCreateRequest,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> PaymentResponse:
    service = OrderService(session)
    payment_dto = await service.create_payment(payload)
    await session.commit()
    return payment_dto


@router.get("/payments/order/{order_id}", response_model=list[PaymentResponse])
async def list_payments_by_order(
    order_id: uuid.UUID,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> list[PaymentResponse]:
    service = OrderService(session)
    return await service.list_payments_by_order(order_id)


# Reviews
@router.post("/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    payload: ReviewCreateRequest,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> ReviewResponse:
    service = OrderService(session)
    review_dto = await service.create_review(payload)
    await session.commit()
    return review_dto


@router.get("/reviews/order/{order_id}", response_model=list[ReviewResponse])
async def list_reviews_by_order(
    order_id: uuid.UUID,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> list[ReviewResponse]:
    service = OrderService(session)
    return await service.list_reviews_by_order(order_id)
