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


__all__ = ["Success", "Failure", "T"]
