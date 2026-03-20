from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ..enums import DocType, DocumentStatus


class DocumentStatusItem(BaseModel):
    document_id: UUID
    filename: str
    doc_type: DocType
    status: DocumentStatus
    error_reason: str | None = None
    created_at: datetime
    updated_at: datetime


class DocumentListResponse(BaseModel):
    total: int
    page: int
    items: list[DocumentStatusItem]
