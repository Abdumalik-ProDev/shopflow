"""Recommendations domain models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ProductRecommendation:
    product_id: str
    score: float
    reason: str


__all__ = ["ProductRecommendation"]
