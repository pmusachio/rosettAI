import json
from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.models.schemas import GeminiExtractionResult


class GeminiExtractionError(Exception):
    """Falha ao chamar a API do Gemini (timeout, rate limit, rede, resposta inválida)."""


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
    Analise o documento anexo e extraia as informações pedidas.

    Regras:
    1. Se um campo não for encontrado, o valor deve ser null.
    2. Datas devem vir no formato DD/MM/YYYY.
    3. CPF deve ter a pontuação (XXX.XXX.XXX-XX).
    4. CRM deve ter uf, ex: CRM-SP 12345.
    """

    # Prepara o documento para envio
    document = types.Part.from_bytes(
        data=file_bytes,
        mime_type=mime_type
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt, document],
            config=types.GenerateContentConfig(
                temperature=0.0, # Respostas determinísticas
                response_mime_type="application/json",
                # response_schema explícito: sem ele, alguns modelos param de
                # gerar o JSON antes de fechar a última chave (finish_reason
                # STOP, sem MAX_TOKENS) mesmo com response_mime_type=json.
                response_schema=GeminiExtractionResult,
                max_output_tokens=1024,
                # "thinking" não ajuda numa extração estruturada simples e só
                # consome tokens/latência à toa.
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            )
        )
    except Exception as exc:
        raise GeminiExtractionError(f"Falha ao chamar a API do Gemini: {exc}") from exc

    # O SDK já entrega a resposta parseada no schema quando dá certo.
    if response.parsed is not None:
        return response.parsed

    # Fallback: parse manual caso o parsing automático do SDK falhe.
    try:
        data = json.loads(response.text)
        return GeminiExtractionResult(**data)
    except (json.JSONDecodeError, TypeError):
        print(f"Erro ao parsear JSON: {response.text!r}")
        # Retorna objeto vazio se falhar completamente
        return GeminiExtractionResult()
