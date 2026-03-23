from enum import Enum


class DocType(str, Enum):
    xml = "xml"
    pdf = "pdf"
    img = "img"


class BatchStatus(str, Enum):
    pending_upload = "pending_upload"
    processing = "processing"
    completed = "completed"
    partial_failure = "partial_failure"
    failed = "failed"


class DocumentStatus(str, Enum):
    pending_upload = "pending_upload"
    upload_confirmed = "upload_confirmed"
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class MimeType(str, Enum):
    jpeg = "image/jpeg"
    png = "image/png"
    webp = "image/webp"
    tiff = "image/tiff"
    pdf = "application/pdf"
    xml = "application/xml"
    xml_text = "text/xml"
