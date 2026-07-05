"""Document upload endpoints.

Every route requires authentication and workspace membership. Uploads
are validated by size and content type. Text extraction happens
immediately only for plain text files; PDF text extraction is deferred
to the document-processing phase (PyMuPDF/Unstructured) — PDFs are
accepted and stored with raw_text left unset for now.
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.api.deps.auth import get_current_user
from app.core.logging import get_logger
from app.models.document import (
    Document,
    generate_document_id,
    get_document_by_id,
    list_documents_for_workspace,
    save_document,
)
from app.models.user import User
from app.models.workspace import Workspace, get_workspace_by_id, is_member
from app.schemas.document import DocumentDetailResponse, DocumentResponse

router = APIRouter(prefix="/workspaces/{workspace_id}/documents", tags=["documents"])
logger = get_logger(__name__)

MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_CONTENT_TYPES = {"text/plain", "application/pdf"}


def _require_workspace_member(workspace_id: str, current_user: User) -> Workspace:
    """Fetch a workspace and enforce membership, or raise 404/403."""
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

    return workspace


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    workspace_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
) -> DocumentResponse:
    """Upload a document (TXT or PDF) into a workspace."""
    _require_workspace_member(workspace_id, current_user)

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Allowed types: TXT, PDF.",
        )

    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE_BYTES:
        # 413 status code used as a literal to avoid depending on a
        # specific starlette constant name (renamed across versions).
        raise HTTPException(
            status_code=413,
            detail="File exceeds the maximum upload size of 10 MB.",
        )

    # Immediate extraction only for plain text; PDF parsing arrives with
    # the document-processing pipeline in a later phase.
    raw_text = (
        content.decode("utf-8", errors="replace")
        if file.content_type == "text/plain"
        else None
    )

    document = Document(
        id=generate_document_id(),
        workspace_id=workspace_id,
        filename=file.filename or "untitled",
        content_type=file.content_type,
        size=len(content),
        raw_text=raw_text,
        uploaded_by=current_user.id,
    )
    save_document(document)

    logger.info(
        "Document uploaded: %s (%s, %d bytes) into workspace %s by user %s",
        document.id,
        document.content_type,
        document.size,
        workspace_id,
        current_user.id,
    )
    return DocumentResponse.model_validate(document)


@router.get("", response_model=list[DocumentResponse])
async def list_documents(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
) -> list[DocumentResponse]:
    """List all documents in a workspace."""
    _require_workspace_member(workspace_id, current_user)
    documents = list_documents_for_workspace(workspace_id)
    return [DocumentResponse.model_validate(document) for document in documents]


@router.get("/{document_id}", response_model=DocumentDetailResponse)
async def get_document(
    workspace_id: str,
    document_id: str,
    current_user: User = Depends(get_current_user),
) -> DocumentDetailResponse:
    """Retrieve a single document, including extracted text if available."""
    _require_workspace_member(workspace_id, current_user)

    document = get_document_by_id(document_id)
    if document is None or document.workspace_id != workspace_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return DocumentDetailResponse.model_validate(document)