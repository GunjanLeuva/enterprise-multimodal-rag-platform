"""Authentication endpoints: registration and login.

Uses an in-memory user store (app.models.user) as temporary persistence
until PostgreSQL is introduced. Passwords are hashed with bcrypt; a
successful login returns a signed JWT access token.
"""

from fastapi import APIRouter, HTTPException, status

from app.core.logging import get_logger
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, generate_user_id, get_user_by_email, save_user
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])
logger = get_logger(__name__)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(payload: UserCreate) -> UserResponse:
    """Register a new user."""

    email = payload.email.lower().strip()
    full_name = payload.full_name.strip()

    if get_user_by_email(email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    user = User(
        id=generate_user_id(),
        full_name=full_name,
        email=email,
        hashed_password=hash_password(payload.password),
    )

    save_user(user)

    logger.info("User registered successfully.")
    return UserResponse.model_validate(user)


@router.post("/login", response_model=Token)
async def login(payload: UserLogin) -> Token:
    """Authenticate user and return JWT token."""

    email = payload.email.lower().strip()

    user = get_user_by_email(email)

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive.",
        )

    access_token = create_access_token(subject=user.id)

    logger.info("User login successful.")
    return Token(access_token=access_token)