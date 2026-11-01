"""Catalog mappers."""

from shopflow.modules.catalog.application.dtos.catalog import (
    CategoryCreate, CategoryOut, ProductCreate, ProductOut, ProductUpdate,
)
from shopflow.modules.catalog.domain.models.product import Category, Product


def category_domain_to_dto(c: Category) -> CategoryOut:
    return CategoryOut(id=str(c.id), name=c.name, name_english=c.name_english)


def product_domain_to_dto(p: Product) -> ProductOut:
    return ProductOut(
        id=str(p.id), sku=p.sku, name=p.name, description=p.description,
        price=p.price, stock_quantity=p.stock_quantity, category_id=p.category_id,
        seller_id=p.seller_id, is_active=p.is_active, weight_g=p.weight_g,
        length_cm=p.length_cm, height_cm=p.height_cm, width_cm=p.width_cm,
        photos_qty=p.photos_qty,
    )


def product_dto_to_domain(dto: ProductCreate) -> Product:
    return Product(
        sku=dto.sku, name=dto.name, description=dto.description, price=dto.price,
        stock_quantity=dto.stock_quantity, category_id=dto.category_id,
        seller_id=dto.seller_id, is_active=dto.is_active, weight_g=dto.weight_g,
        length_cm=dto.length_cm, height_cm=dto.height_cm, width_cm=dto.width_cm,
        photos_qty=dto.photos_qty,
    )


def product_update_domain_from_dto(p: Product, dto: ProductUpdate) -> None:
    for field, value in dto.model_dump(exclude_unset=True).items():
        setattr(p, field, value)
    p.touch()


__all__ = [
    "category_domain_to_dto", "product_domain_to_dto",
    "product_dto_to_domain", "product_update_domain_from_dto",
]
