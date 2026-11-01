"""Orders domain repository interfaces."""

from typing import Optional, List
from shopflow.modules.orders.domain.models.order import Order, OrderItem


class OrderRepository:
    async def add(self, order: Order) -> None: raise NotImplementedError
    async def get_by_id(self, order_id: str) -> Optional[Order]: raise NotImplementedError
    async def list(self, skip: int = 0, limit: int = 100,
                   customer_id: str | None = None, status: str | None = None) -> List[Order]: raise NotImplementedError
    async def update(self, order: Order) -> None: raise NotImplementedError
    async def delete(self, order_id: str) -> None: raise NotImplementedError


class OrderItemRepository:
    async def add(self, item: OrderItem) -> None: raise NotImplementedError
    async def get_by_id(self, item_id: str) -> Optional[OrderItem]: raise NotImplementedError
    async def list_by_order(self, order_id: str) -> List[OrderItem]: raise NotImplementedError
    async def update(self, item: OrderItem) -> None: raise NotImplementedError
    async def delete(self, item_id: str) -> None: raise NotImplementedError


__all__ = ["OrderRepository", "OrderItemRepository"]
