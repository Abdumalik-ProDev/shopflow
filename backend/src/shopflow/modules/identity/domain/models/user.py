"""Identity domain models."""

from __future__ import annotations

from shopflow.shared.domain.base_entity import BaseEntity


class User(BaseEntity):
    def __init__(
        self,
        id: str | None = None,
        email: str = "",
        username: str = "",
        hashed_password: str = "",
        full_name: str = "",
        is_active: bool = True,
        is_superuser: bool = False,
        role: str = "customer",
    ):
        super().__init__()
        self.id = id or self.id
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.role = role

    def activate(self) -> None:
        self.is_active = True
        self.touch()

    def deactivate(self) -> None:
        self.is_active = False
        self.touch()


__all__ = ["User"]
