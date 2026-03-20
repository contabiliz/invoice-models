from datetime import date
from decimal import Decimal

import pytest
from pydantic import BaseModel, ValidationError

from invoice_models.validators import (
    CNPJ,
    CPF,
    BRLDecimal,
    ChaveAcesso,
    FlexibleDate,
    UFCode,
    ValidationResult,
    validate_cnpj,
    validate_cpf,
    validate_cpf_ou_cnpj,
    validate_data,
    validate_moeda_brl,
    validate_texto,
    validate_texto_numerico_44,
    validate_cidade_uf,
)


# ---------------------------------------------------------------------------
# Helpers — thin Pydantic wrappers for Annotated type testing
# ---------------------------------------------------------------------------

class _CNPJ(BaseModel):
    v: CNPJ

class _CPF(BaseModel):
    v: CPF

class _BRL(BaseModel):
    v: BRLDecimal

class _Date(BaseModel):
    v: FlexibleDate

class _Chave(BaseModel):
    v: ChaveAcesso

class _UF(BaseModel):
    v: UFCode


_VALID_CNPJ_BARE = "11222333000181"
_VALID_CNPJ_FORMATTED = "11.222.333/0001-81"
_VALID_CPF_BARE = "52998224725"
_VALID_CPF_FORMATTED = "529.982.247-25"


# ---------------------------------------------------------------------------
# ValidationResult
# ---------------------------------------------------------------------------

def test_validation_result_ok():
    r = ValidationResult(ok=True, normalized_value="foo")
    assert r.ok
    assert r.reason is None

def test_validation_result_fail():
    r = ValidationResult(ok=False, normalized_value=None, reason="bad")
    assert not r.ok
    assert r.normalized_value is None


# ---------------------------------------------------------------------------
# validate_cnpj — standalone
# ---------------------------------------------------------------------------

def test_validate_cnpj_ok():
    r = validate_cnpj(_VALID_CNPJ_BARE)
    assert r.ok
    assert r.normalized_value == _VALID_CNPJ_FORMATTED

def test_validate_cnpj_formatted_input():
    r = validate_cnpj(_VALID_CNPJ_FORMATTED)
    assert r.ok

def test_validate_cnpj_wrong_length():
    r = validate_cnpj("1122233300018")
    assert not r.ok

def test_validate_cnpj_bad_check_digit():
    r = validate_cnpj("11222333000182")
    assert not r.ok

def test_validate_cnpj_all_same():
    r = validate_cnpj("00000000000000")
    assert not r.ok


# ---------------------------------------------------------------------------
# CNPJ — Annotated type
# ---------------------------------------------------------------------------

def test_cnpj_annotated_ok():
    assert _CNPJ(v=_VALID_CNPJ_BARE).v == _VALID_CNPJ_FORMATTED

def test_cnpj_annotated_invalid():
    with pytest.raises(ValidationError):
        _CNPJ(v="11222333000182")


# ---------------------------------------------------------------------------
# validate_cpf — standalone
# ---------------------------------------------------------------------------

def test_validate_cpf_ok():
    r = validate_cpf(_VALID_CPF_BARE)
    assert r.ok
    assert r.normalized_value == _VALID_CPF_BARE

def test_validate_cpf_formatted_input():
    r = validate_cpf(_VALID_CPF_FORMATTED)
    assert r.ok
    assert r.normalized_value == _VALID_CPF_BARE

def test_validate_cpf_bad_check_digit():
    r = validate_cpf("52998224726")
    assert not r.ok

def test_validate_cpf_all_same():
    r = validate_cpf("00000000000")
    assert not r.ok


# ---------------------------------------------------------------------------
# validate_cpf_ou_cnpj — standalone
# ---------------------------------------------------------------------------

def test_validate_cpf_ou_cnpj_cnpj():
    r = validate_cpf_ou_cnpj(_VALID_CNPJ_BARE)
    assert r.ok
    assert r.normalized_value == _VALID_CNPJ_FORMATTED

def test_validate_cpf_ou_cnpj_cpf():
    r = validate_cpf_ou_cnpj(_VALID_CPF_BARE)
    assert r.ok
    assert r.normalized_value == _VALID_CPF_BARE

def test_validate_cpf_ou_cnpj_wrong_length():
    r = validate_cpf_ou_cnpj("123")
    assert not r.ok


# ---------------------------------------------------------------------------
# validate_moeda_brl — standalone
# ---------------------------------------------------------------------------

def test_validate_moeda_brl_full():
    r = validate_moeda_brl("1.234.567,89")
    assert r.ok
    assert r.normalized_value == "1234567.89"

def test_validate_moeda_brl_simple():
    r = validate_moeda_brl("0,50")
    assert r.ok
    assert r.normalized_value == "0.50"

def test_validate_moeda_brl_plain():
    r = validate_moeda_brl("1234.56")
    assert r.ok
    assert r.normalized_value == "1234.56"

def test_validate_moeda_brl_invalid():
    r = validate_moeda_brl("not-a-number")
    assert not r.ok


# ---------------------------------------------------------------------------
# BRLDecimal — Annotated type
# ---------------------------------------------------------------------------

def test_brl_annotated_brl_format():
    assert _BRL(v="1.234,56").v == Decimal("1234.56")

def test_brl_annotated_plain():
    assert _BRL(v="1234.56").v == Decimal("1234.56")

def test_brl_annotated_already_decimal():
    assert _BRL(v=Decimal("99.99")).v == Decimal("99.99")

def test_brl_annotated_invalid():
    with pytest.raises(ValidationError):
        _BRL(v="not-a-number")


# ---------------------------------------------------------------------------
# validate_data — standalone
# ---------------------------------------------------------------------------

def test_validate_data_dd_mm_yyyy():
    r = validate_data("31/12/2024")
    assert r.ok
    assert r.normalized_value == "2024-12-31"

def test_validate_data_dd_mm_yyyy_hyphen():
    r = validate_data("31-12-2024")
    assert r.ok
    assert r.normalized_value == "2024-12-31"

def test_validate_data_iso():
    r = validate_data("2024-12-31")
    assert r.ok
    assert r.normalized_value == "2024-12-31"

def test_validate_data_invalid():
    r = validate_data("32/13/2024")
    assert not r.ok

def test_validate_data_wrong_format():
    r = validate_data("2024/12/31")
    assert not r.ok


# ---------------------------------------------------------------------------
# FlexibleDate — Annotated type
# ---------------------------------------------------------------------------

def test_flexible_date_dd_mm_yyyy():
    assert _Date(v="31/12/2024").v == date(2024, 12, 31)

def test_flexible_date_iso():
    assert _Date(v="2024-12-31").v == date(2024, 12, 31)

def test_flexible_date_passthrough():
    assert _Date(v=date(2024, 1, 1)).v == date(2024, 1, 1)

def test_flexible_date_invalid():
    with pytest.raises(ValidationError):
        _Date(v="2024/12/31")


# ---------------------------------------------------------------------------
# validate_texto_numerico_44 — standalone
# ---------------------------------------------------------------------------

def test_validate_texto_numerico_44_ok():
    r = validate_texto_numerico_44("1" * 44)
    assert r.ok

def test_validate_texto_numerico_44_short():
    r = validate_texto_numerico_44("1" * 43)
    assert not r.ok

def test_validate_texto_numerico_44_non_digit():
    r = validate_texto_numerico_44("A" * 44)
    assert not r.ok


# ---------------------------------------------------------------------------
# ChaveAcesso — Annotated type
# ---------------------------------------------------------------------------

def test_chave_acesso_valid():
    assert _Chave(v="1" * 44).v == "1" * 44

def test_chave_acesso_invalid():
    with pytest.raises(ValidationError):
        _Chave(v="1" * 43)


# ---------------------------------------------------------------------------
# validate_cidade_uf — standalone
# ---------------------------------------------------------------------------

def test_validate_cidade_uf_ok():
    r = validate_cidade_uf("São Paulo/SP")
    assert r.ok
    assert r.normalized_value == "SÃO PAULO/SP"

def test_validate_cidade_uf_invalid_uf():
    r = validate_cidade_uf("Cidade/XX")
    assert not r.ok

def test_validate_cidade_uf_no_slash():
    r = validate_cidade_uf("SãoPaulo")
    assert not r.ok


# ---------------------------------------------------------------------------
# UFCode — Annotated type
# ---------------------------------------------------------------------------

def test_uf_valid():
    assert _UF(v="SP").v == "SP"

def test_uf_invalid():
    with pytest.raises(ValidationError):
        _UF(v="XX")

def test_uf_lowercase_rejected():
    with pytest.raises(ValidationError):
        _UF(v="sp")


# ---------------------------------------------------------------------------
# validate_texto — standalone
# ---------------------------------------------------------------------------

def test_validate_texto_ok():
    r = validate_texto("  hello  world  ")
    assert r.ok
    assert r.normalized_value == "hello world"

def test_validate_texto_empty():
    r = validate_texto("   ")
    assert not r.ok
