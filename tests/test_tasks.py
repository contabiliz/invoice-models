from uuid import uuid4

import pytest
from pydantic import ValidationError

from invoice_models.tasks import (
    ImageTaskPayload,
    PdfTaskPayload,
    UploadConfirmationNotification,
    XmlTaskPayload,
)


_DOC = uuid4()
_BATCH = uuid4()
_USER = uuid4()
_KEY = "user/batch/doc/invoice.xml"


def test_xml_task_payload():
    p = XmlTaskPayload(document_id=_DOC, batch_id=_BATCH, user_id=_USER, s3_key=_KEY)
    assert p.doc_type == "xml"


def test_pdf_task_payload():
    p = PdfTaskPayload(document_id=_DOC, batch_id=_BATCH, user_id=_USER, s3_key=_KEY)
    assert p.doc_type == "pdf"


def test_image_task_payload_default_source():
    p = ImageTaskPayload(document_id=_DOC, batch_id=_BATCH, user_id=_USER, s3_key=_KEY)
    assert p.doc_type == "img"
    assert p.source == "direct"


def test_image_task_payload_pdf_fallback():
    p = ImageTaskPayload(document_id=_DOC, batch_id=_BATCH, user_id=_USER, s3_key=_KEY, source="pdf_fallback")
    assert p.source == "pdf_fallback"


def test_task_payload_serializes_to_json():
    p = XmlTaskPayload(document_id=_DOC, batch_id=_BATCH, user_id=_USER, s3_key=_KEY)
    data = p.model_dump(mode="json")
    assert data["doc_type"] == "xml"
    assert isinstance(data["document_id"], str)


def test_upload_confirmation_notification():
    n = UploadConfirmationNotification(document_id=_DOC, batch_id=_BATCH)
    assert n.document_id == _DOC
