"""Analytics module."""

from shopflow.modules.analytics.application.services.analytics import AnalyticsService
from shopflow.modules.analytics.api.controllers.analytics import router as analytics_router

__all__ = ["AnalyticsService", "analytics_router"]
