"""Customer repository for persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, customer_id: uuid.UUID) -> Customer | None:
        return await self.session.get(Customer, customer_id)

    async def get_by_unique_id(self, customer_unique_id: str) -> Customer | None:
        result = await self.session.execute(
            select(Customer).where(Customer.customer_unique_id == customer_unique_id)
        )
        return result.scalar_one_or_none()

    async def create(self, customer: Customer) -> Customer:
        self.session.add(customer)
        await self.session.flush()
        return customer

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[Customer]:
        result = await self.session.execute(select(Customer).offset(skip).limit(limit))
        return list(result.scalars().all())
