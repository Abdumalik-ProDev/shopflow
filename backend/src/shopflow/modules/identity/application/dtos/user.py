"""Identity application DTOs."""

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
    full_name: str | None = None
    role: str = "customer"


class UserUpdate(BaseModel):
    full_name: str | None = None
    is_active: bool | None = None
    role: str | None = None


class UserOut(BaseModel):
    id: str
    email: str
    username: str
    full_name: str | None
    is_active: bool
    is_superuser: bool
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: str | None = None


__all__ = ["UserCreate", "UserUpdate", "UserOut", "Token", "TokenData"]
