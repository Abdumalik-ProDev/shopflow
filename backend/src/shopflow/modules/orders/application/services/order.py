"""Orders application service."""

from datetime import datetime, timezone
from typing import List

from shopflow.core.exceptions import ConflictError, NotFoundError
from shopflow.modules.orders.application.dtos.order import (
    OrderCreate, OrderOut, OrderItemCreate, OrderItemOut, OrderStatusUpdate,
)
from shopflow.modules.orders.domain.models.order import Order, OrderItem, OrderStatus
from shopflow.modules.orders.domain.repositories.order import (
    OrderRepository, OrderItemRepository,
)
from shopflow.modules.catalog.domain.repositories.catalog import ProductRepository


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        order_item_repo: OrderItemRepository,
        product_repo: ProductRepository,
    ):
        self.order_repo = order_repo
        self.order_item_repo = order_item_repo
        self.product_repo = product_repo

    async def create(self, dto: OrderCreate) -> OrderOut:
        order = Order(
            customer_id=dto.customer_id,
            status=OrderStatus.PENDING,
            purchase_timestamp=datetime.now(timezone.utc),
            estimated_delivery_date=dto.estimated_delivery_date,
            total=0.0,
        )
        await self.order_repo.add(order)

        total = 0.0
        for item_dto in dto.items:
            product = await self.product_repo.get_by_id(item_dto.product_id)
            if product is None:
                raise NotFoundError(f"Product {item_dto.product_id} not found", code="PRODUCT_NOT_FOUND")
            if not product.is_active:
                raise ConflictError(f"Product {item_dto.product_id} is not active", code="PRODUCT_INACTIVE")
            if product.stock_quantity < item_dto.quantity:
                raise ConflictError(f"Insufficient stock for {item_dto.product_id}", code="INSUFFICIENT_STOCK")

            item = OrderItem(
                order_id=str(order.id),
                product_id=item_dto.product_id,
                seller_id=item_dto.seller_id,
                price=item_dto.price,
                freight_value=item_dto.freight_value,
                quantity=item_dto.quantity,
            )
            await self.order_item_repo.add(item)
            total += item.subtotal

            product.adjust_stock(-item_dto.quantity)

        order.total = total
        await self.order_repo.update(order)
        return await self.get_by_id(str(order.id))

    async def get_by_id(self, order_id: str) -> OrderOut | None:
        order = await self.order_repo.get_by_id(order_id)
        if order is None:
            return None
        items = await self.order_item_repo.list_by_order(order_id)
        return OrderOut(
            id=str(order.id), customer_id=order.customer_id, status=order.status,
            purchase_timestamp=order.purchase_timestamp, approved_at=order.approved_at,
            delivered_customer_date=order.delivered_customer_date,
            estimated_delivery_date=order.estimated_delivery_date,
            total=order.total,
            items=[
                OrderItemOut(
                    id=str(i.id), order_id=str(i.order_id),
                    product_id=i.product_id, seller_id=i.seller_id,
                    price=i.price, freight_value=i.freight_value, quantity=i.quantity,
                )
                for i in items
            ],
        )

    async def list(self, skip: int = 0, limit: int = 100,
                   customer_id: str | None = None, status: str | None = None) -> list[OrderOut]:
        orders = await self.order_repo.list(
            skip=skip, limit=limit, customer_id=customer_id, status=status,
        )
        result: list[OrderOut] = []
        for o in orders:
            items = await self.order_item_repo.list_by_order(str(o.id))
            result.append(OrderOut(
                id=str(o.id), customer_id=o.customer_id, status=o.status,
                purchase_timestamp=o.purchase_timestamp, approved_at=o.approved_at,
                delivered_customer_date=o.delivered_customer_date,
                estimated_delivery_date=o.estimated_delivery_date,
                total=o.total,
                items=[
                    OrderItemOut(
                        id=str(i.id), order_id=str(i.order_id),
                        product_id=i.product_id, seller_id=i.seller_id,
                        price=i.price, freight_value=i.freight_value, quantity=i.quantity,
                    )
                    for i in items
                ],
            ))
        return result

    async def update_status(self, order_id: str, dto: OrderStatusUpdate) -> OrderOut | None:
        order = await self.order_repo.get_by_id(order_id)
        if order is None:
            raise NotFoundError("Order not found", code="ORDER_NOT_FOUND")
        order.status = dto.status
        if dto.status == OrderStatus.DELIVERED:
            order.mark_delivered()
        elif dto.status == OrderStatus.CANCELLED:
            order.cancel()
        await self.order_repo.update(order)
        return await self.get_by_id(order_id)


__all__ = ["OrderService"]
