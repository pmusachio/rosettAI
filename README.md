# 🪨 rosettAI

> **Por que "rosettAI"?** — Assim como a [Pedra de Rosetta](https://pt.wikipedia.org/wiki/Pedra_de_Roseta) permitiu decifrar hieróglifos ao traduzir uma mesma mensagem entre línguas diferentes, o **rosettAI** decifra atestados médicos — documentos não estruturados, escritos em formatos variados e muitas vezes ilegíveis — e os traduz para dados estruturados que o RH consegue entender e analisar. É a sua **Rosetta Stone** turbinada por **IA**. 🤖

---

## 📋 Sobre o Projeto

Sistema inteligente de processamento de atestados médicos que utiliza **IA generativa (Gemini)** para extrair automaticamente informações de documentos médicos, estruturá-las e armazená-las em banco de dados, eliminando digitação manual e reduzindo erros.

### O Problema

| Desafio atual | Solução rosettAI |
|---|---|
| Documentos em formatos variados (PDF, foto, scan) | Upload unificado com suporte a PDF, JPG e PNG |
| Digitação manual propensa a erros | Extração automática via IA multimodal |
| Baixa rastreabilidade | Auditoria completa com timestamps e eventos |
| Dificuldade para gerar indicadores | Dados estruturados prontos para analytics |

---

## 🏗️ Arquitetura

```
Colaborador → Streamlit UI → Upload arquivo
                                  ↓
                          Supabase Storage
                                  ↓
                           Gemini API (IA)
                                  ↓
                         JSON Estruturado
                          ↙            ↘
                Dados completos    Dados faltantes
                      ↓                  ↓
                      ↓          Formulário complementar
                      ↓                  ↓
                      ↘                ↙
                  PostgreSQL (Supabase)
                          ↓
                  SQL / Dashboards
```

---

## 🛠️ Tech Stack

| Componente | Tecnologia |
|---|---|
| Interface | Streamlit |
| Hospedagem | Render |
| IA | Google Gemini API (multimodal) |
| Banco de Dados | Supabase (PostgreSQL) |
| Storage | Supabase Storage |
| Linguagem | Python 3.11+ |
| Controle de versão | GitHub |

---

## 📁 Estrutura do Projeto

```
rosettAI/
├── app/
│   ├── main.py                  # Ponto de entrada Streamlit
│   ├── config.py                # Configurações e variáveis de ambiente
│   ├── pages/
│   │   ├── 01_upload.py         # Página de upload de atestados
│   │   └── 02_historico.py      # Página de histórico/consulta
│   ├── services/
│   │   ├── gemini_service.py    # Integração com Gemini API
│   │   ├── storage_service.py   # Upload/download Supabase Storage
│   │   └── database_service.py  # CRUD PostgreSQL
│   ├── models/
│   │   └── schemas.py           # Modelos de dados (Pydantic)
│   └── utils/
│       ├── validators.py        # Validações de campos
│       └── date_utils.py        # Cálculos de prazo
├── sql/
│   ├── create_schema.sql        # DDL das tabelas
│   ├── insert_demo_data.sql     # Dados de teste
│   └── analytics_queries.sql    # Queries analíticas
├── tests/
│   ├── test_gemini_service.py
│   ├── test_validators.py
│   └── test_date_utils.py
├── docs/
│   └── PRD_Sistema_Inteligente_Atestados_MVP.md
├── .env.example                 # Template de variáveis de ambiente
├── .gitignore
├── .streamlit/
│   └── config.toml              # Configuração visual Streamlit
├── requirements.txt
├── Procfile                     # Deploy Render
├── LICENSE
└── README.md
```

---

## 🚀 Setup Local

### Pré-requisitos

- Python 3.11+
- Conta no [Supabase](https://supabase.com) (projeto criado)
- Chave de API do [Google Gemini](https://ai.google.dev)

### Instalação

```bash
# Clone o repositório
git clone git@github.com:pmusachio/rosettAI.git
cd rosettAI

# Crie o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais
```

### Variáveis de Ambiente

```env
GEMINI_API_KEY=sua_chave_gemini
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_anon
SUPABASE_SERVICE_KEY=sua_chave_service
```

### Executando

```bash
streamlit run app/main.py
```

---

## 📊 Modelo de Dados

### `documents` — Controle de arquivos

| Campo | Tipo | Descrição |
|---|---|---|
| id | UUID | Chave primária |
| file_name | VARCHAR | Nome original do arquivo |
| file_url | TEXT | URL no Supabase Storage |
| uploaded_at | TIMESTAMP | Data/hora do upload |
| accepted_at | TIMESTAMP | Data/hora de aceite |
| document_issue_date | DATE | Data de emissão do atestado |
| processing_status | VARCHAR | pending / processing / completed / error |
| submission_status | VARCHAR | on_time / retroactive |
| created_at | TIMESTAMP | Criação do registro |
| updated_at | TIMESTAMP | Última atualização |

### `medical_certificates` — Dados extraídos

| Campo | Tipo | Descrição |
|---|---|---|
| id | UUID | Chave primária |
| document_id | UUID | FK → documents |
| employee_name | VARCHAR | Nome do colaborador |
| employee_cpf | VARCHAR | CPF |
| doctor_name | VARCHAR | Nome do médico |
| crm | VARCHAR | CRM do médico |
| health_facility | VARCHAR | Estabelecimento de saúde |
| cid | VARCHAR | Código CID |
| issue_date | DATE | Data de emissão |
| leave_start_date | DATE | Início do afastamento |
| leave_end_date | DATE | Fim do afastamento |
| leave_days | INTEGER | Dias de afastamento |
| document_type | VARCHAR | Tipo do documento |

### `processing_events` — Auditoria

| Campo | Tipo | Descrição |
|---|---|---|
| id | UUID | Chave primária |
| document_id | UUID | FK → documents |
| event_type | VARCHAR | Tipo do evento |
| timestamp | TIMESTAMP | Data/hora |
| details | JSONB | Detalhes adicionais |

**Eventos rastreados:** `UPLOAD_RECEIVED` → `AI_STARTED` → `AI_COMPLETED` → `USER_COMPLEMENTED` → `FINALIZED`

---

## 📌 Status do Projeto

🟡 **Em desenvolvimento** — MVP

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT — veja o arquivo [LICENSE](LICENSE) para detalhes.