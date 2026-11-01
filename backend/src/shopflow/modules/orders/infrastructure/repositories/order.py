"""Orders infrastructure repository."""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from shopflow.modules.orders.domain.models.order import Order, OrderItem
from shopflow.modules.orders.domain.repositories.order import OrderRepository, OrderItemRepository
from shopflow.modules.orders.infrastructure.persistence.models import OrderRow, OrderItemRow


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, order: Order) -> None:
        self.session.add(OrderRow(
            id=order.id, customer_id=order.customer_id, status=order.status,
            purchase_timestamp=order.purchase_timestamp, approved_at=order.approved_at,
            delivered_carrier_date=order.delivered_carrier_date,
            delivered_customer_date=order.delivered_customer_date,
            estimated_delivery_date=order.estimated_delivery_date, total=order.total,
        ))
        await self.session.flush()

    async def get_by_id(self, order_id: str) -> Optional[Order]:
        row = await self.session.get(OrderRow, UUID(order_id))
        return self._to_domain(row) if row else None

    async def list(self, skip: int = 0, limit: int = 100,
                   customer_id: str | None = None, status: str | None = None) -> List[Order]:
        query = select(OrderRow)
        if customer_id:
            query = query.where(OrderRow.customer_id == UUID(customer_id))
        if status:
            query = query.where(OrderRow.status == status)
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return [self._to_domain(r) for r in result.scalars().all()]

    async def update(self, order: Order) -> None:
        row = await self.session.get(OrderRow, order.id)
        if not row: return
        row.customer_id = order.customer_id
        row.status = order.status
        row.purchase_timestamp = order.purchase_timestamp
        row.approved_at = order.approved_at
        row.delivered_carrier_date = order.delivered_carrier_date
        row.delivered_customer_date = order.delivered_customer_date
        row.estimated_delivery_date = order.estimated_delivery_date
        row.total = order.total
        await self.session.flush()

    async def delete(self, order_id: str) -> None:
        row = await self.session.get(OrderRow, UUID(order_id))
        if row: await self.session.delete(row)

    @staticmethod
    def _to_domain(row: OrderRow) -> Order:
        return Order(
            id=str(row.id), customer_id=str(row.customer_id), status=row.status,
            purchase_timestamp=row.purchase_timestamp, approved_at=row.approved_at,
            delivered_carrier_date=row.delivered_carrier_date,
            delivered_customer_date=row.delivered_customer_date,
            estimated_delivery_date=row.estimated_delivery_date, total=row.total,
        )


class SqlAlchemyOrderItemRepository(OrderItemRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, item: OrderItem) -> None:
        self.session.add(OrderItemRow(
            id=item.id, order_id=item.order_id, product_id=item.product_id,
            seller_id=item.seller_id, price=item.price,
            freight_value=item.freight_value, quantity=item.quantity,
        ))
        await self.session.flush()

    async def get_by_id(self, item_id: str) -> Optional[OrderItem]:
        row = await self.session.get(OrderItemRow, UUID(item_id))
        return self._to_domain(row) if row else None

    async def list_by_order(self, order_id: str) -> List[OrderItem]:
        result = await self.session.execute(
            select(OrderItemRow).where(OrderItemRow.order_id == UUID(order_id))
        )
        return [self._to_domain(r) for r in result.scalars().all()]

    async def update(self, item: OrderItem) -> None:
        row = await self.session.get(OrderItemRow, item.id)
        if not row: return
        row.product_id = item.product_id
        row.seller_id = item.seller_id
        row.price = item.price
        row.freight_value = item.freight_value
        row.quantity = item.quantity
        await self.session.flush()

    async def delete(self, item_id: str) -> None:
        row = await self.session.get(OrderItemRow, UUID(item_id))
        if row: await self.session.delete(row)

    @staticmethod
    def _to_domain(row: OrderItemRow) -> OrderItem:
        return OrderItem(
            id=str(row.id), order_id=str(row.order_id), product_id=row.product_id,
            seller_id=row.seller_id, price=row.price,
            freight_value=row.freight_value, quantity=row.quantity,
        )


__all__ = ["SqlAlchemyOrderRepository", "SqlAlchemyOrderItemRepository"]
