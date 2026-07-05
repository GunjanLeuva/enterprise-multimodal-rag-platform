"""Workspace management endpoints.

Every route requires authentication via get_current_user. Reading a
specific workspace is further restricted to its owner or members.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps.auth import get_current_user
from app.core.logging import get_logger
from app.models.user import User
from app.models.workspace import (
    Workspace,
    generate_workspace_id,
    get_workspace_by_id,
    is_member,
    list_workspaces_for_user,
    save_workspace,
)
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse

router = APIRouter(prefix="/workspaces", tags=["workspaces"])
logger = get_logger(__name__)


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    payload: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
) -> WorkspaceResponse:
    """Create a new workspace owned by the current user."""
    workspace = Workspace(
        id=generate_workspace_id(),
        name=payload.name,
        owner_id=current_user.id,
        members=[current_user.id],  # owner is implicitly a member
    )
    save_workspace(workspace)

    logger.info("Workspace created: %s by user %s", workspace.id, current_user.id)
    return WorkspaceResponse.model_validate(workspace)


@router.get("", response_model=list[WorkspaceResponse])
async def list_my_workspaces(
    current_user: User = Depends(get_current_user),
) -> list[WorkspaceResponse]:
    """List all workspaces the current user owns or belongs to."""
    workspaces = list_workspaces_for_user(current_user.id)
    return [WorkspaceResponse.model_validate(workspace) for workspace in workspaces]


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
) -> WorkspaceResponse:
    """Retrieve a single workspace. Restricted to its owner or members."""
    workspace = get_workspace_by_id(workspace_id)
    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found.",
        )

    if not is_member(workspace, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this workspace.",
        )

    return WorkspaceResponse.model_validate(workspace)