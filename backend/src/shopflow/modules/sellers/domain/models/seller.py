"""Sellers domain models."""

from __future__ import annotations

from shopflow.shared.domain.base_entity import BaseEntity


class Seller(BaseEntity):
    def __init__(
        self,
        id: str | None = None,
        seller_zip_code_prefix: str = "",
        seller_city: str = "",
        seller_state: str = "",
        user_id: str | None = None,
    ):
        super().__init__()
        self.id = id or self.id
        self.seller_zip_code_prefix = seller_zip_code_prefix
        self.seller_city = seller_city
        self.seller_state = seller_state
        self.user_id = user_id

    def update_location(
        self, zip_code_prefix: str, city: str, state: str
    ) -> None:
        self.seller_zip_code_prefix = zip_code_prefix
        self.seller_city = city
        self.seller_state = state
        self.touch()


__all__ = ["Seller"]
