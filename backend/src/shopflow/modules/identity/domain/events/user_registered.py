"""Identity domain events."""

from __future__ import annotations

from shopflow.shared.domain.base_entity import DomainEvent


class UserRegistered(DomainEvent):
    def __init__(self, user_id: str, email: str):
        super().__init__()
        self.user_id = user_id
        self.email = email


__all__ = ["UserRegistered"]
