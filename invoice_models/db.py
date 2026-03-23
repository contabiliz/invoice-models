from datetime import datetime
from typing import Any, ClassVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .enums import BatchStatus, DocType, DocumentStatus


class User(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class Batch(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    status: BatchStatus
    total_documents: int
    queued_count: int
    completed_count: int
    failed_count: int
    created_at: datetime
    updated_at: datetime


class Document(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: UUID
    batch_id: UUID
    user_id: UUID
    original_filename: str
    s3_key: str
    file_size: int
    doc_type: DocType
    status: DocumentStatus
    extracted_data: dict[str, Any] | None = None
    error_reason: str | None = None
    retry_count: int = 0
    created_at: datetime
    updated_at: datetime
    processing_started_at: datetime | None = None
    completed_at: datetime | None = None
