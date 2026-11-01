"""Customers mappers."""

from shopflow.modules.customers.application.dtos.customer import CustomerCreate, CustomerOut, CustomerUpdate
from shopflow.modules.customers.domain.models.customer import Customer


def domain_to_dto(c: Customer) -> CustomerOut:
    return CustomerOut(
        id=str(c.id), customer_unique_id=c.customer_unique_id,
        customer_zip_code_prefix=c.customer_zip_code_prefix,
        customer_city=c.customer_city, customer_state=c.customer_state, user_id=c.user_id,
    )


def dto_to_domain(dto: CustomerCreate) -> Customer:
    return Customer(
        customer_unique_id=dto.customer_unique_id,
        customer_zip_code_prefix=dto.customer_zip_code_prefix,
        customer_city=dto.customer_city,
        customer_state=dto.customer_state,
    )


def update_domain_from_dto(c: Customer, dto: CustomerUpdate) -> None:
    for field, value in dto.model_dump(exclude_unset=True).items():
        setattr(c, field, value)
    c.touch()


__all__ = ["domain_to_dto", "dto_to_domain", "update_domain_from_dto"]
