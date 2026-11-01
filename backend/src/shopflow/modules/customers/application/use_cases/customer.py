"""Customers application use cases."""

from __future__ import annotations

from shopflow.core.exceptions import NotFoundError
from shopflow.modules.customers.application.dtos.customer import (
    CustomerCreate,
    CustomerOut,
    CustomerUpdate,
)
from shopflow.modules.customers.domain.models.customer import Customer
from shopflow.modules.customers.domain.repositories.customer import CustomerRepository


class CreateCustomerUseCase:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    async def execute(self, dto: CustomerCreate) -> CustomerOut:
        customer = Customer(
            customer_unique_id=dto.customer_unique_id,
            customer_zip_code_prefix=dto.customer_zip_code_prefix,
            customer_city=dto.customer_city,
            customer_state=dto.customer_state,
        )
        await self.customer_repo.add(customer)
        return CustomerOut.model_validate(customer)


class GetCustomerUseCase:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    async def execute(self, customer_id: str) -> CustomerOut | None:
        customer = await self.customer_repo.get_by_id(customer_id)
        if customer is None:
            return None
        return CustomerOut.model_validate(customer)


class UpdateCustomerUseCase:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    async def execute(self, customer_id: str, dto: CustomerUpdate) -> CustomerOut | None:
        customer = await self.customer_repo.get_by_id(customer_id)
        if customer is None:
            raise NotFoundError("Customer not found", code="CUSTOMER_NOT_FOUND")
        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(customer, field, value)
        await self.customer_repo.update(customer)
        return CustomerOut.model_validate(customer)


class ListCustomersUseCase:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    async def execute(self, skip: int = 0, limit: int = 100) -> list[CustomerOut]:
        customers = await self.customer_repo.list(skip=skip, limit=limit)
        return [CustomerOut.model_validate(c) for c in customers]


__all__ = [
    "CreateCustomerUseCase",
    "GetCustomerUseCase",
    "UpdateCustomerUseCase",
    "ListCustomersUseCase",
]
