from datetime import date
from decimal import Decimal

from pydantic import BaseModel, field_validator

from ..validators import validate_cnpj, validate_cpf_ou_cnpj, validate_data, validate_texto_numerico_44


class NfeLineItem(BaseModel):
    numero_item: int
    codigo_produto: str
    descricao: str
    quantidade: Decimal
    unidade: str
    valor_unitario: Decimal
    valor_total_item: Decimal
    ncm: str
    cfop: str


class NfeXmlResult(BaseModel):
    chave_acesso: str
    cnpj_emitente: str
    nome_emitente: str
    documento_destinatario: str
    nome_destinatario: str
    data_emissao: date
    valor_total_nota: Decimal
    numero_nota: str
    serie: str
    items: list[NfeLineItem]

    @field_validator("chave_acesso", mode="before")
    @classmethod
    def _chave(cls, v: str) -> str:
        result = validate_texto_numerico_44(v)
        if not result.ok:
            raise ValueError(result.reason)
        return result.normalized_value  # type: ignore[return-value]

    @field_validator("cnpj_emitente", mode="before")
    @classmethod
    def _cnpj(cls, v: str) -> str:
        result = validate_cnpj(v)
        if not result.ok:
            raise ValueError(result.reason)
        return result.normalized_value  # type: ignore[return-value]

    @field_validator("documento_destinatario", mode="before")
    @classmethod
    def _doc_dest(cls, v: str) -> str:
        result = validate_cpf_ou_cnpj(v)
        if not result.ok:
            raise ValueError(result.reason)
        return result.normalized_value  # type: ignore[return-value]

    @field_validator("data_emissao", mode="before")
    @classmethod
    def _data(cls, v: object) -> object:
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            result = validate_data(v)
            if not result.ok:
                raise ValueError(result.reason)
            from datetime import datetime
            return datetime.strptime(result.normalized_value, "%Y-%m-%d").date()  # type: ignore[arg-type]
        raise ValueError(f"Cannot convert {type(v).__name__} to date")
