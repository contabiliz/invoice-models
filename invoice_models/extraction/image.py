from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, field_validator

from ..validators import validate_cnpj, validate_cpf_ou_cnpj, validate_data, validate_moeda_brl


class ImageLineItem(BaseModel):
    descricao: str
    quantidade: Decimal | None = None
    unidade: str | None = None
    valor_unitario: Decimal | None = None
    valor_total: Decimal | None = None


class ImageExtractionResult(BaseModel):
    cnpj_emitente: str | None = None
    nome_emitente: str | None = None
    documento_destinatario: str | None = None
    nome_destinatario: str | None = None
    data_emissao: date | None = None
    valor_total_nota: Decimal | None = None
    numero_nota: str | None = None
    items: list[ImageLineItem] = []

    @field_validator("cnpj_emitente", mode="before")
    @classmethod
    def _cnpj(cls, v: str | None) -> str | None:
        if v is None:
            return None
        result = validate_cnpj(v)
        if not result.ok:
            raise ValueError(result.reason)
        return result.normalized_value

    @field_validator("documento_destinatario", mode="before")
    @classmethod
    def _doc_dest(cls, v: str | None) -> str | None:
        if v is None:
            return None
        result = validate_cpf_ou_cnpj(v)
        if not result.ok:
            raise ValueError(result.reason)
        return result.normalized_value

    @field_validator("data_emissao", mode="before")
    @classmethod
    def _data(cls, v: object) -> date | None:
        if v is None or isinstance(v, date):
            return v
        if isinstance(v, str):
            result = validate_data(v)
            if not result.ok:
                raise ValueError(result.reason)
            return datetime.strptime(result.normalized_value, "%Y-%m-%d").date()  # type: ignore[arg-type]
        raise ValueError(f"Cannot convert {type(v).__name__} to date")

    @field_validator("valor_total_nota", mode="before")
    @classmethod
    def _valor(cls, v: object) -> Decimal | None:
        if v is None or isinstance(v, Decimal):
            return v
        if isinstance(v, str):
            result = validate_moeda_brl(v)
            if not result.ok:
                raise ValueError(result.reason)
            return Decimal(result.normalized_value)  # type: ignore[arg-type]
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        raise ValueError(f"Cannot convert {type(v).__name__} to Decimal")
