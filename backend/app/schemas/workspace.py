"""Pydantic schemas for workspace-related requests and responses."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WorkspaceCreate(BaseModel):
    """Payload for creating a new workspace."""

    name: str = Field(min_length=2, max_length=100)


class WorkspaceResponse(BaseModel):
    """Public-facing workspace representation."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    owner_id: str
    members: list[str]
    created_at: datetime