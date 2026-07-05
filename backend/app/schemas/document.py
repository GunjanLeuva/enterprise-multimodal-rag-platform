"""Pydantic schemas for document-related responses."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    """Public-facing document metadata (excludes extracted text)."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    workspace_id: str
    filename: str
    content_type: str
    size: int
    uploaded_by: str
    created_at: datetime


class DocumentDetailResponse(DocumentResponse):
    """Document representation including extracted text, if available."""

    raw_text: str | None