from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from invoice_models.extraction import (
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


_VALID_CHAVE = "1" * 44
_VALID_CNPJ_BARE = "11222333000181"
_VALID_CNPJ_FORMATTED = "11.222.333/0001-81"
_VALID_CPF = "52998224725"


# ---------------------------------------------------------------------------
# FieldOutput
# ---------------------------------------------------------------------------


def test_field_output_found():
    f = FieldOutput(
        value="11.222.333/0001-81",
        confidence=0.95,
        method="ngram",
        raw_text="11222333000181",
    )
    assert f.errors == []


def test_field_output_not_found():
    f = FieldOutput(
        value=None,
        confidence=0.0,
        method="ngram",
        raw_text=None,
        errors=["label not detected"],
    )
    assert f.value is None
    assert len(f.errors) == 1


# ---------------------------------------------------------------------------
# NfeXmlResult
# ---------------------------------------------------------------------------


def _nfe(**overrides):
    defaults = dict(
        chave_acesso=_VALID_CHAVE,
        cnpj_emitente=_VALID_CNPJ_BARE,
        nome_emitente="Empresa Ltda",
        documento_destinatario=_VALID_CPF,
        nome_destinatario="Cliente S.A.",
        data_emissao="31/12/2024",
        valor_total_nota=Decimal("1000.00"),
        numero_nota="001",
        serie="1",
        items=[],
    )
    return NfeXmlResult(**{**defaults, **overrides})


def test_nfe_xml_result_valid():
    r = _nfe()
    assert r.chave_acesso == _VALID_CHAVE
    assert r.cnpj_emitente == _VALID_CNPJ_FORMATTED
    assert r.data_emissao == date(2024, 12, 31)


def test_nfe_xml_result_invalid_chave():
    with pytest.raises(ValidationError):
        _nfe(chave_acesso="123")


def test_nfe_xml_result_invalid_cnpj():
    with pytest.raises(ValidationError):
        _nfe(cnpj_emitente="00000000000000")


def test_nfe_xml_result_invalid_doc_destinatario():
    with pytest.raises(ValidationError):
        _nfe(documento_destinatario="999")


def test_nfe_xml_result_cnpj_destinatario():
    r = _nfe(documento_destinatario=_VALID_CNPJ_BARE)
    assert r.documento_destinatario == _VALID_CNPJ_FORMATTED


def test_nfe_xml_result_with_items():
    item = NfeLineItem(
        numero_item=1,
        codigo_produto="ABC",
        descricao="Produto X",
        quantidade=Decimal("2"),
        unidade="UN",
        valor_unitario=Decimal("10.50"),
        valor_total_item=Decimal("21.00"),
        ncm="12345678",
        cfop="5102",
        cst_csosn="000",
        new_cfop="1102",
    )
    r = _nfe(items=[item])
    assert len(r.items) == 1


# ---------------------------------------------------------------------------
# PdfExtractionResult
# ---------------------------------------------------------------------------


def _field(value=None, confidence=0.9, method="ngram"):
    return FieldOutput(
        value=value, confidence=confidence, method=method, raw_text=value
    )


def test_pdf_extraction_result_valid():
    r = PdfExtractionResult(
        chave_acesso=_field(_VALID_CHAVE),
        cnpj_emitente=_field(_VALID_CNPJ_FORMATTED),
        documento_destinatario=_field(_VALID_CPF),
        nome_destinatario=_field("Cliente"),
        uf_destinatario=_field("SP"),
        data_emissao=_field("2024-12-31"),
        valor_total_nota=_field("1000.00"),
        numero_nota=_field("001"),
        serie=_field("1"),
        items=[],
        table_confidence=0.85,
    )
    assert r.table_confidence == 0.85
    assert r.items == []


def test_pdf_extraction_result_with_line_item():
    item = PdfLineItem(
        descricao="Produto A",
        quantidade=Decimal("2"),
        valor_total_item=Decimal("20.00"),
    )
    r = PdfExtractionResult(
        chave_acesso=_field(),
        cnpj_emitente=_field(),
        documento_destinatario=_field(),
        nome_destinatario=_field(),
        uf_destinatario=_field(),
        data_emissao=_field(),
        valor_total_nota=_field(),
        numero_nota=_field(),
        serie=_field(),
        items=[item],
        table_confidence=0.55,
    )
    assert item.unidade is None
    assert item.ncm is None


# ---------------------------------------------------------------------------
# ImageExtractionResult
# ---------------------------------------------------------------------------


def test_image_extraction_result_all_none():
    r = ImageExtractionResult()
    assert r.cnpj_emitente is None
    assert r.items == []


def test_image_extraction_result_partial():
    r = ImageExtractionResult(
        cnpj_emitente=_VALID_CNPJ_BARE,
        nome_emitente="Empresa",
        valor_total_nota=Decimal("500.00"),
    )
    assert r.cnpj_emitente == _VALID_CNPJ_FORMATTED
    assert r.documento_destinatario is None


def test_image_extraction_result_cnpj_normalized():
    r = ImageExtractionResult(cnpj_emitente=_VALID_CNPJ_BARE)
    assert r.cnpj_emitente == _VALID_CNPJ_FORMATTED


def test_image_extraction_result_invalid_cnpj_rejected():
    with pytest.raises(ValidationError):
        ImageExtractionResult(cnpj_emitente="00000000000000")


def test_image_extraction_result_doc_dest_cpf():
    r = ImageExtractionResult(documento_destinatario=_VALID_CPF)
    assert r.documento_destinatario == _VALID_CPF


def test_image_extraction_result_doc_dest_cnpj():
    r = ImageExtractionResult(documento_destinatario=_VALID_CNPJ_BARE)
    assert r.documento_destinatario == _VALID_CNPJ_FORMATTED


def test_image_extraction_result_invalid_doc_dest_rejected():
    with pytest.raises(ValidationError):
        ImageExtractionResult(documento_destinatario="999")


def test_image_extraction_result_data_emissao_string():
    r = ImageExtractionResult(data_emissao="31/12/2024")
    assert r.data_emissao == date(2024, 12, 31)


def test_image_extraction_result_data_emissao_invalid():
    with pytest.raises(ValidationError):
        ImageExtractionResult(data_emissao="2024/12/31")


def test_image_extraction_result_valor_brl_string():
    r = ImageExtractionResult(valor_total_nota="1.500,00")
    assert r.valor_total_nota == Decimal("1500.00")


def test_image_extraction_result_valor_invalid():
    with pytest.raises(ValidationError):
        ImageExtractionResult(valor_total_nota="not-a-number")


def test_image_extraction_result_with_items():
    r = ImageExtractionResult(
        items=[
            ImageLineItem(
                descricao="Produto A",
                quantidade=Decimal("1"),
                valor_total=Decimal("10.00"),
            )
        ]
    )
    assert len(r.items) == 1


# ---------------------------------------------------------------------------
# ProcessorResult
# ---------------------------------------------------------------------------


def test_processor_result_success():
    r = ProcessorResult(result=_nfe())
    assert not r.is_terminal_failure
    assert r.routing_override is None
    assert r.terminal_reason is None


def test_processor_result_terminal_failure():
    r = ProcessorResult(
        result=None,
        is_terminal_failure=True,
        terminal_reason="magic byte mismatch: not an XML file",
    )
    assert r.is_terminal_failure
    assert r.result is None


def test_processor_result_routing_override():
    r = ProcessorResult(result=None, routing_override=RoutingOverride.IMAGE)
    assert r.routing_override == RoutingOverride.IMAGE
    assert r.routing_override == "image"
