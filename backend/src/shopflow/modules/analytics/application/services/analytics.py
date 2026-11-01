"""Analytics application service (read-only aggregations)."""

from typing import List, Optional
from datetime import datetime

from shopflow.modules.orders.domain.repositories.order import OrderRepository
from shopflow.modules.payments.domain.repositories.payment import PaymentRepository
from shopflow.modules.customers.domain.repositories.customer import CustomerRepository
from shopflow.modules.sellers.domain.repositories.seller import SellerRepository
from shopflow.modules.catalog.domain.repositories.catalog import ProductRepository


class KPI:
    def __init__(self, label: str, value: float, delta: Optional[float] = None, delta_percent: Optional[float] = None):
        self.label = label
        self.value = value
        self.delta = delta
        self.delta_percent = delta_percent


class SalesPoint:
    def __init__(self, date: str, sales: float, orders: int):
        self.date = date
        self.sales = sales
        self.orders = orders


class AnalyticsService:
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

    async def get_kpis(self) -> List[KPI]:
        orders = await self.order_repo.list()
        customers = await self.customer_repo.list()
        sellers = await self.seller_repo.list()
        products = await self.product_repo.list()

        total_sales = sum(o.total for o in orders)
        delivered = [o for o in orders if o.status == "delivered"]
        gmv = sum(o.total for o in delivered)

        return [
            KPI("Total Orders", float(len(orders))),
            KPI("GMV (Delivered)", float(gmv)),
            KPI("Customers", float(len(customers))),
            KPI("Sellers", float(len(sellers))),
            KPI("Products", float(len(products))),
            KPI("Conversion Rate", float(len(delivered) / max(len(orders), 1) * 100)),
        ]

    async def get_sales_over_time(self) -> List[SalesPoint]:
        orders = await self.order_repo.list()
        by_date: dict[str, dict] = {}
        for o in orders:
            if o.purchase_timestamp is None:
                continue
            ts = o.purchase_timestamp
            if isinstance(ts, str):
                date = ts[:10]
            else:
                date = ts.date().isoformat() if hasattr(ts, "date") else str(ts)[:10]
            entry = by_date.setdefault(date, {"sales": 0.0, "orders": 0})
            entry["sales"] += o.total
            entry["orders"] += 1
        return [
            SalesPoint(date=d, sales=v["sales"], orders=v["orders"])
            for d, v in sorted(by_date.items())
        ]


__all__ = ["AnalyticsService", "KPI", "SalesPoint"]
