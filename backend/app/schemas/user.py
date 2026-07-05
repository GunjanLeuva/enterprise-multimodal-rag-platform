"""Pydantic schemas for user-related requests and responses."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Payload for registering a new user."""

    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)


class UserLogin(BaseModel):
    """Payload for authenticating an existing user."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Public-facing user representation — never includes the password."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    email: EmailStr
    is_active: bool


class Token(BaseModel):
    """JWT access token response."""

    access_token: str
    token_type: str = "bearer"