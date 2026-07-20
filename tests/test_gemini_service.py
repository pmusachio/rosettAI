import json
from unittest.mock import MagicMock, patch

import pytest

from app.models.schemas import GeminiExtractionResult
from app.services.gemini_service import GeminiExtractionError, extract_certificate_data

VALID_JSON = json.dumps({
    "nome_colaborador": "João Silva",
    "cpf": "123.456.789-00",
    "nome_medico": "Dra. Ana Costa",
    "crm": "CRM-SP 12345",
    "estabelecimento_saude": "Hospital das Clínicas",
    "cid": "J01.9",
    "data_emissao": "01/01/2026",
    "inicio_afastamento": "01/01/2026",
    "fim_afastamento": "03/01/2026",
    "quantidade_dias": "3",
    "tipo_documento": "Atestado Médico",
})


def _mock_response(text):
    response = MagicMock()
    response.text = text
    return response


@patch("app.services.gemini_service.genai.Client")
@patch("app.services.gemini_service.GEMINI_API_KEY", "fake-key")
def test_extract_certificate_data_valid_json(mock_client_cls):
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = _mock_response(VALID_JSON)
    mock_client_cls.return_value = mock_client

    result = extract_certificate_data(b"fake-bytes", "image/png")

    assert isinstance(result, GeminiExtractionResult)
    assert result.nome_colaborador == "João Silva"
    assert result.quantidade_dias == "3"


@patch("app.services.gemini_service.genai.Client")
@patch("app.services.gemini_service.GEMINI_API_KEY", "fake-key")
def test_extract_certificate_data_malformed_json_falls_back_to_empty(mock_client_cls):
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = _mock_response("isso não é um json")
    mock_client_cls.return_value = mock_client

    result = extract_certificate_data(b"fake-bytes", "image/png")

    assert isinstance(result, GeminiExtractionResult)
    assert result.nome_colaborador is None


@patch("app.services.gemini_service.genai.Client")
@patch("app.services.gemini_service.GEMINI_API_KEY", "fake-key")
def test_extract_certificate_data_strips_markdown_fences(mock_client_cls):
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = _mock_response(f"```json\n{VALID_JSON}\n```")
    mock_client_cls.return_value = mock_client

    result = extract_certificate_data(b"fake-bytes", "image/png")

    assert result.cid == "J01.9"


@patch("app.services.gemini_service.genai.Client")
@patch("app.services.gemini_service.GEMINI_API_KEY", "fake-key")
def test_extract_certificate_data_null_fields(mock_client_cls):
    partial = json.dumps({"nome_colaborador": "Maria Oliveira", "cid": None, "quantidade_dias": None})
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = _mock_response(partial)
    mock_client_cls.return_value = mock_client

    result = extract_certificate_data(b"fake-bytes", "image/png")

    assert result.nome_colaborador == "Maria Oliveira"
    assert result.cid is None
    assert result.quantidade_dias is None


@patch("app.services.gemini_service.genai.Client")
@patch("app.services.gemini_service.GEMINI_API_KEY", "fake-key")
def test_extract_certificate_data_api_error_raises_gemini_extraction_error(mock_client_cls):
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = TimeoutError("timeout")
    mock_client_cls.return_value = mock_client

    with pytest.raises(GeminiExtractionError):
        extract_certificate_data(b"fake-bytes", "image/png")


def test_extract_certificate_data_without_api_key_returns_mock():
    with patch("app.services.gemini_service.GEMINI_API_KEY", None):
        result = extract_certificate_data(b"fake-bytes", "image/png")

    assert result.nome_colaborador == "João Mock"
