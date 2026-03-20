from datetime import datetime, timezone
from uuid import uuid4

from invoice_models.db import Batch, Document, User
from invoice_models.enums import BatchStatus, DocType, DocumentStatus


_NOW = datetime.now(tz=timezone.utc)
_UUID = uuid4()


def test_user_construction():
    u = User(id=_UUID, created_at=_NOW, updated_at=_NOW)
    assert u.id == _UUID


def test_user_from_attributes():
    class FakeRow:
        id = _UUID
        created_at = _NOW
        updated_at = _NOW

    u = User.model_validate(FakeRow(), from_attributes=True)
    assert u.id == _UUID


def test_batch_construction():
    b = Batch(
        id=_UUID,
        user_id=_UUID,
        status=BatchStatus.processing,
        total_documents=10,
        queued_count=5,
        completed_count=3,
        failed_count=2,
        created_at=_NOW,
        updated_at=_NOW,
    )
    assert b.status == BatchStatus.processing
    assert b.total_documents == 10


def test_document_defaults():
    d = Document(
        id=_UUID,
        batch_id=_UUID,
        user_id=_UUID,
        original_filename="invoice.xml",
        s3_key="user/batch/doc/invoice.xml",
        file_size=1024,
        doc_type=DocType.xml,
        status=DocumentStatus.pending_upload,
        created_at=_NOW,
        updated_at=_NOW,
    )
    assert d.retry_count == 0
    assert d.extracted_data is None
    assert d.error_reason is None
    assert d.processing_started_at is None
    assert d.completed_at is None


def test_document_with_extracted_data():
    d = Document(
        id=_UUID,
        batch_id=_UUID,
        user_id=_UUID,
        original_filename="invoice.xml",
        s3_key="user/batch/doc/invoice.xml",
        file_size=1024,
        doc_type=DocType.xml,
        status=DocumentStatus.completed,
        extracted_data={"chave_acesso": "1" * 44},
        created_at=_NOW,
        updated_at=_NOW,
    )
    assert d.extracted_data == {"chave_acesso": "1" * 44}
