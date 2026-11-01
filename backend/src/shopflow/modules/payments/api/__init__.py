"""Payments API __init__."""

from shopflow.modules.payments.api.controllers.payment import router as payments_router

__all__ = ["payments_router"]
