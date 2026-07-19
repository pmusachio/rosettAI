import json
import re
from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY
from app.models.schemas import GeminiExtractionResult

def extract_certificate_data(file_bytes: bytes, mime_type: str) -> GeminiExtractionResult:
    """
    Sents the document to Gemini and extracts the data as a structured JSON.
    """
    if not GEMINI_API_KEY:
        # Mock para ambiente sem chave (só para UI test)
        return GeminiExtractionResult(
            nome_colaborador="João Mock",
            quantidade_dias="3",
            data_emissao="01/01/2026"
        )
        
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = """
    Você é um assistente especializado em extrair dados de atestados médicos brasileiros.
    Analise o documento anexo e extraia as informações no formato JSON rigoroso abaixo.
    
    Regras:
    1. Responda APENAS com um JSON válido, sem markdown (` ```json `), sem texto antes ou depois.
    2. Se um campo não for encontrado, o valor deve ser null.
    3. Datas devem vir no formato DD/MM/YYYY.
    4. CPF deve ter a pontuação (XXX.XXX.XXX-XX).
    5. CRM deve ter uf, ex: CRM-SP 12345.
    
    Formato esperado:
    {
        "nome_colaborador": "string ou null",
        "cpf": "string ou null",
        "nome_medico": "string ou null",
        "crm": "string ou null",
        "estabelecimento_saude": "string ou null",
        "cid": "string ou null",
        "data_emissao": "string DD/MM/YYYY ou null",
        "inicio_afastamento": "string DD/MM/YYYY ou null",
        "fim_afastamento": "string DD/MM/YYYY ou null",
        "quantidade_dias": "string ou null",
        "tipo_documento": "string ou null"
    }
    """
    
    # Prepara o documento para envio
    document = types.Part.from_bytes(
        data=file_bytes,
        mime_type=mime_type
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[prompt, document],
        config=types.GenerateContentConfig(
            temperature=0.0, # Respostas determinísticas
            response_mime_type="application/json"
        )
    )
    
    text = response.text
    
    # Limpa markdown se o modelo ainda retornar com crases
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
        
    try:
        data = json.loads(text)
        return GeminiExtractionResult(**data)
    except json.JSONDecodeError:
        print(f"Erro ao parsear JSON: {text}")
        # Retorna objeto vazio se falhar completamente
        return GeminiExtractionResult()
