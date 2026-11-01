"""Customers API __init__."""

from shopflow.modules.customers.api.controllers.customer import router as customers_router

__all__ = ["customers_router"]
