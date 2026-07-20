from typing import Optional
import uuid
from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY
from app.models.schemas import DocumentCreate, MedicalCertificateCreate, ProcessingEventCreate

# Inicializar client do Supabase
supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class DatabaseError(Exception):
    """Falha ao ler ou gravar no Supabase (rede, credenciais, RLS, etc.)."""


def _run(query):
    try:
        return query.execute()
    except Exception as exc:
        raise DatabaseError(f"Falha ao acessar o banco de dados: {exc}") from exc


def create_document(doc_data: DocumentCreate) -> dict:
    if not supabase: return {"id": str(uuid.uuid4())} # Mock for missing config

    data = {
        "file_name": doc_data.file_name,
        "file_url": doc_data.file_url,
        "processing_status": "pending"
    }
    response = _run(supabase.table("documents").insert(data))
    return response.data[0]

def update_document_status(doc_id: str, status: str, issue_date: str = None) -> dict:
    if not supabase: return {}

    update_data = {"processing_status": status}
    if issue_date:
        update_data["document_issue_date"] = issue_date

    response = _run(supabase.table("documents").update(update_data).eq("id", doc_id))
    return response.data[0] if response.data else {}

def create_medical_certificate(doc_id: str, cert_data: dict) -> dict:
    if not supabase: return {}

    data = cert_data.copy()
    data["document_id"] = doc_id

    response = _run(supabase.table("medical_certificates").insert(data))
    return response.data[0] if response.data else {}

def update_medical_certificate(cert_id: str, cert_data: dict) -> dict:
    if not supabase: return {}

    response = _run(supabase.table("medical_certificates").update(cert_data).eq("id", cert_id))
    return response.data[0] if response.data else {}

def create_processing_event(doc_id: str, event_type: str, details: dict = None) -> dict:
    if not supabase: return {}

    if details is None:
        details = {}

    data = {
        "document_id": doc_id,
        "event_type": event_type,
        "details": details
    }
    response = _run(supabase.table("processing_events").insert(data))
    return response.data[0] if response.data else {}

def list_documents():
    if not supabase: return []

    # Query with join to get employee name from certificate
    response = _run(
        supabase.table("documents")
        .select("*, medical_certificates(employee_name, leave_days, cid)")
        .order("uploaded_at", desc=True)
    )

    return response.data

def get_document_details(doc_id: str):
    if not supabase: return None

    doc_response = _run(supabase.table("documents").select("*").eq("id", doc_id))
    cert_response = _run(supabase.table("medical_certificates").select("*").eq("document_id", doc_id))
    events_response = _run(supabase.table("processing_events").select("*").eq("document_id", doc_id).order("timestamp"))

    if not doc_response.data:
        return None

    return {
        "document": doc_response.data[0],
        "certificate": cert_response.data[0] if cert_response.data else None,
        "events": events_response.data
    }
