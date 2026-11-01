"""Customers domain models."""

from shopflow.shared.domain.base_entity import BaseEntity


class Customer(BaseEntity):
    def __init__(self, id=None, customer_unique_id="", customer_zip_code_prefix="",
                 customer_city="", customer_state="", user_id=None):
        super().__init__()
        self.id = id or self.id
        self.customer_unique_id = customer_unique_id
        self.customer_zip_code_prefix = customer_zip_code_prefix
        self.customer_city = customer_city
        self.customer_state = customer_state
        self.user_id = user_id


__all__ = ["Customer"]
