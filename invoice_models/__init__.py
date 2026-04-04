from .api import (
    BatchPresignRequest,
    BatchPresignResponse,
    BatchStatusResponse,
    DocumentListResponse,
    DocumentMetadata,
    DocumentPresignUrl,
    DocumentStatusItem,
    DocumentDetailResponse,
)
from .db import Batch, Document, Entidade, Invoice, InvoiceItem, User
from .enums import BatchStatus, DocType, DocumentStatus, MimeType
from .extraction import (
    FieldOutput,
    ImageExtractionResult,
    ImageLineItem,
    NfeLineItem,
    NfeXmlResult,
    PdfExtractionResult,
    PdfLineItem,
    ProcessorResult,
    RoutingOverride,
)
from .tasks import (
    BaseTaskPayload,
    ImageTaskPayload,
    PdfTaskPayload,
    UploadConfirmationNotification,
    XmlTaskPayload,
)
from .validators import (
    CNPJ,
    CPF,
    BRLDecimal,
    ChaveAcesso,
    FlexibleDate,
    UFCode,
    ValidationResult,
    validate_uf,
    validate_cnpj,
    validate_cpf,
    validate_cpf_ou_cnpj,
    validate_data,
    validate_moeda_brl,
    validate_texto,
    validate_texto_numerico_44,
)

__all__ = [
    # enums
    "DocType",
    "BatchStatus",
    "DocumentStatus",
    "MimeType",
    # validators — standalone functions
    "ValidationResult",
    "validate_cnpj",
    "validate_cpf",
    "validate_cpf_ou_cnpj",
    "validate_moeda_brl",
    "validate_data",
    "validate_texto_numerico_44",
    "validate_uf",
    "validate_texto",
    # validators — Annotated types
    "CNPJ",
    "CPF",
    "BRLDecimal",
    "FlexibleDate",
    "ChaveAcesso",
    "UFCode",
    # db — pipeline
    "User",
    "Batch",
    "Document",
    # db — analytics
    "Entidade",
    "Invoice",
    "InvoiceItem",
    # api
    "DocumentMetadata",
    "BatchPresignRequest",
    "DocumentPresignUrl",
    "BatchPresignResponse",
    "BatchStatusResponse",
    "DocumentStatusItem",
    "DocumentListResponse",
    "DocumentDetailResponse",
    # tasks
    "UploadConfirmationNotification",
    "BaseTaskPayload",
    "XmlTaskPayload",
    "PdfTaskPayload",
    "ImageTaskPayload",
    # extraction
    "FieldOutput",
    "RoutingOverride",
    "NfeLineItem",
    "NfeXmlResult",
    "PdfLineItem",
    "PdfExtractionResult",
    "ImageLineItem",
    "ImageExtractionResult",
    "ProcessorResult",
]
