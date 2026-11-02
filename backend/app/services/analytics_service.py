"""Analytics business logic service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.analytics import AnalyticsSummaryResponse, KPIResponse, SalesPointResponse
from app.repositories.customer_repository import CustomerRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.seller_repository import SellerRepository


class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session)
        self.customer_repo = CustomerRepository(session)
        self.seller_repo = SellerRepository(session)

    async def get_summary(self) -> AnalyticsSummaryResponse:
        orders = await self.order_repo.list_orders(skip=0, limit=5000)
        customers = await self.customer_repo.list_all(skip=0, limit=5000)
        sellers = await self.seller_repo.list_all(skip=0, limit=5000)

        delivered = [o for o in orders if o.status == "delivered"]
        gmv = sum(o.total for o in delivered)

        kpis = [
            KPIResponse(label="Total Orders", value=float(len(orders))),
            KPIResponse(label="GMV (Delivered)", value=float(round(gmv, 2))),
            KPIResponse(label="Customers", value=float(len(customers))),
            KPIResponse(label="Sellers", value=float(len(sellers))),
            KPIResponse(
                label="Conversion Rate",
                value=float(round(len(delivered) / max(len(orders), 1) * 100, 2)),
            ),
        ]

        by_date: dict[str, dict] = {}
        for o in orders:
            if o.purchase_timestamp is None:
                continue
            ts = o.purchase_timestamp
            if isinstance(ts, str):
                date_str = ts[:10]
            else:
                date_str = ts.date().isoformat() if hasattr(ts, "date") else str(ts)[:10]
            entry = by_date.setdefault(date_str, {"sales": 0.0, "orders": 0})
            entry["sales"] += o.total
            entry["orders"] += 1

        sales_over_time = [
            SalesPointResponse(
                date=d,
                sales=round(v["sales"], 2),
                orders=v["orders"],
            )
            for d, v in sorted(by_date.items())
        ]

        return AnalyticsSummaryResponse(kpis=kpis, sales_over_time=sales_over_time)
