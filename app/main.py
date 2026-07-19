import streamlit as st

st.set_page_config(
    page_title="rosettAI",
    page_icon="🪨",
    layout="wide"
)

st.title("🪨 rosettAI")
st.markdown("""
### Sistema Inteligente de Processamento de Atestados Médicos

Bem-vindo ao **rosettAI**, sua Rosetta Stone para decifrar documentos não estruturados de RH. 🤖

---

👈 **Selecione uma opção no menu lateral:**
- **Upload de Atestado**: Envie um novo atestado (PDF ou Imagem) para processamento automático via IA.
- **Histórico**: Consulte os atestados já processados e visualize os dados extraídos.
""")

st.info("MVP para validação do fluxo de envio, extração de dados com IA e preenchimento complementar.")
