"""Custom application exceptions."""

from typing import Any


class ShopFlowError(Exception):
    """Base application exception."""

    def __init__(self, message: str, code: str | None = None, details: dict[str, Any] | None = None):
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or {}
        super().__init__(message)


class NotFoundError(ShopFlowError):
    pass


class ConflictError(ShopFlowError):
    pass


class ValidationError(ShopFlowError):
    pass


class AuthorizationError(ShopFlowError):
    pass


class AuthenticationError(ShopFlowError):
    pass
