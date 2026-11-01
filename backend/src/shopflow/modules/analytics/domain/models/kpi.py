"""Analytics domain models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class KPI:
    label: str
    value: float
    delta: float | None = None
    delta_percent: float | None = None


@dataclass
class SalesPoint:
    date: str
    sales: float
    orders: int


@dataclass
class TopProduct:
    product_id: str
    name: str
    sales: float
    units: int


__all__ = ["KPI", "SalesPoint", "TopProduct"]
