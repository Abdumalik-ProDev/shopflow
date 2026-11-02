"""Order repository for persistence operations."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order, OrderItem
from app.models.product import Product


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, order_id: uuid.UUID) -> Order | None:
        query = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                selectinload(Order.items),
                selectinload(Order.payments),
                selectinload(Order.reviews),
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_orders(
        self,
        skip: int = 0,
        limit: int = 100,
        customer_id: uuid.UUID | None = None,
        status: str | None = None,
    ) -> list[Order]:
        query = (
            select(Order)
            .options(
                selectinload(Order.items),
                selectinload(Order.payments),
                selectinload(Order.reviews),
            )
        )
        if customer_id:
            query = query.where(Order.customer_id == customer_id)
        if status:
            query = query.where(Order.status == status)
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(
        self,
        customer_id: uuid.UUID,
        items_data: list[dict],
        estimated_delivery_date: datetime | None = None,
    ) -> Order:
        order = Order(
            customer_id=customer_id,
            status="pending",
            purchase_timestamp=datetime.now(timezone.utc),
            estimated_delivery_date=estimated_delivery_date,
            total=0.0,
        )
        self.session.add(order)
        await self.session.flush()

        total = 0.0
        for it in items_data:
            item = OrderItem(
                order_id=order.id,
                product_id=it["product_id"],
                seller_id=it["seller_id"],
                price=it["price"],
                freight_value=it.get("freight_value", 0.0),
                quantity=it.get("quantity", 1),
            )
            self.session.add(item)
            total += item.price * item.quantity

            # Decrement stock if product exists
            try:
                prod_uuid = uuid.UUID(it["product_id"])
                prod = await self.session.get(Product, prod_uuid)
                if prod:
                    prod.stock_quantity = max(0, prod.stock_quantity - item.quantity)
            except (ValueError, TypeError):
                pass

        order.total = round(total, 2)
        await self.session.flush()

        # Eagerly reload with items loaded
        loaded_order = await self.get_by_id(order.id)
        return loaded_order or order

    async def update_status(self, order: Order, new_status: str) -> Order:
        order.status = new_status
        if new_status == "delivered":
            order.delivered_customer_date = datetime.now(timezone.utc)
        await self.session.flush()
        loaded_order = await self.get_by_id(order.id)
        return loaded_order or order
