from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class BaseTaskPayload(BaseModel):
    document_id: UUID
    batch_id: UUID
    user_id: UUID
    s3_key: str


class XmlTaskPayload(BaseTaskPayload):
    doc_type: Literal["xml"] = "xml"


class PdfTaskPayload(BaseTaskPayload):
    doc_type: Literal["pdf"] = "pdf"


class ImageTaskPayload(BaseTaskPayload):
    doc_type: Literal["img"] = "img"
    source: Literal["direct", "pdf_fallback"] = "direct"


class UploadConfirmationNotification(BaseModel):
    document_id: UUID
    batch_id: UUID
