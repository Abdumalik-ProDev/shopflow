"""Orders API __init__."""

from shopflow.modules.orders.api.controllers.order import router as orders_router

__all__ = ["orders_router"]
