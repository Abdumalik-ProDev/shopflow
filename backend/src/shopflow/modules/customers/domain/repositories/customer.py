"""Customers domain repository interface."""

from __future__ import annotations

from typing import Optional, List

from shopflow.modules.customers.domain.models.customer import Customer


class CustomerRepository:
    async def add(self, customer: Customer) -> None:
        raise NotImplementedError

    async def get_by_id(self, customer_id: str) -> Optional[Customer]:
        raise NotImplementedError

    async def get_by_unique_id(self, customer_unique_id: str) -> Optional[Customer]:
        raise NotImplementedError

    async def list(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        raise NotImplementedError

    async def update(self, customer: Customer) -> None:
        raise NotImplementedError

    async def delete(self, customer_id: str) -> None:
        raise NotImplementedError


__all__ = ["CustomerRepository"]
