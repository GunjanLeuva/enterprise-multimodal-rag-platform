"""Application entrypoint.

Wires up the FastAPI app, logging, and CORS. No business logic here —
see app/api, app/services, app/rag in upcoming phases.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    """Log basic startup info."""
    logger.info("Starting %s (env=%s)", settings.app_name, settings.app_env)


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """Liveness probe for local dev / container orchestration."""
    return {"status": "ok", "environment": settings.app_env}