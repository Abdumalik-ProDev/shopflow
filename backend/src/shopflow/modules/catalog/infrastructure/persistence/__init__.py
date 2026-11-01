"""Catalog infrastructure persistence __init__."""

from shopflow.modules.catalog.infrastructure.persistence.models import (
    Base,
    CategoryRow,
    ProductRow,
)

__all__ = ["Base", "CategoryRow", "ProductRow"]
