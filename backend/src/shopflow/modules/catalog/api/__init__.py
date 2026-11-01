"""Catalog API __init__."""

from shopflow.modules.catalog.api.controllers.catalog import router as catalog_router

__all__ = ["catalog_router"]
