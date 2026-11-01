"""Shared Unit of Work for transaction management."""

from __future__ import annotations

from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

__all__ = ["UnitOfWork"]
