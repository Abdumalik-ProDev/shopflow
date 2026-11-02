"""Controllers layer exports and master API router."""

from fastapi import APIRouter

from app.controllers.analytics_controller import router as analytics_router
from app.controllers.auth_controller import router as auth_router
from app.controllers.customer_controller import router as customer_router
from app.controllers.order_controller import router as order_router
from app.controllers.product_controller import router as product_router
from app.controllers.recommendation_controller import router as recommendation_router
from app.controllers.seller_controller import router as seller_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(product_router)
api_router.include_router(customer_router)
api_router.include_router(seller_router)
api_router.include_router(order_router)
api_router.include_router(analytics_router)
api_router.include_router(recommendation_router)

__all__ = ["api_router"]
