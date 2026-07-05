"""Authentication dependency for protected routes.

Extracts the bearer token from the Authorization header, decodes it
via the existing security utilities, and resolves the corresponding
authenticated User for injection into route handlers.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token
from app.models.user import User, get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

_INVALID_TOKEN_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Resolve the authenticated user from a validated JWT bearer token."""

    payload = decode_access_token(token)

    if payload is None:
        raise _INVALID_TOKEN_ERROR

    user_id = payload.get("sub")

    if user_id is None:
        raise _INVALID_TOKEN_ERROR

    user = get_user_by_id(user_id)

    if user is None:
        raise _INVALID_TOKEN_ERROR

    return user