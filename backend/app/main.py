"""Application entrypoint.

Wires up the FastAPI app, logging, CORS, and API routers.
No business logic here — only application setup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging, get_logger

# API routers
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.workspaces import router as workspaces_router
from app.api.v1.documents import router as documents_router


# Initialize logging
configure_logging()
logger = get_logger(__name__)


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(workspaces_router, prefix="/api/v1")
app.include_router(documents_router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup() -> None:
    """Log application startup info."""
    logger.info(
        "Starting %s (env=%s)",
        settings.app_name,
        settings.app_env,
    )


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """Liveness probe endpoint."""
    return {
        "status": "ok",
        "environment": settings.app_env,
    }