from decimal import Decimal

from pydantic import BaseModel

from .common import FieldOutput


class PdfLineItem(BaseModel):
    descricao: str
    quantidade: Decimal | None = None
    unidade: str | None = None
    valor_unitario: Decimal | None = None
    valor_total_item: Decimal | None = None
    cst_csosn: str | None = None
    cfop: str | None = None
    ncm: str | None = None


class PdfExtractionResult(BaseModel):
    chave_acesso: FieldOutput
    cnpj_emitente: FieldOutput
    documento_destinatario: FieldOutput
    nome_destinatario: FieldOutput
    uf_destinatario: FieldOutput
    data_emissao: FieldOutput
    valor_total_nota: FieldOutput
    numero_nota: FieldOutput
    serie: FieldOutput
    items: list[PdfLineItem]
    table_confidence: float
