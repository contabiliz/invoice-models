from .api import (
    BatchPresignRequest,
    BatchPresignResponse,
    BatchStatusResponse,
    DocumentListResponse,
    DocumentMetadata,
    DocumentPresignUrl,
    DocumentStatusItem,
)
from .db import Batch, Document, User
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
    validate_cidade_uf,
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
    "validate_cidade_uf",
    "validate_texto",
    # validators — Annotated types
    "CNPJ",
    "CPF",
    "BRLDecimal",
    "FlexibleDate",
    "ChaveAcesso",
    "UFCode",
    # db
    "User",
    "Batch",
    "Document",
    # api
    "DocumentMetadata",
    "BatchPresignRequest",
    "DocumentPresignUrl",
    "BatchPresignResponse",
    "BatchStatusResponse",
    "DocumentStatusItem",
    "DocumentListResponse",
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
