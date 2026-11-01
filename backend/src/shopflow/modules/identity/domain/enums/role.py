"""Identity domain enums."""

from enum import StrEnum


class UserRole(StrEnum):
    CUSTOMER = "customer"
    SELLER = "seller"
    ADMIN = "admin"


class UserStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


__all__ = ["UserRole", "UserStatus"]
