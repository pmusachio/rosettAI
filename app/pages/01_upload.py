import streamlit as st
import io
from app.services.storage_service import upload_file
from app.services.gemini_service import extract_certificate_data
from app.services.database_service import (
    create_document, update_document_status, 
    create_medical_certificate, update_medical_certificate,
    create_processing_event
)
from app.models.schemas import DocumentCreate
from app.utils.validators import get_missing_fields, is_complete
from app.utils.date_utils import calculate_submission_status, parse_date_br

st.set_page_config(page_title="Upload de Atestado | rosettAI", page_icon="🪨", layout="wide")
st.title("📤 Upload de Atestado")

# Session state to handle multi-step form
if 'step' not in st.session_state:
    st.session_state.step = 'upload'
if 'doc_id' not in st.session_state:
    st.session_state.doc_id = None
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = None
if 'missing_fields' not in st.session_state:
    st.session_state.missing_fields = []
if 'cert_id' not in st.session_state:
    st.session_state.cert_id = None


if st.session_state.step == 'upload':
    st.markdown("Faça o upload do seu atestado médico (PDF, JPG, PNG). O tamanho máximo é 10MB.")
    
    uploaded_file = st.file_uploader("Escolha o arquivo", type=['pdf', 'jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        if uploaded_file.type.startswith('image/'):
            st.image(uploaded_file, caption="Preview", width=400)
        else:
            st.info(f"Arquivo PDF selecionado: {uploaded_file.name}")
            
        if st.button("Enviar para Processamento", type="primary"):
            with st.spinner("Processando..."):
                # 1. Upload to Storage
                file_bytes = uploaded_file.getvalue()
                mime_type = uploaded_file.type
                file_name = uploaded_file.name
                
                file_url = upload_file(file_bytes, file_name)
                
                # 2. Register Document
                doc = create_document(DocumentCreate(file_name=file_name, file_url=file_url))
                doc_id = doc.get("id")
                st.session_state.doc_id = doc_id
                
                if doc_id:
                    create_processing_event(doc_id, "UPLOAD_RECEIVED", {"source": "web_ui", "file_name": file_name})
                    create_processing_event(doc_id, "AI_STARTED")
                
                # 3. Call Gemini API
                extracted = extract_certificate_data(file_bytes, mime_type)
                st.session_state.extracted_data = extracted
                
                if doc_id:
                    create_processing_event(doc_id, "AI_COMPLETED", {"extracted_keys": list(extracted.model_dump(exclude_none=True).keys())})
                
                # 4. Check missing fields
                missing = get_missing_fields(extracted)
                st.session_state.missing_fields = missing
                
                # Save initial certificate state
                cert_data = extracted.model_dump()
                # Try to parse issue date for submission status
                issue_date_obj = parse_date_br(extracted.data_emissao)
                if issue_date_obj:
                    sub_status = calculate_submission_status(issue_date_obj)
                    update_document_status(doc_id, "processing", sub_status, issue_date_obj.isoformat())
                else:
                    update_document_status(doc_id, "processing")
                    
                # Format cert_data dates for DB
                formatted_cert_data = {
                    "employee_name": cert_data.get("nome_colaborador"),
                    "employee_cpf": cert_data.get("cpf"),
                    "doctor_name": cert_data.get("nome_medico"),
                    "crm": cert_data.get("crm"),
                    "health_facility": cert_data.get("estabelecimento_saude"),
                    "cid": cert_data.get("cid"),
                    "document_type": cert_data.get("tipo_documento"),
                    "leave_days": int(cert_data.get("quantidade_dias")) if cert_data.get("quantidade_dias") and cert_data.get("quantidade_dias").isdigit() else None
                }
                
                if issue_date_obj:
                    formatted_cert_data["issue_date"] = issue_date_obj.isoformat()
                
                start_d = parse_date_br(cert_data.get("inicio_afastamento"))
                if start_d: formatted_cert_data["leave_start_date"] = start_d.isoformat()
                
                end_d = parse_date_br(cert_data.get("fim_afastamento"))
                if end_d: formatted_cert_data["leave_end_date"] = end_d.isoformat()
                    
                cert = create_medical_certificate(doc_id, formatted_cert_data)
                st.session_state.cert_id = cert.get("id")
                
                if len(missing) == 0:
                    update_document_status(doc_id, "completed")
                    create_processing_event(doc_id, "FINALIZED")
                    st.session_state.step = 'success'
                else:
                    st.session_state.step = 'complement'
                
                st.rerun()

elif st.session_state.step == 'complement':
    st.warning("⚠️ Alguns campos obrigatórios não puderam ser extraídos automaticamente. Por favor, preencha-os.")
    
    extracted = st.session_state.extracted_data
    missing = st.session_state.missing_fields
    
    with st.form("complement_form"):
        st.subheader("Dados do Atestado")
        
        # Helper function to style missing fields
        def get_val(field_name):
            return getattr(extracted, field_name, "") or ""
            
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do Colaborador *", value=get_val("nome_colaborador"))
            cpf = st.text_input("CPF", value=get_val("cpf"))
            dt_emissao = st.text_input("Data de Emissão (DD/MM/YYYY) *", value=get_val("data_emissao"))
            cid = st.text_input("CID", value=get_val("cid"))
            
        with col2:
            medico = st.text_input("Nome do Médico", value=get_val("nome_medico"))
            crm = st.text_input("CRM", value=get_val("crm"))
            dt_inicio = st.text_input("Início do Afastamento (DD/MM/YYYY) *", value=get_val("inicio_afastamento"))
            dias = st.text_input("Quantidade de Dias *", value=get_val("quantidade_dias"))
            
        st.info("Campos com * são obrigatórios.")
        submitted = st.form_submit_button("Confirmar e Salvar", type="primary")
        
        if submitted:
            if not (nome and dt_emissao and dt_inicio and dias):
                st.error("Preencha todos os campos obrigatórios (*).")
            else:
                # Update logic
                update_data = {
                    "employee_name": nome,
                    "employee_cpf": cpf,
                    "doctor_name": medico,
                    "crm": crm,
                    "cid": cid,
                }
                
                if dias.isdigit():
                    update_data["leave_days"] = int(dias)
                
                i_date = parse_date_br(dt_emissao)
                if i_date: update_data["issue_date"] = i_date.isoformat()
                
                s_date = parse_date_br(dt_inicio)
                if s_date: update_data["leave_start_date"] = s_date.isoformat()
                
                update_medical_certificate(st.session_state.cert_id, update_data)
                
                doc_id = st.session_state.doc_id
                
                # Recalculate submission status if issue date changed manually
                if i_date:
                    sub_status = calculate_submission_status(i_date)
                    update_document_status(doc_id, "completed", sub_status, i_date.isoformat())
                else:
                    update_document_status(doc_id, "completed")
                    
                create_processing_event(doc_id, "USER_COMPLEMENTED", {"fields": ["manual_review"]})
                create_processing_event(doc_id, "FINALIZED")
                
                st.session_state.step = 'success'
                st.rerun()

elif st.session_state.step == 'success':
    st.success("✅ Atestado processado e salvo com sucesso!")
    st.balloons()
    
    if st.button("Enviar Novo Atestado"):
        st.session_state.step = 'upload'
        for key in ['doc_id', 'extracted_data', 'missing_fields', 'cert_id']:
            st.session_state[key] = None
        st.rerun()
