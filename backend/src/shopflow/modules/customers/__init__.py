"""Customers module."""

from shopflow.modules.identity.infrastructure.persistence.models import Base as _i  # noqa
from shopflow.modules.customers.infrastructure.persistence.models import Base, CustomerRow
from shopflow.modules.customers.infrastructure.repositories.customer import SqlAlchemyCustomerRepository
from shopflow.modules.customers.application.services.customer import CustomerService
from shopflow.modules.customers.api.controllers.customer import router as customers_router

__all__ = ["Base", "CustomerRow", "SqlAlchemyCustomerRepository", "CustomerService", "customers_router"]
