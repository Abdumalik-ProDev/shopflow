"""Customers infrastructure repository implementation."""

from __future__ import annotations

from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.modules.customers.domain.models.customer import Customer
from shopflow.modules.customers.domain.repositories.customer import CustomerRepository
from shopflow.modules.customers.infrastructure.persistence.models import CustomerRow


class SqlAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, customer: Customer) -> None:
        row = CustomerRow(
            id=customer.id,
            customer_unique_id=customer.customer_unique_id,
            customer_zip_code_prefix=customer.customer_zip_code_prefix,
            customer_city=customer.customer_city,
            customer_state=customer.customer_state,
        )
        self.session.add(row)
        await self.session.flush()

    async def get_by_id(self, customer_id: str) -> Optional[Customer]:
        from uuid import UUID

        row = await self.session.get(CustomerRow, UUID(customer_id))
        return self._to_domain(row) if row else None

    async def get_by_unique_id(self, customer_unique_id: str) -> Optional[Customer]:
        result = await self.session.execute(
            select(CustomerRow).where(CustomerRow.customer_unique_id == customer_unique_id)
        )
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def list(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        result = await self.session.execute(select(CustomerRow).offset(skip).limit(limit))
        return [self._to_domain(r) for r in result.scalars().all()]

    async def update(self, customer: Customer) -> None:
        row = await self.session.get(CustomerRow, customer.id)
        if not row:
            return
        row.customer_unique_id = customer.customer_unique_id
        row.customer_zip_code_prefix = customer.customer_zip_code_prefix
        row.customer_city = customer.customer_city
        row.customer_state = customer.customer_state
        await self.session.flush()

    async def delete(self, customer_id: str) -> None:
        from uuid import UUID

        row = await self.session.get(CustomerRow, UUID(customer_id))
        if row:
            await self.session.delete(row)

    @staticmethod
    def _to_domain(row: CustomerRow) -> Customer:
        return Customer(
            id=str(row.id),
            customer_unique_id=row.customer_unique_id,
            customer_zip_code_prefix=row.customer_zip_code_prefix,
            customer_city=row.customer_city,
            customer_state=row.customer_state,
        )


__all__ = ["SqlAlchemyCustomerRepository"]
