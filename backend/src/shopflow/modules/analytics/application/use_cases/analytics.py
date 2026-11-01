"""Analytics application use cases (read-only aggregations)."""

from __future__ import annotations

from shopflow.modules.analytics.application.dtos.analytics import (
    KPIOut,
    SalesPointOut,
    TopProductOut,
)
from shopflow.modules.orders.domain.repositories.order import OrderRepository
from shopflow.modules.payments.domain.repositories.payment import PaymentRepository
from shopflow.modules.customers.domain.repositories.customer import CustomerRepository
from shopflow.modules.sellers.domain.repositories.seller import SellerRepository
from shopflow.modules.catalog.domain.repositories.catalog import ProductRepository


class GetKPIsUseCase:
    def __init__(
        self,
        order_repo: OrderRepository,
        payment_repo: PaymentRepository,
        customer_repo: CustomerRepository,
        seller_repo: SellerRepository,
        product_repo: ProductRepository,
    ):
        self.order_repo = order_repo
        self.payment_repo = payment_repo
        self.customer_repo = customer_repo
        self.seller_repo = seller_repo
        self.product_repo = product_repo

    async def execute(self) -> list[KPIOut]:
        orders = await self.order_repo.list()
        customers = await self.customer_repo.list()
        sellers = await self.seller_repo.list()
        products = await self.product_repo.list()

        total_sales = sum(o.total for o in orders)
        delivered = [o for o in orders if o.status == "delivered"]
        gmv = sum(o.total for o in delivered)

        return [
            KPIOut(label="Total Orders", value=float(len(orders))),
            KPIOut(label="GMV (Delivered)", value=float(gmv)),
            KPIOut(label="Customers", value=float(len(customers))),
            KPIOut(label="Sellers", value=float(len(sellers))),
            KPIOut(label="Products", value=float(len(products))),
            KPIOut(label="Conversion Rate", value=float(len(delivered) / max(len(orders), 1) * 100)),
        ]


class GetSalesOverTimeUseCase:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    async def execute(self) -> list[SalesPointOut]:
        orders = await self.order_repo.list()
        by_date: dict[str, dict] = {}
        for o in orders:
            if o.purchase_timestamp is None:
                continue
            date = o.purchase_timestamp.date().isoformat() if hasattr(o.purchase_timestamp, "date") else str(o.purchase_timestamp)[:10]
            entry = by_date.setdefault(date, {"sales": 0.0, "orders": 0})
            entry["sales"] += o.total
            entry["orders"] += 1
        return [
            SalesPointOut(date=d, sales=v["sales"], orders=v["orders"])
            for d, v in sorted(by_date.items())
        ]


__all__ = ["GetKPIsUseCase", "GetSalesOverTimeUseCase"]
