"""General utility helpers for parsing, formatting, and pagination."""

from datetime import datetime
from decimal import Decimal
from typing import Any


def parse_datetime(value: Any) -> datetime | None:
    if not value or str(value).strip() == "":
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value))
    except (ValueError, TypeError):
        return None


def parse_float(value: Any, default: float = 0.0) -> float:
    if value is None or str(value).strip() == "":
        return default
    try:
        return float(Decimal(str(value)))
    except Exception:
        return default


def parse_int(value: Any, default: int = 0) -> int:
    if value is None or str(value).strip() == "":
        return default
    try:
        return int(float(str(value)))
    except Exception:
        return default
