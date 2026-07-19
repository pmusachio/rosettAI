from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class GeminiExtractionResult(BaseModel):
    """Modelo do JSON esperado como resposta do Gemini."""
    nome_colaborador: Optional[str] = None
    cpf: Optional[str] = None
    nome_medico: Optional[str] = None
    crm: Optional[str] = None
    estabelecimento_saude: Optional[str] = None
    cid: Optional[str] = None
    data_emissao: Optional[str] = None
    inicio_afastamento: Optional[str] = None
    fim_afastamento: Optional[str] = None
    quantidade_dias: Optional[str] = None
    tipo_documento: Optional[str] = None

class DocumentCreate(BaseModel):
    file_name: str
    file_url: str
    
class MedicalCertificateCreate(BaseModel):
    employee_name: Optional[str] = None
    employee_cpf: Optional[str] = None
    doctor_name: Optional[str] = None
    crm: Optional[str] = None
    health_facility: Optional[str] = None
    cid: Optional[str] = None
    issue_date: Optional[date] = None
    leave_start_date: Optional[date] = None
    leave_end_date: Optional[date] = None
    leave_days: Optional[int] = None
    document_type: Optional[str] = None

class ProcessingEventCreate(BaseModel):
    event_type: str
    details: dict = Field(default_factory=dict)
