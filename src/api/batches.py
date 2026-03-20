from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..enums import BatchStatus, MimeType


class DocumentMetadata(BaseModel):
    filename: str
    mime_type: MimeType
    file_size: int = Field(ge=1, le=52_428_800)


class BatchPresignRequest(BaseModel):
    documents: list[DocumentMetadata] = Field(min_length=1, max_length=500)


class DocumentPresignUrl(BaseModel):
    document_id: UUID
    upload_url: str
    upload_url_expires_at: datetime
    object_key: str


class BatchPresignResponse(BaseModel):
    batch_id: UUID
    documents: list[DocumentPresignUrl]


class BatchStatusResponse(BaseModel):
    batch_id: UUID
    status: BatchStatus
    total: int
    queued: int
    processing: int
    completed: int
    failed: int
    created_at: datetime
    completed_at: datetime | None = None
