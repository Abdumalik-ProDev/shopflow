"""Catalog domain models: Product and Category."""

from __future__ import annotations

from shopflow.shared.domain.base_entity import BaseEntity


class Category(BaseEntity):
    def __init__(
        self,
        id: str | None = None,
        name: str = "",
        name_english: str | None = None,
    ):
        super().__init__()
        self.id = id or self.id
        self.name = name
        self.name_english = name_english


class Product(BaseEntity):
    def __init__(
        self,
        id: str | None = None,
        sku: str = "",
        name: str = "",
        description: str = "",
        price: float = 0.0,
        stock_quantity: int = 0,
        category_id: str | None = None,
        seller_id: str | None = None,
        is_active: bool = True,
        weight_g: float | None = None,
        length_cm: float | None = None,
        height_cm: float | None = None,
        width_cm: float | None = None,
        photos_qty: int | None = None,
    ):
        super().__init__()
        self.id = id or self.id
        self.sku = sku
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.category_id = category_id
        self.seller_id = seller_id
        self.is_active = is_active
        self.weight_g = weight_g
        self.length_cm = length_cm
        self.height_cm = height_cm
        self.width_cm = width_cm
        self.photos_qty = photos_qty

    def adjust_stock(self, delta: int) -> None:
        self.stock_quantity += delta
        if self.stock_quantity < 0:
            raise ValueError("Stock cannot be negative")
        self.touch()


__all__ = ["Category", "Product"]
