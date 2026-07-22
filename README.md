# rosettAI

> **Por que "rosettAI"?** — Assim como a [Pedra de Rosetta](https://pt.wikipedia.org/wiki/Pedra_de_Roseta) permitiu decifrar hieróglifos ao traduzir uma mesma mensagem entre línguas diferentes, o **rosettAI** decifra atestados médicos — documentos não estruturados, escritos em formatos variados e muitas vezes ilegíveis — e os traduz para dados estruturados que o RH consegue entender e analisar.

---

## Acesso

**[rosettai.onrender.com](https://rosettai.onrender.com)**

A aplicação está publicada e disponível para uso — não é necessário instalar nada localmente.

---

## Sobre o Projeto

Sistema inteligente de processamento de atestados médicos que utiliza **IA generativa (Gemini)** para extrair automaticamente informações de documentos médicos, estruturá-las e armazená-las em banco de dados, eliminando digitação manual e reduzindo erros de transcrição.

### O Problema

| Desafio atual | Solução rosettAI |
|---|---|
| Documentos em formatos variados (PDF, foto, scan) | Upload unificado com suporte a PDF, JPG e PNG |
| Digitação manual propensa a erros | Extração automática via IA multimodal |
| Baixa rastreabilidade | Auditoria completa com timestamps e eventos |
| Dificuldade para gerar indicadores | Dados estruturados prontos para analytics |

---

## Capturas de Tela

| Upload — antes do envio | Upload — complementação manual |
|---|---|
| ![Tela de upload, arquivo selecionado](docs/screenshots/upload_preview.png) | ![Formulário de complementação com campo faltante](docs/screenshots/upload_complement.png) |

| Página inicial | Histórico com detalhes do atestado |
|---|---|
| ![Página inicial do rosettAI](docs/screenshots/home.png) | ![Histórico de atestados com detalhes expandidos](docs/screenshots/historico_detail.png) |

> Capturas com dados fictícios — nenhum atestado real foi utilizado.

---

## Arquitetura

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

## Tech Stack

| Componente | Tecnologia |
|---|---|
| Interface | Streamlit |
| Hospedagem | Render |
| IA | Google Gemini API (multimodal) |
| Banco de Dados | Supabase (PostgreSQL) |
| Storage | Supabase Storage |
| Linguagem | Python 3.12+ |
| Controle de versão | GitHub |

---

## Estrutura do Projeto

```
rosettAI/
├── app/
│   ├── main.py                  # Ponto de entrada Streamlit
│   ├── config.py                # Configurações e variáveis de ambiente
│   ├── components.py            # Branding compartilhado (sidebar)
│   ├── pages/
│   │   ├── 01_upload.py         # Página de upload de atestados
│   │   └── 02_historico.py      # Página de histórico/consulta
│   ├── services/
│   │   ├── gemini_service.py    # Integração com Gemini API
│   │   ├── storage_service.py   # Upload/download Supabase Storage
│   │   ├── database_service.py  # CRUD PostgreSQL
│   │   └── supabase_client.py   # Client Supabase compartilhado
│   ├── models/
│   │   └── schemas.py           # Modelos de dados (Pydantic)
│   └── utils/
│       ├── validators.py        # Validações de campos obrigatórios
│       └── date_utils.py        # Parsing de datas (DD/MM/YYYY)
├── sql/
│   ├── create_schema.sql        # DDL das tabelas
│   ├── insert_demo_data.sql     # Dados de teste
│   └── analytics_queries.sql    # Queries analíticas
├── tests/
│   ├── test_gemini_service.py
│   ├── test_validators.py
│   └── test_date_utils.py
├── docs/
│   └── screenshots/              # Capturas de tela usadas neste README
├── .streamlit/config.toml        # Configuração visual Streamlit
├── requirements.txt
├── Procfile                      # Deploy Render
├── render.yaml                   # Blueprint do Render
└── LICENSE
```

---

## Modelo de Dados

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

**Eventos rastreados:** `UPLOAD_RECEIVED` → `AI_STARTED` → `AI_COMPLETED` → (`USER_COMPLEMENTED`) → `FINALIZED`, ou `ERROR` em caso de falha na IA/Storage/banco.
