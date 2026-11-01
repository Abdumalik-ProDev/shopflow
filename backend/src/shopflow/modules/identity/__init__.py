"""Identity module package."""

from shopflow.modules.identity.api.controllers.auth import router as auth_router

__all__ = ["auth_router"]
