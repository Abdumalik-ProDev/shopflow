"""Shared domain base types."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class DomainEvent:
    event_id: UUID = field(default_factory=uuid4)
    occurred_on: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: str = field(init=False)

    def __post_init__(self) -> None:
        self.event_type = self.__class__.__name__


@dataclass
class BaseEntity:
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)


@dataclass
class AggregateRoot(BaseEntity):
    _domain_events: list[DomainEvent] = field(default_factory=list, repr=False, compare=False)

    def add_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def clear_events(self) -> None:
        self._domain_events.clear()

    @property
    def domain_events(self) -> list[DomainEvent]:
        return list(self._domain_events)
