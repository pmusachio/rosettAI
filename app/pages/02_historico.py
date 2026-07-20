import streamlit as st
import pandas as pd
from app.components import render_sidebar
from app.services.database_service import list_documents, get_document_details, DatabaseError

st.set_page_config(page_title="Histórico | rosettAI", page_icon="🪨", layout="wide")
render_sidebar()
st.title("🗂️ Histórico de Atestados")

try:
    documents = list_documents()
except DatabaseError as exc:
    st.error(f"⚠️ Não foi possível carregar o histórico: {exc}")
    st.stop()

if not documents:
    st.info("Nenhum atestado encontrado na base de dados.")
else:
    # Prepare data for table
    table_data = []
    for doc in documents:
        cert = doc.get("medical_certificates", {})
        if isinstance(cert, list) and len(cert) > 0:
            cert = cert[0]
            
        status_emoji = "✅" if doc.get("processing_status") == "completed" else ("⏳" if doc.get("processing_status") == "pending" else "⚠️")

        table_data.append({
            "ID": doc.get("id")[:8],
            "Data Upload": doc.get("uploaded_at")[:10] if doc.get("uploaded_at") else "",
            "Colaborador": cert.get("employee_name", "N/A"),
            "CID": cert.get("cid", "N/A"),
            "Dias": cert.get("leave_days", "N/A"),
            "Status": f"{status_emoji} {doc.get('processing_status')}",
            "_id": doc.get("id") # Hidden column for fetching details
        })
        
    df = pd.DataFrame(table_data)
    
    # Display dataframe (without the full ID column)
    st.dataframe(
        df.drop(columns=["_id"]),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    st.subheader("Ver Detalhes")
    
    selected_id_short = st.selectbox("Selecione o ID do atestado para ver detalhes:", df["ID"].tolist())
    
    if selected_id_short:
        full_id = df[df["ID"] == selected_id_short]["_id"].values[0]
        try:
            details = get_document_details(full_id)
        except DatabaseError as exc:
            st.error(f"⚠️ Não foi possível carregar os detalhes: {exc}")
            details = None

        if details:
            doc = details["document"]
            cert = details["certificate"]
            events = details["events"]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📄 Dados do Atestado")
                if cert:
                    st.write(f"**Colaborador:** {cert.get('employee_name')}")
                    st.write(f"**CPF:** {cert.get('employee_cpf')}")
                    st.write(f"**Médico:** {cert.get('doctor_name')} ({cert.get('crm')})")
                    st.write(f"**Local:** {cert.get('health_facility')}")
                    st.write(f"**CID:** {cert.get('cid')}")
                    st.write(f"**Emissão:** {cert.get('issue_date')}")
                    st.write(f"**Afastamento:** {cert.get('leave_start_date')} até {cert.get('leave_end_date')} ({cert.get('leave_days')} dias)")
                
                st.markdown("### 🔗 Arquivo")
                st.markdown(f"[Visualizar Original]({doc.get('file_url')})")
                
            with col2:
                st.markdown("### ⏱️ Timeline de Processamento")
                for event in events:
                    st.text(f"[{event.get('timestamp')[:19]}] {event.get('event_type')}")
                    if event.get("details"):
                        st.caption(str(event.get("details")))
