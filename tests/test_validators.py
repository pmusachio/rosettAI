import pytest
from app.utils.validators import get_missing_fields, is_complete
from app.models.schemas import GeminiExtractionResult

def test_get_missing_fields_complete():
    data = GeminiExtractionResult(
        nome_colaborador="João",
        data_emissao="01/01/2026",
        inicio_afastamento="01/01/2026",
        quantidade_dias="3"
    )
    assert get_missing_fields(data) == []
    assert is_complete(data) == True

def test_get_missing_fields_incomplete():
    data = GeminiExtractionResult(
        nome_colaborador="João",
        data_emissao=None,
        inicio_afastamento="",
        quantidade_dias="3"
    )
    missing = get_missing_fields(data)
    assert "data_emissao" in missing
    assert "inicio_afastamento" in missing
    assert len(missing) == 2
    assert is_complete(data) == False
