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
    Category,
    Customer,
    Order,
    OrderItem,
    Payment,
    Product,
    Review,
    Seller,
    User,
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


async def seed(data_dir: Path, limit: int | None = None) -> None:  # noqa: PLR0912, PLR0915
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    print(f"Reading dataset from: {data_dir.resolve()}")
    customers = read_csv(data_dir / "olist_customers_dataset.csv")
    sellers = read_csv(data_dir / "olist_sellers_dataset.csv")
    products = read_csv(data_dir / "olist_products_dataset.csv")
    orders = read_csv(data_dir / "olist_orders_dataset.csv")
    all_order_items = read_csv(data_dir / "olist_order_items_dataset.csv")
    all_payments = read_csv(data_dir / "olist_order_payments_dataset.csv")
    all_reviews = read_csv(data_dir / "olist_order_reviews_dataset.csv")
    translations = read_csv(data_dir / "product_category_name_translation.csv")

    if limit:
        customers = customers[:limit]
        sellers = sellers[:limit]
        products = products[:limit]
        orders = orders[:limit]

    # Pre-build product price map from all order items
    prod_prices: dict[str, float] = {}
    for it in all_order_items:
        it_pid = it.get("product_id", "")
        it_price = parse_decimal(it.get("price"))
        if it_pid and it_price > 0 and it_pid not in prod_prices:
            prod_prices[it_pid] = it_price

    print(
        f"Loaded -> customers: {len(customers)}, sellers: {len(sellers)}, "
        f"products: {len(products)}, orders: {len(orders)}, "
        f"order_items_dataset: {len(all_order_items)}, price_map: {len(prod_prices)}"
    )

    cat_name_to_english = {
        r.get("product_category_name", ""): r.get("product_category_name_english", "")
        for r in translations
    }

    async with async_session() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        # 1. Users
        default_hashed_pw = hash_password("Password123!")

        # Add explicit standard seed accounts for testing
        admin_uid = uuid.uuid4()
        session.add(
            User(
                id=admin_uid,
                email="admin@shopflow.com",
                username="admin",
                hashed_password=default_hashed_pw,
                full_name="Marketplace Admin",
                is_active=True,
                is_superuser=True,
                role="admin",
            )
        )
        test_cust_uid = uuid.uuid4()
        session.add(
            User(
                id=test_cust_uid,
                email="customer@shopflow.com",
                username="democustomer",
                hashed_password=default_hashed_pw,
                full_name="Demo Customer",
                is_active=True,
                is_superuser=False,
                role="customer",
            )
        )
        test_sell_uid = uuid.uuid4()
        session.add(
            User(
                id=test_sell_uid,
                email="seller@shopflow.com",
                username="demoseller",
                hashed_password=default_hashed_pw,
                full_name="Demo Merchant",
                is_active=True,
                is_superuser=False,
                role="seller",
            )
        )

        cust_user_id: dict[str, uuid.UUID] = {}
        cust_row_id: dict[str, uuid.UUID] = {}
        cust_id_to_uniq: dict[str, str] = {}
        unique_customers: dict[str, dict[str, Any]] = {}

        for c in customers:
            c_id = c.get("customer_id", "")
            c_uniq = c.get("customer_unique_id", "")
            if not c_id or not c_uniq:
                continue
            cust_id_to_uniq[c_id] = c_uniq
            if c_uniq not in unique_customers:
                unique_customers[c_uniq] = c
                uid = uuid.uuid4()
                cust_user_id[c_uniq] = uid
                session.add(
                    User(
                        id=uid,
                        email=f"{c_uniq}@shopflow.example",
                        username=c_uniq,
                        hashed_password=default_hashed_pw,
                        full_name=None,
                        is_active=True,
                        is_superuser=False,
                        role="customer",
                    )
                )

        sell_user_id: dict[str, uuid.UUID] = {}
        sell_row_id: dict[str, uuid.UUID] = {}
        unique_sellers: dict[str, dict[str, Any]] = {}

        for s in sellers:
            s_id = s.get("seller_id", "")
            if not s_id or s_id in unique_sellers:
                continue
            unique_sellers[s_id] = s
            uid = uuid.uuid4()
            sell_user_id[s_id] = uid
            session.add(
                User(
                    id=uid,
                    email=f"seller-{s_id}@shopflow.example",
                    username=f"seller_{s_id[:8]}",
                    hashed_password=default_hashed_pw,
                    full_name=None,
                    is_active=True,
                    is_superuser=False,
                    role="seller",
                )
            )

        # Flush users first to satisfy foreign keys
        await session.flush()

        # 2. Customers & Sellers
        session.add(
            Customer(
                id=uuid.uuid4(),
                customer_unique_id="democustomer",
                customer_zip_code_prefix="01310",
                customer_city="São Paulo",
                customer_state="SP",
                user_id=test_cust_uid,
            )
        )
        session.add(
            Seller(
                id=uuid.uuid4(),
                seller_zip_code_prefix="01310",
                seller_city="São Paulo",
                seller_state="SP",
                user_id=test_sell_uid,
            )
        )

        for c_uniq, c in unique_customers.items():
            cid = uuid.uuid4()
            cust_row_id[c_uniq] = cid
            session.add(
                Customer(
                    id=cid,
                    customer_unique_id=c_uniq,
                    customer_zip_code_prefix=c.get("customer_zip_code_prefix", "") or "",
                    customer_city=c.get("customer_city", "") or "",
                    customer_state=c.get("customer_state", "") or "",
                    user_id=cust_user_id[c_uniq],
                )
            )

        for s_id, s in unique_sellers.items():
            sid = uuid.uuid4()
            sell_row_id[s_id] = sid
            session.add(
                Seller(
                    id=sid,
                    seller_zip_code_prefix=s.get("seller_zip_code_prefix", "") or "",
                    seller_city=s.get("seller_city", "") or "",
                    seller_state=s.get("seller_state", "") or "",
                    user_id=sell_user_id[s_id],
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
            p_id = p.get("product_id", "")
            if not p_id or p_id in prod_id:
                continue
            pid = uuid.uuid4()
            prod_id[p_id] = pid
            seller_uuid = (
                sell_row_id.get(seller_keys[i % len(seller_keys)]) if seller_keys else None
            )
            raw_cname = p.get("product_category_name", "") or ""
            eng_cname = cat_name_to_english.get(raw_cname) or raw_cname or "General"
            cat_label = eng_cname.replace("_", " ").title()

            price_val = prod_prices.get(p_id, round(29.99 + ((i % 15) * 5.50), 2))
            session.add(
                Product(
                    id=pid,
                    sku=p_id,
                    name=cat_label,
                    description=f"Authentic {cat_label} item from verified marketplace merchants.",
                    price=price_val,
                    stock_quantity=max(parse_int(p.get("product_photos_qty")) * 5, 10),
                    category_id=cat_id.get(raw_cname),
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
            o_id = o.get("order_id", "")
            if not o_id or o_id in order_id:
                continue
            oid = uuid.uuid4()
            c_uniq = cust_id_to_uniq.get(o.get("customer_id", ""))
            cust_uuid = cust_row_id.get(c_uniq) if c_uniq else None
            if cust_uuid is None:
                continue
            order_id[o_id] = oid
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
        order_totals: dict[str, float] = dict.fromkeys(order_id, 0.0)
        item_count = 0
        for it in all_order_items:
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
        for py in all_payments:
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
        for rv in all_reviews:
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
