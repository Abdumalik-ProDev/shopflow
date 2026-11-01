"""Customers application service."""

from shopflow.core.exceptions import NotFoundError
from shopflow.modules.customers.application.dtos.customer import CustomerCreate, CustomerOut, CustomerUpdate
from shopflow.modules.customers.application.mappers.customer import (
    domain_to_dto, dto_to_domain, update_domain_from_dto,
)
from shopflow.modules.customers.domain.models.customer import Customer
from shopflow.modules.customers.domain.repositories.customer import CustomerRepository


class CustomerService:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    async def create(self, dto: CustomerCreate) -> CustomerOut:
        customer = dto_to_domain(dto)
        await self.customer_repo.add(customer)
        return domain_to_dto(customer)

    async def get_by_id(self, customer_id: str) -> CustomerOut | None:
        c = await self.customer_repo.get_by_id(customer_id)
        return domain_to_dto(c) if c else None

    async def update(self, customer_id: str, dto: CustomerUpdate) -> CustomerOut | None:
        c = await self.customer_repo.get_by_id(customer_id)
        if c is None:
            raise NotFoundError("Customer not found", code="CUSTOMER_NOT_FOUND")
        update_domain_from_dto(c, dto)
        await self.customer_repo.update(c)
        return domain_to_dto(c)

    async def list(self, skip: int = 0, limit: int = 100) -> list[CustomerOut]:
        return [domain_to_dto(c) for c in await self.customer_repo.list(skip=skip, limit=limit)]


__all__ = ["CustomerService"]
