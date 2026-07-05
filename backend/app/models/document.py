"""Document domain model.

Defines the core Document entity and a temporary in-memory store,
mirroring the pattern used for User and Workspace. Raw file bytes are
not retained here — only extracted text and metadata — keeping this
model compatible with a future move to PostgreSQL metadata plus
object storage (e.g. S3) for the underlying files.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Document:
    """Core document entity — a file uploaded into a workspace."""

    id: str
    workspace_id: str
    filename: str
    content_type: str
    size: int
    raw_text: str | None
    uploaded_by: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


_documents_by_id: dict[str, Document] = {}


def generate_document_id() -> str:
    """Generate a unique document identifier."""
    return str(uuid.uuid4())


def save_document(document: Document) -> None:
    """Persist a document in the in-memory store."""
    _documents_by_id[document.id] = document


def get_document_by_id(document_id: str) -> Document | None:
    """Look up a document by id."""
    return _documents_by_id.get(document_id)


def list_documents_for_workspace(workspace_id: str) -> list[Document]:
    """Return all documents belonging to a given workspace."""
    return [
        document
        for document in _documents_by_id.values()
        if document.workspace_id == workspace_id
    ]