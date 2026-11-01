"""Identity domain value objects."""

from __future__ import annotations

import re
from dataclasses import dataclass

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not EMAIL_REGEX.match(self.value.strip().lower()):
            raise ValueError(f"Invalid email address: {self.value}")
        object.__setattr__(self, "value", self.value.strip().lower())


__all__ = ["Email"]
