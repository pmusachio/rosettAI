from app.models.schemas import GeminiExtractionResult

# Campos obrigatórios para considerar o atestado completo
REQUIRED_FIELDS = [
    "nome_colaborador",
    "data_emissao",
    "inicio_afastamento",
    "quantidade_dias"
]

def get_missing_fields(extraction: GeminiExtractionResult | dict) -> list[str]:
    """Identifica quais campos obrigatórios estão faltando (None ou string vazia)."""
    missing = []
    
    # Se for dict, converte para facilitar
    if isinstance(extraction, dict):
        extraction = GeminiExtractionResult(**extraction)
        
    for field in REQUIRED_FIELDS:
        value = getattr(extraction, field, None)
        if value is None or str(value).strip() == "":
            missing.append(field)
            
    return missing

def is_complete(extraction: GeminiExtractionResult | dict) -> bool:
    """Verifica se todos os campos obrigatórios estão preenchidos."""
    return len(get_missing_fields(extraction)) == 0
