"""Feature engineering: customer features."""

from __future__ import annotations

import pandas as pd


def compute_rfm(orders: pd.DataFrame) -> pd.DataFrame:
    """Compute Recency, Frequency, Monetary features per customer."""
    now = orders["order_purchase_timestamp"].max()
    rfm = (
        orders.groupby("customer_id")
        .agg(
            recency=("order_purchase_timestamp", lambda x: (now - x.max()).days),
            frequency=("order_id", "nunique"),
            monetary=("payment_value", "sum"),
        )
        .reset_index()
    )
    return rfm


__all__ = ["compute_rfm"]
