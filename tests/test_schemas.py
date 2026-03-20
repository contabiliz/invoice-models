from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from invoice_models.enums import BatchStatus, DocType, DocumentStatus, MimeType
from invoice_models.api import (
    BatchPresignRequest,
    BatchPresignResponse,
    BatchStatusResponse,
    DocumentListResponse,
    DocumentMetadata,
    DocumentPresignUrl,
    DocumentStatusItem,
)


_NOW = datetime.now(tz=timezone.utc)
_UUID = uuid4()


def _doc(**kwargs):
    return DocumentMetadata(filename="f.pdf", mime_type=MimeType.pdf, file_size=1024, **kwargs)


def test_document_metadata_valid():
    m = _doc()
    assert m.mime_type == MimeType.pdf


def test_document_metadata_file_size_zero_rejected():
    with pytest.raises(ValidationError):
        DocumentMetadata(filename="f.pdf", mime_type=MimeType.pdf, file_size=0)


def test_document_metadata_file_size_over_limit_rejected():
    with pytest.raises(ValidationError):
        DocumentMetadata(filename="f.pdf", mime_type=MimeType.pdf, file_size=52_428_801)


def test_document_metadata_invalid_mime_rejected():
    with pytest.raises(ValidationError):
        DocumentMetadata(filename="f.pdf", mime_type="application/octet-stream", file_size=1024)


def test_batch_presign_request_valid():
    r = BatchPresignRequest(documents=[_doc()])
    assert len(r.documents) == 1


def test_batch_presign_request_empty_rejected():
    with pytest.raises(ValidationError):
        BatchPresignRequest(documents=[])


def test_batch_presign_request_501_rejected():
    with pytest.raises(ValidationError):
        BatchPresignRequest(documents=[_doc() for _ in range(501)])


def test_batch_presign_response():
    r = BatchPresignResponse(
        batch_id=_UUID,
        documents=[
            DocumentPresignUrl(
                document_id=_UUID,
                upload_url="https://example.com/upload",
                upload_url_expires_at=_NOW,
                object_key="user/batch/doc/f.pdf",
            )
        ],
    )
    assert len(r.documents) == 1


def test_batch_status_response_no_completed_at():
    r = BatchStatusResponse(
        batch_id=_UUID,
        status=BatchStatus.processing,
        total=10,
        queued=3,
        processing=2,
        completed=4,
        failed=1,
        created_at=_NOW,
    )
    assert r.completed_at is None


def test_document_list_response():
    item = DocumentStatusItem(
        document_id=_UUID,
        filename="invoice.xml",
        doc_type=DocType.xml,
        status=DocumentStatus.completed,
        created_at=_NOW,
        updated_at=_NOW,
    )
    r = DocumentListResponse(total=1, page=1, items=[item])
    assert r.items[0].error_reason is None
