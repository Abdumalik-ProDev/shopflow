"""ML inference entry points (used by backend recommendations module)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import mlflow.pyfunc


def predict_delivery_eta(features: Dict[str, Any]) -> float:
    """Predict delivery ETA in days for an order.

    Falls back to a statistical baseline (5 days) when no model artifact is
    registered in MLflow. Independent of HTTP/React.
    """
    try:
        model = mlflow.pyfunc.load_model("models:/delivery_eta_model/Production")
        return float(model.predict([features])[0])
    except Exception:
        # Deterministic baseline
        base = 5.0
        item_count = float(features.get("item_count", 1))
        freight = float(features.get("freight_sum", 0))
        return round(base + item_count * 0.5 + min(freight, 50) * 0.02, 1)


def recommend_products(customer_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Return product recommendations for a customer.

    Uses popularity-based ranking from Olist historical data. Replace with
    trained collaborative-filtering / LightFM model artifact when available.
    """
    from ml.features import load_order_items, load_products, load_orders

    items = load_order_items()
    orders = load_orders()[["order_id", "order_purchase_timestamp"]]
    orders["order_purchase_timestamp"] = pd_to_datetime_safe(orders["order_purchase_timestamp"])
    merged = items.merge(orders, on="order_id", how="left")

    # Recent window (last 90 days) for recency-weighted popularity
    cutoff = merged["order_purchase_timestamp"].max() - pd.Timedelta(days=90)
    recent = merged[merged["order_purchase_timestamp"] >= cutoff]

    pop = (
        recent.groupby("product_id")
        .agg(score=("price", "sum"), units=("order_item_id", "count"))
        .reset_index()
        .sort_values("score", ascending=False)
        .head(limit)
    )

    products = load_products()[["product_id", "product_category_name"]]
    pop = pop.merge(products, on="product_id", how="left")

    return [
        {
            "product_id": str(r.product_id),
            "score": round(float(r.score), 2),
            "reason": f"Popular in {r.product_category_name or 'your region'}",
        }
        for r in pop.itertuples()
    ]


def pd_to_datetime_safe(s):
    import pandas as pd
    return pd.to_datetime(s, errors="coerce")


__all__ = ["predict_delivery_eta", "recommend_products"]
