"""Shared application result types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Success(Generic[T]):
    value: T


@dataclass
class Failure:
    code: str
    message: str


@dataclass
class Paginated(Generic[T]):
    items: list[T]
    total: int
    skip: int
    limit: int

__all__ = ["Success", "Failure", "Paginated", "T"]
