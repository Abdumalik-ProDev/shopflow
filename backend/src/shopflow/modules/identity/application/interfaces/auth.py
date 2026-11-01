"""Identity application interfaces."""

from typing import Optional

from shopflow.modules.identity.domain.models.user import User


class PasswordHasher:
    async def hash(self, password: str) -> str:
        raise NotImplementedError

    async def verify(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError


class TokenService:
    async def create_access_token(self, user_id: str) -> str:
        raise NotImplementedError

    async def decode_token(self, token: str) -> Optional[dict]:
        raise NotImplementedError


__all__ = ["PasswordHasher", "TokenService"]
