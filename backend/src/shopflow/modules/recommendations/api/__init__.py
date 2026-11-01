"""Recommendations API __init__."""

from shopflow.modules.recommendations.api.controllers.recommendation import router as recommendations_router

__all__ = ["recommendations_router"]
