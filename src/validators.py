from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Annotated

from pydantic import AfterValidator, BeforeValidator, Field


# ---------------------------------------------------------------------------
# ValidationResult — returned by all standalone validator functions.
# Used directly by invoice-processors during candidate scoring.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    normalized_value: str | None
    reason: str | None = None


# ---------------------------------------------------------------------------
# CNPJ
# ---------------------------------------------------------------------------

_CNPJ_WEIGHTS_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
_CNPJ_WEIGHTS_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]


def validate_cnpj(raw: str) -> ValidationResult:
    digits = "".join(c for c in raw if c.isdigit())
    if len(digits) != 14:
        return ValidationResult(False, None, f"CNPJ must have 14 digits, got {len(digits)}")
    if len(set(digits)) == 1:
        return ValidationResult(False, None, "CNPJ cannot be all the same digit")
    for weights, pos in [(_CNPJ_WEIGHTS_1, 12), (_CNPJ_WEIGHTS_2, 13)]:
        total = sum(int(d) * w for d, w in zip(digits, weights))
        r = total % 11
        expected = 0 if r < 2 else 11 - r
        if expected != int(digits[pos]):
            return ValidationResult(False, None, f"CNPJ check digit {pos - 11} is invalid")
    normalized = f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"
    return ValidationResult(True, normalized)


def _pydantic_cnpj(v: str) -> str:
    result = validate_cnpj(v)
    if not result.ok:
        raise ValueError(result.reason)
    return result.normalized_value  # type: ignore[return-value]


CNPJ = Annotated[str, AfterValidator(_pydantic_cnpj)]


# ---------------------------------------------------------------------------
# CPF
# ---------------------------------------------------------------------------

_CPF_WEIGHTS_1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
_CPF_WEIGHTS_2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]


def validate_cpf(raw: str) -> ValidationResult:
    digits = "".join(c for c in raw if c.isdigit())
    if len(digits) != 11:
        return ValidationResult(False, None, f"CPF must have 11 digits, got {len(digits)}")
    if len(set(digits)) == 1:
        return ValidationResult(False, None, "CPF cannot be all the same digit")
    for weights, pos in [(_CPF_WEIGHTS_1, 9), (_CPF_WEIGHTS_2, 10)]:
        total = sum(int(d) * w for d, w in zip(digits, weights))
        r = total % 11
        expected = 0 if r < 2 else 11 - r
        if expected != int(digits[pos]):
            return ValidationResult(False, None, f"CPF check digit {pos - 8} is invalid")
    return ValidationResult(True, digits)


def validate_cpf_ou_cnpj(raw: str) -> ValidationResult:
    digits = "".join(c for c in raw if c.isdigit())
    if len(digits) == 14:
        return validate_cnpj(raw)
    if len(digits) == 11:
        return validate_cpf(raw)
    return ValidationResult(False, None, f"Expected 11 (CPF) or 14 (CNPJ) digits, got {len(digits)}")


def _pydantic_cpf(v: str) -> str:
    result = validate_cpf(v)
    if not result.ok:
        raise ValueError(result.reason)
    return result.normalized_value  # type: ignore[return-value]


CPF = Annotated[str, AfterValidator(_pydantic_cpf)]


# ---------------------------------------------------------------------------
# BRL monetary value
# ---------------------------------------------------------------------------

def validate_moeda_brl(raw: str) -> ValidationResult:
    try:
        normalized = raw.replace(".", "").replace(",", ".") if "," in raw else raw
        Decimal(normalized)
        return ValidationResult(True, normalized)
    except InvalidOperation:
        return ValidationResult(False, None, f"Cannot parse '{raw}' as a BRL decimal")


def _pydantic_brl(value: object) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    if isinstance(value, str):
        result = validate_moeda_brl(value)
        if not result.ok:
            raise ValueError(result.reason)
        return Decimal(result.normalized_value)  # type: ignore[arg-type]
    raise ValueError(f"Cannot convert {type(value).__name__} to Decimal")


BRLDecimal = Annotated[Decimal, BeforeValidator(_pydantic_brl)]


# ---------------------------------------------------------------------------
# Date
# ---------------------------------------------------------------------------

_DATE_FORMATS = ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d/%m/%y")


def validate_data(raw: str) -> ValidationResult:
    for fmt in _DATE_FORMATS:
        try:
            return ValidationResult(True, datetime.strptime(raw, fmt).strftime("%Y-%m-%d"))
        except ValueError:
            continue
    return ValidationResult(False, None, f"Cannot parse '{raw}' as a date (expected DD/MM/YYYY, DD-MM-YYYY, or YYYY-MM-DD)")


def _pydantic_date(value: object) -> date:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        result = validate_data(value)
        if not result.ok:
            raise ValueError(result.reason)
        return datetime.strptime(result.normalized_value, "%Y-%m-%d").date()  # type: ignore[arg-type]
    raise ValueError(f"Cannot convert {type(value).__name__} to date")


FlexibleDate = Annotated[date, BeforeValidator(_pydantic_date)]


# ---------------------------------------------------------------------------
# Chave de acesso — exactly 44 digits
# ---------------------------------------------------------------------------

def validate_texto_numerico_44(raw: str) -> ValidationResult:
    if len(raw) == 44 and raw.isdigit():
        return ValidationResult(True, raw)
    return ValidationResult(False, None, f"chave_acesso must be exactly 44 digits, got '{raw}'")


ChaveAcesso = Annotated[str, Field(pattern=r"^\d{44}$")]


# ---------------------------------------------------------------------------
# UF code — Brazilian state abbreviation
# ---------------------------------------------------------------------------

_VALID_UF = frozenset({
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
})


def validate_cidade_uf(raw: str) -> ValidationResult:
    parts = raw.rsplit("/", 1)
    if len(parts) != 2:
        return ValidationResult(False, None, f"Expected format CIDADE/UF, got '{raw}'")
    cidade, uf = parts[0].strip(), parts[1].strip().upper()
    if not cidade:
        return ValidationResult(False, None, "City name cannot be empty")
    if uf not in _VALID_UF:
        return ValidationResult(False, None, f"'{uf}' is not a valid UF code")
    return ValidationResult(True, f"{cidade.upper()}/{uf}")


def _pydantic_uf(v: str) -> str:
    if v not in _VALID_UF:
        raise ValueError(f"'{v}' is not a valid Brazilian UF code")
    return v


UFCode = Annotated[str, AfterValidator(_pydantic_uf)]


# ---------------------------------------------------------------------------
# Texto — non-empty, whitespace-normalized
# ---------------------------------------------------------------------------

def validate_texto(raw: str) -> ValidationResult:
    normalized = " ".join(raw.split())
    if not normalized:
        return ValidationResult(False, None, "Value cannot be empty")
    return ValidationResult(True, normalized)
