"""Workspace domain model.

Defines the core Workspace entity and a temporary in-memory store,
mirroring the pattern used for User in app/models/user.py. This store
is a placeholder — it will be replaced by a PostgreSQL-backed
repository once persistence is introduced, at which point RAG document
collections will attach to workspaces via a foreign key.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Workspace:
    """Core workspace entity — an isolated space for documents and chats."""

    id: str
    name: str
    owner_id: str
    members: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


_workspaces_by_id: dict[str, Workspace] = {}


def generate_workspace_id() -> str:
    """Generate a unique workspace identifier."""
    return str(uuid.uuid4())


def save_workspace(workspace: Workspace) -> None:
    """Persist a workspace in the in-memory store."""
    _workspaces_by_id[workspace.id] = workspace


def get_workspace_by_id(workspace_id: str) -> Workspace | None:
    """Look up a workspace by id."""
    return _workspaces_by_id.get(workspace_id)


def list_workspaces_for_user(user_id: str) -> list[Workspace]:
    """Return all workspaces where the given user is owner or member."""
    return [
        workspace
        for workspace in _workspaces_by_id.values()
        if is_member(workspace, user_id)
    ]


def is_member(workspace: Workspace, user_id: str) -> bool:
    """Check whether a user is the owner or a member of a workspace."""
    return user_id == workspace.owner_id or user_id in workspace.members