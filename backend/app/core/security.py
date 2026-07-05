"""
Security utilities: password hashing and JWT access tokens.

Handles:
- Password hashing (bcrypt)
- Password verification
- JWT token creation & validation
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# ---------------------------------------------------------------------
# Password Hashing Configuration
# ---------------------------------------------------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# ---------------------------------------------------------------------
# Password Utilities
# ---------------------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Hash a plaintext password.

    Note:
    bcrypt only supports passwords up to 72 bytes.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    password = password.strip()

    if not password:
        raise ValueError("Password cannot be empty.")

    # bcrypt limitation
    if len(password.encode("utf-8")) > 72:
        raise ValueError(
            "Password cannot exceed 72 UTF-8 bytes for bcrypt."
        )

    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against its bcrypt hash.
    """
    try:
        return pwd_context.verify(password, hashed_password)
    except Exception:
        return False


# ---------------------------------------------------------------------
# JWT Utilities
# ---------------------------------------------------------------------

def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT access token.
    """

    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=settings.jwt_expire_minutes)
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any] | None:
    """
    Decode and validate a JWT access token.

    Returns:
        dict: JWT payload if valid.
        None: If token is invalid or expired.
    """

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        return None