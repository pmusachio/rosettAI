import sys
from pathlib import Path

# `streamlit run app/main.py` não coloca a raiz do projeto no sys.path,
# o que quebraria todo import `from app.X import Y` nas páginas. Este é o
# script de entrada, então basta corrigir aqui uma vez por processo.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from app.components import render_sidebar

st.set_page_config(
    page_title="rosettAI",
    layout="wide"
)
render_sidebar()

st.title("rosettAI")
st.markdown("""
### Sistema Inteligente de Processamento de Atestados Médicos

Bem-vindo ao **rosettAI**, sua Rosetta Stone para decifrar documentos não estruturados de RH.

---

**Selecione uma opção no menu lateral:**
- **Upload de Atestado**: Envie um novo atestado (PDF ou Imagem) para processamento automático via IA.
- **Histórico**: Consulte os atestados já processados e visualize os dados extraídos.
""")

st.info("MVP para validação do fluxo de envio, extração de dados com IA e preenchimento complementar.")
