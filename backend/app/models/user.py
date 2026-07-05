"""User domain model.

Defines the core User entity and a temporary in-memory store. This
store is a placeholder — it will be replaced by a PostgreSQL-backed
repository in a later phase.
"""

import uuid
from dataclasses import dataclass


@dataclass
class User:
    """Core user entity."""

    id: str
    full_name: str
    email: str
    hashed_password: str
    is_active: bool = True


# Keyed by lowercased email for O(1) uniqueness checks during registration.
_users_by_email: dict[str, User] = {}


def get_user_by_email(email: str) -> User | None:
    """Look up a user by email address (case-insensitive)."""
    return _users_by_email.get(email.lower())

def get_user_by_id(user_id: str) -> User | None:
    """Look up a user by id."""
    return next(
        (user for user in _users_by_email.values() if user.id == user_id),
        None,
    )


def save_user(user: User) -> None:
    """Persist a user in the in-memory store."""
    _users_by_email[user.email.lower()] = user


def generate_user_id() -> str:
    """Generate a unique user identifier."""
    return str(uuid.uuid4())