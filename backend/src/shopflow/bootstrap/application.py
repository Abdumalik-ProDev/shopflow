"""Backend bootstrap: DI container and FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shopflow.core.config.settings import settings
from shopflow.core.logging.config import configure_logging

# Module routers
from shopflow.modules.identity.api.controllers.auth import router as auth_router
from shopflow.modules.customers.api.controllers.customer import router as customers_router
from shopflow.modules.sellers.api.controllers.seller import router as sellers_router
from shopflow.modules.catalog.api.controllers.catalog import router as catalog_router
from shopflow.modules.orders.api.controllers.order import router as orders_router
from shopflow.modules.payments.api.controllers.payment import router as payments_router
from shopflow.modules.reviews.api.controllers.review import router as reviews_router
from shopflow.modules.recommendations.api.controllers.recommendation import router as recommendations_router
from shopflow.modules.analytics.api.controllers.analytics import router as analytics_router


configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: could initialize DB connection pool, ML model warm-up, etc.
    yield
    # Shutdown: close resources


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth
app.include_router(auth_router)
# Customers
app.include_router(customers_router)
# Sellers
app.include_router(sellers_router)
# Catalog
app.include_router(catalog_router)
# Orders
app.include_router(orders_router)
# Payments
app.include_router(payments_router)
# Reviews
app.include_router(reviews_router)
# Recommendations (ML)
app.include_router(recommendations_router)
# Analytics
app.include_router(analytics_router)


@app.get("/health")
async def health():
    return {"status": "healthy", "service": settings.APP_NAME}


@app.get("/")
async def root():
    return {"message": "Welcome to ShopFlow API", "docs": "/docs"}
