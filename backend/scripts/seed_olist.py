"""Seed script: loads the Brazilian Olist e-commerce dataset into PostgreSQL.

Populates the live marketplace database with a curated subset of the Olist
historical data. Per VISION.md §5, raw Olist data remains in ml/data/raw/olist/,
separate from live marketplace data.

Usage:
    cd backend
    uv run python scripts/seed_olist.py --data-dir ../ml/data/raw/olist --limit 2000
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import uuid
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.database import Base
from app.models import (
    User,
    Category,
    Product,
    Customer,
    Seller,
    Order,
    OrderItem,
    Payment,
    Review,
)
from app.security import hash_password


def parse_ts(value: str | None) -> datetime | None:
    if not value or str(value).strip() == "":
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None


def parse_decimal(value: str | None) -> float:
    if value is None or str(value).strip() == "":
        return 0.0
    try:
        return float(Decimal(str(value)))
    except Exception:
        return 0.0


def parse_int(value: str | None) -> int:
    if value is None or str(value).strip() == "":
        return 0
    try:
        return int(float(str(value)))
    except Exception:
        return 0


def read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        print(f"Warning: File {path} not found.")
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


async def seed(data_dir: Path, limit: int | None = None) -> None:
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    print(f"Reading dataset from: {data_dir.resolve()}")
    customers = read_csv(data_dir / "olist_customers_dataset.csv")
    sellers = read_csv(data_dir / "olist_sellers_dataset.csv")
    products = read_csv(data_dir / "olist_products_dataset.csv")
    orders = read_csv(data_dir / "olist_orders_dataset.csv")
    order_items = read_csv(data_dir / "olist_order_items_dataset.csv")
    payments = read_csv(data_dir / "olist_order_payments_dataset.csv")
    reviews = read_csv(data_dir / "olist_order_reviews_dataset.csv")
    translations = read_csv(data_dir / "product_category_name_translation.csv")

    if limit:
        customers = customers[:limit]
        sellers = sellers[:limit]
        products = products[:limit]
        orders = orders[:limit]
        order_items = order_items[:limit]
        payments = payments[:limit]
        reviews = reviews[:limit]

    print(
        f"Loaded -> customers: {len(customers)}, sellers: {len(sellers)}, "
        f"products: {len(products)}, orders: {len(orders)}, items: {len(order_items)}, "
        f"payments: {len(payments)}, reviews: {len(reviews)}"
    )

    cat_name_to_english = {
        r.get("product_category_name", ""): r.get("product_category_name_english", "")
        for r in translations
    }

    async with async_session() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Users
        cust_user_id: dict[str, uuid.UUID] = {}
        sell_user_id: dict[str, uuid.UUID] = {}
        for c in customers:
            uid = uuid.uuid4()
            cust_user_id[c["customer_unique_id"]] = uid
            session.add(
                User(
                    id=uid,
                    email=f"{c['customer_unique_id']}@shopflow.example",
                    username=c["customer_unique_id"],
                    hashed_password=hash_password("Password123!"),
                    full_name=None,
                    is_active=True,
                    is_superuser=False,
                    role="customer",
                )
            )
        for s in sellers:
            uid = uuid.uuid4()
            sell_user_id[s["seller_id"]] = uid
            session.add(
                User(
                    id=uid,
                    email=f"seller-{s['seller_id']}@shopflow.example",
                    username=f"seller_{s['seller_id'][:8]}",
                    hashed_password=hash_password("Password123!"),
                    full_name=None,
                    is_active=True,
                    is_superuser=False,
                    role="seller",
                )
            )
        await session.flush()

        # Customers
        cust_row_id: dict[str, uuid.UUID] = {}
        for c in customers:
            cid = uuid.uuid4()
            cust_row_id[c["customer_unique_id"]] = cid
            session.add(
                Customer(
                    id=cid,
                    customer_unique_id=c["customer_unique_id"],
                    customer_zip_code_prefix=c.get("customer_zip_code_prefix", "") or "",
                    customer_city=c.get("customer_city", "") or "",
                    customer_state=c.get("customer_state", "") or "",
                    user_id=cust_user_id[c["customer_unique_id"]],
                )
            )
        await session.flush()

        # Sellers
        sell_row_id: dict[str, uuid.UUID] = {}
        for s in sellers:
            sid = uuid.uuid4()
            sell_row_id[s["seller_id"]] = sid
            session.add(
                Seller(
                    id=sid,
                    seller_zip_code_prefix=s.get("seller_zip_code_prefix", "") or "",
                    seller_city=s.get("seller_city", "") or "",
                    seller_state=s.get("seller_state", "") or "",
                    user_id=sell_user_id[s["seller_id"]],
                )
            )
        await session.flush()

        # Categories
        cat_id: dict[str, uuid.UUID] = {}
        seen: set[str] = set()
        for p in products:
            cname = p.get("product_category_name", "") or ""
            if cname and cname not in seen:
                seen.add(cname)
                cid = uuid.uuid4()
                cat_id[cname] = cid
                session.add(
                    Category(
                        id=cid,
                        name=cname,
                        name_english=cat_name_to_english.get(cname),
                    )
                )
        await session.flush()

        # Products
        prod_id: dict[str, uuid.UUID] = {}
        seller_keys = list(sell_row_id.keys())
        for i, p in enumerate(products):
            pid = uuid.uuid4()
            prod_id[p["product_id"]] = pid
            seller_uuid = (
                sell_row_id.get(seller_keys[i % len(seller_keys)]) if seller_keys else None
            )
            session.add(
                Product(
                    id=pid,
                    sku=p["product_id"],
                    name=(p.get("product_category_name", "") or "Product").replace("_", " ").title(),
                    description=None,
                    price=0.0,
                    stock_quantity=max(parse_int(p.get("product_photos_qty")) * 5, 10),
                    category_id=cat_id.get(p.get("product_category_name", "") or ""),
                    seller_id=seller_uuid,
                    is_active=True,
                    weight_g=parse_decimal(p.get("product_weight_g")) or None,
                    length_cm=parse_decimal(p.get("product_length_cm")) or None,
                    height_cm=parse_decimal(p.get("product_height_cm")) or None,
                    width_cm=parse_decimal(p.get("product_width_cm")) or None,
                    photos_qty=parse_int(p.get("product_photos_qty")) or None,
                )
            )
        await session.flush()

        # Orders
        order_id: dict[str, uuid.UUID] = {}
        for o in orders:
            oid = uuid.uuid4()
            order_id[o["order_id"]] = oid
            cust_uuid = cust_row_id.get(o["customer_id"])
            if cust_uuid is None:
                continue
            session.add(
                Order(
                    id=oid,
                    customer_id=cust_uuid,
                    status=o.get("order_status", "delivered") or "delivered",
                    purchase_timestamp=parse_ts(o.get("order_purchase_timestamp")),
                    approved_at=parse_ts(o.get("order_approved_at")),
                    delivered_carrier_date=parse_ts(o.get("order_delivered_carrier_date")),
                    delivered_customer_date=parse_ts(o.get("order_delivered_customer_date")),
                    estimated_delivery_date=parse_ts(o.get("order_estimated_delivery_date")),
                    total=0.0,
                )
            )
        await session.flush()

        # Order items
        order_totals: dict[str, float] = {k: 0.0 for k in order_id}
        item_count = 0
        for it in order_items:
            oid = order_id.get(it["order_id"])
            if oid is None:
                continue
            price = parse_decimal(it.get("price"))
            freight = parse_decimal(it.get("freight_value"))
            qty = parse_int(it.get("quantity")) or 1
            item_count += 1
            session.add(
                OrderItem(
                    id=uuid.uuid4(),
                    order_id=oid,
                    product_id=it["product_id"],
                    seller_id=it.get("seller_id", "") or "",
                    price=price,
                    freight_value=freight,
                    quantity=qty,
                )
            )
            order_totals[str(oid)] = order_totals.get(str(oid), 0.0) + (price * qty)

        for oid_str, total in order_totals.items():
            oid = uuid.UUID(oid_str)
            row = await session.get(Order, oid)
            if row:
                row.total = round(total, 2)

        await session.flush()

        # Payments
        for py in payments:
            oid = order_id.get(py["order_id"])
            if oid is None:
                continue
            session.add(
                Payment(
                    id=uuid.uuid4(),
                    order_id=oid,
                    payment_sequential=parse_int(py.get("payment_sequential")) or 1,
                    payment_type=py.get("payment_type", "credit_card") or "credit_card",
                    payment_installments=parse_int(py.get("payment_installments")) or 1,
                    payment_value=parse_decimal(py.get("payment_value")),
                )
            )
        await session.flush()

        # Reviews
        for rv in reviews:
            oid = order_id.get(rv["order_id"])
            if oid is None:
                continue
            session.add(
                Review(
                    id=uuid.uuid4(),
                    order_id=oid,
                    review_score=parse_int(rv.get("review_score")) or 5,
                    comment_title=rv.get("comment_title") or None,
                    comment_message=rv.get("comment_message") or None,
                )
            )
        await session.flush()

        await session.commit()

    print(f"Seed complete. Orders: {len(order_id)}, OrderItems: {item_count}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed ShopFlow with Olist dataset")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("../ml/data/raw/olist"),
        help="Path to dataset folder containing Olist CSVs",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max rows per table (useful for tests / smoke runs)",
    )
    args = parser.parse_args()

    asyncio.run(seed(args.data_dir, args.limit))


if __name__ == "__main__":
    main()
