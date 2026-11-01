"""Shared application layer."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Command(ABC):
    """Marker base for application commands."""


@dataclass
class Query(ABC):
    """Marker base for application queries."""


__all__ = ["Command", "Query"]
