"""Clean and prepare raw Olist dataset for downstream ML training.

Reads raw CSVs from ml/data/raw/olist/, validates schemas, parses timestamps,
cleans nulls/outliers, and exports cleaned parquet/csv datasets to ml/data/cleared/.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).resolve().parent / "raw" / "olist"
CLEARED_DIR = Path(__file__).resolve().parent / "cleared"


def clean_datasets() -> None:
    CLEARED_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Reading raw data from: {RAW_DIR}")

    # 1. Orders
    orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
    ts_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in ts_cols:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")
    orders = orders.dropna(subset=["order_id", "customer_id", "order_purchase_timestamp"])
    orders.to_parquet(CLEARED_DIR / "clean_orders.parquet", index=False)
    orders.to_csv(CLEARED_DIR / "clean_orders.csv", index=False)
    print(f"Saved clean_orders: {len(orders)} rows")

    # 2. Order Items
    items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")
    items["shipping_limit_date"] = pd.to_datetime(items["shipping_limit_date"], errors="coerce")
    items["price"] = pd.to_numeric(items["price"], errors="coerce").fillna(0.0)
    items["freight_value"] = pd.to_numeric(items["freight_value"], errors="coerce").fillna(0.0)
    items = items.dropna(subset=["order_id", "product_id", "seller_id"])
    items.to_parquet(CLEARED_DIR / "clean_order_items.parquet", index=False)
    items.to_csv(CLEARED_DIR / "clean_order_items.csv", index=False)
    print(f"Saved clean_order_items: {len(items)} rows")

    # 3. Products & Category Translation
    products = pd.read_csv(RAW_DIR / "olist_products_dataset.csv")
    trans = pd.read_csv(RAW_DIR / "product_category_name_translation.csv")
    products = products.merge(trans, on="product_category_name", how="left")
    products["product_category_name_english"] = products["product_category_name_english"].fillna("other")
    num_cols = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]
    for col in num_cols:
        products[col] = pd.to_numeric(products[col], errors="coerce").fillna(0)
    products.to_parquet(CLEARED_DIR / "clean_products.parquet", index=False)
    products.to_csv(CLEARED_DIR / "clean_products.csv", index=False)
    print(f"Saved clean_products: {len(products)} rows")

    # 4. Customers
    customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")
    customers = customers.dropna(subset=["customer_id", "customer_unique_id"])
    customers["customer_zip_code_prefix"] = customers["customer_zip_code_prefix"].astype(str)
    customers.to_parquet(CLEARED_DIR / "clean_customers.parquet", index=False)
    customers.to_csv(CLEARED_DIR / "clean_customers.csv", index=False)
    print(f"Saved clean_customers: {len(customers)} rows")

    # 5. Sellers
    sellers = pd.read_csv(RAW_DIR / "olist_sellers_dataset.csv")
    sellers = sellers.dropna(subset=["seller_id"])
    sellers["seller_zip_code_prefix"] = sellers["seller_zip_code_prefix"].astype(str)
    sellers.to_parquet(CLEARED_DIR / "clean_sellers.parquet", index=False)
    sellers.to_csv(CLEARED_DIR / "clean_sellers.csv", index=False)
    print(f"Saved clean_sellers: {len(sellers)} rows")

    # 6. Payments
    payments = pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv")
    payments["payment_value"] = pd.to_numeric(payments["payment_value"], errors="coerce").fillna(0.0)
    payments["payment_installments"] = pd.to_numeric(payments["payment_installments"], errors="coerce").fillna(1).astype(int)
    payments.to_parquet(CLEARED_DIR / "clean_payments.parquet", index=False)
    payments.to_csv(CLEARED_DIR / "clean_payments.csv", index=False)
    print(f"Saved clean_payments: {len(payments)} rows")

    # 7. Reviews
    reviews = pd.read_csv(RAW_DIR / "olist_order_reviews_dataset.csv")
    reviews["review_score"] = pd.to_numeric(reviews["review_score"], errors="coerce").fillna(5).astype(int)
    reviews["review_creation_date"] = pd.to_datetime(reviews["review_creation_date"], errors="coerce")
    reviews["review_answer_timestamp"] = pd.to_datetime(reviews["review_answer_timestamp"], errors="coerce")
    reviews.to_parquet(CLEARED_DIR / "clean_reviews.parquet", index=False)
    reviews.to_csv(CLEARED_DIR / "clean_reviews.csv", index=False)
    print(f"Saved clean_reviews: {len(reviews)} rows")

    print(f"Cleansing completed successfully. All clean datasets saved in: {CLEARED_DIR}")


if __name__ == "__main__":
    clean_datasets()
