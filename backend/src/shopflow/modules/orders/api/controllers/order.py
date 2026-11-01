"""Orders API controllers."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.orders.api.schemas.order import (
    OrderCreateRequest,
    OrderResponse,
    OrderStatusUpdateRequest,
)
from shopflow.modules.orders.application.use_cases.order import (
    CreateOrderUseCase,
    GetOrderUseCase,
    ListOrdersUseCase,
    UpdateOrderStatusUseCase,
)
from shopflow.modules.orders.infrastructure.repositories import (
    SqlAlchemyOrderRepository,
    SqlAlchemyOrderItemRepository,
)
from shopflow.modules.catalog.infrastructure.repositories import SqlAlchemyProductRepository

router = APIRouter(prefix="/orders", tags=["orders"])


def _order_repo(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyOrderRepository(session)


def _item_repo(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyOrderItemRepository(session)


def _product_repo(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyProductRepository(session)


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: OrderCreateRequest,
    order_repo=Depends(_order_repo),
    item_repo=Depends(_item_repo),
    product_repo=Depends(_product_repo),
    session: AsyncSession = Depends(get_session),
):
    use_case = CreateOrderUseCase(order_repo, item_repo, product_repo)
    order = await use_case.execute(payload)
    await session.commit()
    return OrderResponse.model_validate(order)


@router.get("", response_model=list[OrderResponse])
async def list_orders(
    skip: int = 0,
    limit: int = 100,
    customer_id: str | None = Query(None),
    status: str | None = Query(None),
    order_repo=Depends(_order_repo),
):
    use_case = ListOrdersUseCase(order_repo)
    return await use_case.execute(skip=skip, limit=limit, customer_id=customer_id, status=status)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, order_repo=Depends(_order_repo), item_repo=Depends(_item_repo)):
    use_case = GetOrderUseCase(order_repo, item_repo)
    order = await use_case.execute(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse.model_validate(order)


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    payload: OrderStatusUpdateRequest,
    order_repo=Depends(_order_repo),
    session: AsyncSession = Depends(get_session),
):
    use_case = UpdateOrderStatusUseCase(order_repo)
    order = await use_case.execute(order_id, payload)
    await session.commit()
    return OrderResponse.model_validate(order)


__all__ = ["router"]
