"""Customers domain models."""

from __future__ import annotations

from shopflow.shared.domain.base_entity import BaseEntity


class Customer(BaseEntity):
    def __init__(
        self,
        id: str | None = None,
        customer_unique_id: str = "",
        customer_zip_code_prefix: str = "",
        customer_city: str = "",
        customer_state: str = "",
        user_id: str | None = None,
    ):
        super().__init__()
        self.id = id or self.id
        self.customer_unique_id = customer_unique_id
        self.customer_zip_code_prefix = customer_zip_code_prefix
        self.customer_city = customer_city
        self.customer_state = customer_state
        self.user_id = user_id

    def update_location(
        self, zip_code_prefix: str, city: str, state: str
    ) -> None:
        self.customer_zip_code_prefix = zip_code_prefix
        self.customer_city = city
        self.customer_state = state
        self.touch()


__all__ = ["Customer"]
