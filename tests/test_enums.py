from invoice_models.enums import BatchStatus, DocType, DocumentStatus, MimeType


def test_doc_type_values():
    assert DocType.xml == "xml"
    assert DocType.pdf == "pdf"
    assert DocType.img == "img"


def test_batch_status_values():
    assert BatchStatus.pending_upload == "pending_upload"
    assert BatchStatus.processing == "processing"
    assert BatchStatus.completed == "completed"
    assert BatchStatus.partial_failure == "partial_failure"
    assert BatchStatus.failed == "failed"


def test_document_status_values():
    assert DocumentStatus.pending_upload == "pending_upload"
    assert DocumentStatus.upload_confirmed == "upload_confirmed"
    assert DocumentStatus.queued == "queued"
    assert DocumentStatus.processing == "processing"
    assert DocumentStatus.completed == "completed"
    assert DocumentStatus.failed == "failed"


def test_mime_type_values():
    assert MimeType.jpeg == "image/jpeg"
    assert MimeType.png == "image/png"
    assert MimeType.webp == "image/webp"
    assert MimeType.tiff == "image/tiff"
    assert MimeType.pdf == "application/pdf"
    assert MimeType.xml == "application/xml"
    assert MimeType.xml_text == "text/xml"


def test_enums_are_strings():
    assert isinstance(DocType.xml, str)
    assert isinstance(BatchStatus.completed, str)
    assert isinstance(MimeType.pdf, str)
