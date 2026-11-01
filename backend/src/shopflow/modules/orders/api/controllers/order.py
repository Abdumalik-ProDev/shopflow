"""Orders API controllers."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.orders.api.schemas.order import (
    OrderCreateRequest, OrderResponse, OrderStatusUpdateRequest,
)
from shopflow.modules.orders.application.services.order import OrderService
from shopflow.modules.orders.infrastructure.repositories import (
    SqlAlchemyOrderRepository, SqlAlchemyOrderItemRepository,
)
from shopflow.modules.catalog.infrastructure.repositories import SqlAlchemyProductRepository

router = APIRouter(prefix="/orders", tags=["orders"])


def _service(session: AsyncSession = Depends(get_session)) -> OrderService:
    return OrderService(
        order_repo=SqlAlchemyOrderRepository(session),
        order_item_repo=SqlAlchemyOrderItemRepository(session),
        product_repo=SqlAlchemyProductRepository(session),
    )


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreateRequest, svc: OrderService = Depends(_service), session: AsyncSession = Depends(get_session)):
    order = await svc.create(payload)
    await session.commit()
    return OrderResponse.model_validate(order)


@router.get("", response_model=list[OrderResponse])
async def list_orders(
    skip: int = 0, limit: int = 100,
    customer_id: str | None = Query(None), status: str | None = Query(None),
    svc: OrderService = Depends(_service),
):
    return await svc.list(skip=skip, limit=limit, customer_id=customer_id, status=status)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, svc: OrderService = Depends(_service)):
    order = await svc.get_by_id(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse.model_validate(order)


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str, payload: OrderStatusUpdateRequest,
    svc: OrderService = Depends(_service), session: AsyncSession = Depends(get_session),
):
    order = await svc.update_status(order_id, payload)
    await session.commit()
    return OrderResponse.model_validate(order)


__all__ = ["router"]
