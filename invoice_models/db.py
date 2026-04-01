from datetime import date, datetime
from decimal import Decimal
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
    promoted_at: datetime | None = None


class Entidade(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    # CNPJ only
    documento: str
    nome: str
    uf: str
    cnae_fiscal: str
    cnae_fiscal_descricao: str
    created_at: datetime


class Invoice(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    chave_acesso: str
    document_id: UUID
    user_id: UUID
    # Emitente is always a company
    cnpj_emitente: str
    # Destinatário is a company or individual
    destinatario_cpf: str | None = None
    destinatario_cnpj: str | None = None
    destinatario_nome: str
    data_emissao: date
    numero_nota: str
    serie: str
    valor_total: Decimal
    doc_type: DocType
    confidence: int | None = None
    created_at: datetime


class InvoiceItem(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: int
    chave_acesso: str
    user_id: UUID
    numero_item: int
    codigo_produto: str
    descricao: str
    ncm: str
    cfop: str
    cst_csosn: str
    new_cfop: str
    unidade: str
    quantidade: Decimal | None = None
    valor_unitario: Decimal | None = None
    valor_total_item: Decimal | None = None
