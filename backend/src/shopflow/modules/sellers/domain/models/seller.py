"""Sellers domain models."""

from shopflow.shared.domain.base_entity import BaseEntity


class Seller(BaseEntity):
    def __init__(self, id=None, seller_zip_code_prefix="", seller_city="", seller_state="", user_id=None):
        super().__init__()
        self.id = id or self.id
        self.seller_zip_code_prefix = seller_zip_code_prefix
        self.seller_city = seller_city
        self.seller_state = seller_state
        self.user_id = user_id


__all__ = ["Seller"]
