"""Feature engineering for ShopFlow ML pipelines.

Reads the Olist historical dataset from ml/datasets/olist/ and produces
model-ready feature frames. Independent of HTTP/React (Clean Architecture ML
isolation).
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

OLIST_DIR = Path(__file__).resolve().parents[2] / "datasets" / "olist"


def _load(name: str) -> pd.DataFrame:
    return pd.read_csv(OLIST_DIR / name)


def load_orders() -> pd.DataFrame:
    df = _load("olist_orders_dataset.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce")
    df["order_approved_at"] = pd.to_datetime(df["order_approved_at"], errors="coerce")
    df["order_delivered_customer_date"] = pd.to_datetime(
        df["order_delivered_customer_date"], errors="coerce"
    )
    df["order_estimated_delivery_date"] = pd.to_datetime(
        df["order_estimated_delivery_date"], errors="coerce"
    )
    return df


def load_order_items() -> pd.DataFrame:
    return _load("olist_order_items_dataset.csv")


def load_order_payments() -> pd.DataFrame:
    return _load("olist_order_payments_dataset.csv")


def load_order_reviews() -> pd.DataFrame:
    return _load("olist_order_reviews_dataset.csv")


def load_products() -> pd.DataFrame:
    return _load("olist_products_dataset.csv")


def load_customers() -> pd.DataFrame:
    return _load("olist_customers_dataset.csv")


def load_sellers() -> pd.DataFrame:
    return _load("olist_sellers_dataset.csv")


def load_category_translation() -> pd.DataFrame:
    return _load("product_category_name_translation.csv")


def build_order_features() -> pd.DataFrame:
    """Join orders with items, payments, reviews -> one row per order."""
    orders = load_orders()
    items = load_order_items()
    payments = load_order_payments()
    reviews = load_order_reviews()

    items_agg = (
        items.groupby("order_id")
        .agg(
            item_count=("order_item_id", "count"),
            product_count=("product_id", "nunique"),
            seller_count=("seller_id", "nunique"),
            item_price_sum=("price", "sum"),
            freight_sum=("freight_value", "sum"),
        )
        .reset_index()
    )

    payments_agg = (
        payments.groupby("order_id")
        .agg(payment_value_sum=("payment_value", "sum"), payment_types=("payment_type", "nunique"))
        .reset_index()
    )

    reviews_agg = (
        reviews.groupby("order_id")
        .agg(review_score=("review_score", "mean"), review_count=("review_id", "count"))
        .reset_index()
    )

    df = orders.merge(items_agg, on="order_id", how="left")
    df = df.merge(payments_agg, on="order_id", how="left")
    df = df.merge(reviews_agg, on="order_id", how="left")

    # Delivery delay (days) -> target for delivery ETA / late classification
    df["delivery_delay_days"] = (
        df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400
    df["is_late"] = (df["delivery_delay_days"] > 0).astype(int)

    # Actual delivery time (days) -> target for ETA regression
    df["delivery_days"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    df = df.sort_values("order_purchase_timestamp").reset_index(drop=True)
    return df


def build_customer_features() -> pd.DataFrame:
    """RFM + monetary features per customer."""
    orders = load_orders()
    order_items = load_order_items()
    payments = load_order_payments()

    items_with_order = order_items.merge(orders[["order_id", "customer_id", "order_purchase_timestamp"]], on="order_id")
    pay = payments.groupby("order_id")["payment_value"].sum().reset_index(name="order_value")
    items_with_order = items_with_order.merge(pay, on="order_id", how="left")

    items_with_order["order_purchase_timestamp"] = pd.to_datetime(items_with_order["order_purchase_timestamp"])
    now = items_with_order["order_purchase_timestamp"].max()

    rfm = (
        items_with_order.groupby("customer_id")
        .agg(
            recency=("order_purchase_timestamp", lambda x: (now - x.max()).days),
            frequency=("order_id", "nunique"),
            monetary=("order_value", "sum"),
        )
        .reset_index()
    )

    customers = load_customers()
    rfm = rfm.merge(customers[["customer_id", "customer_city", "customer_state"]], on="customer_id", how="left")
    return rfm


def build_product_features() -> pd.DataFrame:
    """Aggregated product features: sales volume, avg price, review score."""
    orders = load_orders()
    items = load_order_items()
    payments = load_order_payments()
    reviews = load_order_reviews()
    products = load_products()

    items_pay = items.merge(payments[["order_id", "payment_value"]], on="order_id", how="left")
    items_orders = items_pay.merge(orders[["order_id", "customer_id", "order_purchase_timestamp"]], on="order_id", how="left")

    prod_agg = (
        items_orders.groupby("product_id")
        .agg(
            units_sold=("order_item_id", "count"),
            revenue=("price", "sum"),
            avg_price=("price", "mean"),
            seller_count=("seller_id", "nunique"),
            buyer_count=("customer_id", "nunique"),
        )
        .reset_index()
    )

    rev_agg = reviews.merge(orders[["order_id", "customer_id"]], on="order_id").groupby("order_id")["review_score"].mean()
    # map review to product via order_items
    rev_items = reviews.merge(items[["order_id", "product_id"]], on="order_id")
    prod_rev = rev_items.groupby("product_id")["review_score"].agg(["mean", "count"]).reset_index()
    prod_rev.columns = ["product_id", "avg_review_score", "review_count"]

    df = products.merge(prod_agg, on="product_id", how="left")
    df = df.merge(prod_rev, on="product_id", how="left")

    # Merge category english name
    trans = load_category_translation()
    df = df.merge(trans, on="product_category_name", how="left")
    return df


__all__ = [
    "load_orders",
    "load_order_items",
    "load_order_payments",
    "load_order_reviews",
    "load_products",
    "load_customers",
    "load_sellers",
    "load_category_translation",
    "build_order_features",
    "build_customer_features",
    "build_product_features",
    "OLIST_DIR",
]
