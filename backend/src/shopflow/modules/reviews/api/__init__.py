"""Reviews API __init__."""

from shopflow.modules.reviews.api.controllers.review import router as reviews_router

__all__ = ["reviews_router"]
