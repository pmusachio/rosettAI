# rosettAI — Backlog Detalhado (MVP)

> Todas as tasks necessárias para entregar o MVP funcional e demonstrável para o time de RH.
> 
> **Legenda:** `[ ]` pendente · `[/]` em progresso · `[x]` concluído

---

## Epic 1 — Infraestrutura e Setup do Projeto

> Objetivo: preparar o ambiente de desenvolvimento, repositório e serviços externos.

- [x] **1.1 — Estrutura de diretórios do projeto**
  - Criar a árvore de pastas: `app/`, `app/pages/`, `app/services/`, `app/models/`, `app/utils/`, `sql/`, `tests/`, `docs/`
  - Mover o PRD para `docs/`

- [x] **1.2 — Configuração do ambiente Python**
  - Criar `requirements.txt` com dependências (mantidas nas versões estáveis mais recentes):
    - `streamlit>=1.59`
    - `google-genai>=2.12`
    - `supabase>=2.31`
    - `python-dotenv>=1.2`
    - `pydantic>=2.13`
    - `Pillow>=12.3`
    - `pytest>=9.1`
  - Criar `.env.example` com template das variáveis
  - Fixar a versão do Python em `.python-version` (3.12 — o 3.9 usado antes está EOL desde out/2025) e validar instalação
  - `requirements-dev.txt` com ferramentas de dev (`pre-commit`, `detect-secrets`)

- [x] **1.3 — Configurar projeto Supabase**
  - [x] Criar projeto no Supabase
  - [x] Criar bucket `atestados` no Supabase Storage
  - [x] Obter credenciais: `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_KEY`
  - [x] Testar conexão de verdade (upload real + insert real, validado nesta rodada — ver commits `fae7dbf` e o fix de `medical_certificates` embutido em `02_historico.py`)

- [x] **1.4 — Configurar API Gemini**
  - [x] Criar chave de API no Google AI Studio
  - [x] Testar chamada real com `google-genai` contra os dois atestados fictícios (completo e parcial) — extração correta nos dois casos
  - Nota: o modelo é configurável via `GEMINI_MODEL` (padrão: `gemini-3.5-flash`,
    ver `app/config.py`). A Google tem restringido/descontinuado modelos com
    pouco aviso para chaves novas — se der 404 `NOT_FOUND`, troque `GEMINI_MODEL`
    no `.env` (local) ou no painel do Render (produção), sem precisar mexer no código.

- [x] **1.5 — Configuração do Streamlit**
  - Criar `.streamlit/config.toml` com tema visual customizado (cores, fonte)
  - Criar `app/config.py` com carregamento de variáveis via `python-dotenv`
  - Criar `app/main.py` com layout base (sidebar, título, navegação)

- [ ] **1.6 — Configurar deploy no Render**
  - [x] Criar `Procfile`: `web: streamlit run app/main.py --server.port=$PORT --server.address=0.0.0.0`
  - [x] Criar `render.yaml` (blueprint) com o Web Service e as env vars marcadas `sync: false` (valor preenchido manualmente no painel, nunca commitado)
  - [ ] Importar o blueprint no Render apontando para o repo GitHub *(depende da conta Render do responsável pelo projeto)*
  - [ ] Preencher as variáveis de ambiente no painel do Render *(depende de credenciais reais — ver 1.3/1.4)*
  - [ ] Validar deploy com página "Hello World"
  - Nota: fica no Render nesta fase do MVP — Google Cloud/Cloud Run só entra em cena se a empresa comprar a solução.

---

## Epic 2 — Banco de Dados (Schema e CRUD)

> Objetivo: criar as tabelas, scripts SQL e camada de acesso a dados.

- [x] **2.1 — Script de criação do schema**
  - Criar `sql/create_schema.sql` com as 3 tabelas:
    - `documents` — controle de arquivos (campos: id UUID PK, file_name, file_url, uploaded_at, accepted_at, document_issue_date, processing_status, created_at, updated_at)
    - `medical_certificates` — dados extraídos (campos: id UUID PK, document_id FK, employee_name, employee_cpf, doctor_name, crm, health_facility, cid, issue_date, leave_start_date, leave_end_date, leave_days, document_type)
    - `processing_events` — auditoria (campos: id UUID PK, document_id FK, event_type, timestamp, details JSONB)
  - Incluir constraints, indexes e defaults (`gen_random_uuid()`, `NOW()`)
  - Executar no Supabase SQL Editor e validar

- [x] **2.2 — Modelos Pydantic**
  - Criar `app/models/schemas.py` com classes:
    - `DocumentCreate` / `DocumentResponse`
    - `MedicalCertificateCreate` / `MedicalCertificateResponse`
    - `ProcessingEventCreate`
    - `GeminiExtractionResult` (11 campos do JSON de retorno)
  - Adicionar validações (CPF format, CRM format, datas)

- [x] **2.3 — Serviço de banco de dados**
  - Criar `app/services/database_service.py` com funções:
    - `create_document(file_name, file_url) → DocumentResponse`
    - `update_document_status(doc_id, status)`
    - `create_medical_certificate(doc_id, data) → MedicalCertificateResponse`
    - `update_medical_certificate(cert_id, data)` — para complementação
    - `create_processing_event(doc_id, event_type, details)`
    - `get_document_with_certificate(doc_id)` — JOIN para visualização
    - `list_documents(limit, offset)` — listagem com paginação
  - Usar client Supabase Python

- [x] **2.4 — Script de dados de demonstração**
  - Criar `sql/insert_demo_data.sql` com 5 registros fictícios cobrindo:
    - Atestado completo, extraído 100% pela IA (João Silva)
    - Atestado com campo obrigatório faltante, complementado manualmente (Maria Oliveira)
    - Diferentes CIDs e quantidades de dias (Carlos Souza, Ana Pereira)
    - Fluxo 100% automático sem intervenção humana (Ana Pereira)
    - Atestado ainda pendente de complementação (Pedro Santos)
  - [ ] Validar inserção no Supabase *(depende do projeto Supabase real — ver 1.3)*

---

## Epic 3 — Upload e Armazenamento

> Objetivo: permitir que o colaborador envie um atestado e o arquivo seja armazenado.

- [x] **3.1 — Serviço de Storage**
  - Criar `app/services/storage_service.py` com funções:
    - `upload_file(file_bytes, file_name, content_type) → file_url`
    - `get_public_url(file_path) → url`
    - `delete_file(file_path)` (para casos de erro)
  - Gerar nome único para evitar colisões (UUID + extensão original)
  - Configurar políticas de acesso no bucket Supabase

- [x] **3.2 — Interface de Upload (Streamlit)**
  - Criar `app/pages/01_upload.py` com:
    - `st.file_uploader` aceitando PDF, JPG, PNG (max 10MB)
    - Preview do documento:
      - Para imagens: `st.image()`
      - Para PDF: mensagem com nome do arquivo e tamanho
    - Botão "Enviar para Processamento"
    - Barra de progresso / spinner durante upload
    - Mensagens de sucesso/erro com `st.success()` / `st.error()`
  - Ao clicar "Enviar":
    1. Upload para Supabase Storage
    2. Criar registro na tabela `documents`
    3. Registrar evento `UPLOAD_RECEIVED`
    4. Redirecionar para processamento IA

---

## Epic 4 — Integração IA (Gemini)

> Objetivo: processar o documento com IA e extrair dados estruturados.

- [x] **4.1 — Serviço Gemini**
  - Criar `app/services/gemini_service.py` com:
    - Inicialização do client `google.genai`
    - Função `extract_certificate_data(file_bytes, mime_type) → GeminiExtractionResult`
    - Enviar documento como input multimodal (imagem ou PDF)
    - Usar prompt estruturado solicitando JSON com os 11 campos

- [x] **4.2 — Engenharia de Prompt**
  - Criar prompt detalhado em português incluindo:
    - Contexto: "Você é um assistente especializado em extrair dados de atestados médicos brasileiros"
    - Instrução clara de formato JSON esperado
    - Regras para cada campo (formato de data DD/MM/YYYY, CPF com pontuação, CRM com UF)
    - Instrução para retornar `null` quando campo não encontrado
    - Exemplos de saída esperada (few-shot)
  - Armazenar prompt como constante ou arquivo de template

- [x] **4.3 — Parser e validação do retorno**
  - Implementar parsing do JSON retornado pelo Gemini
  - Tratar casos de JSON malformado (retry ou fallback)
  - Validar campos extraídos usando modelos Pydantic
  - Identificar campos que vieram como `null` (faltantes)
  - Retornar tupla: `(dados_extraidos, campos_faltantes)`

- [x] **4.4 — Fluxo de processamento completo**
  - Após upload bem-sucedido:
    1. Registrar evento `AI_STARTED`
    2. Chamar `extract_certificate_data()`
    3. Registrar evento `AI_COMPLETED`
    4. Se todos os campos preenchidos → salvar e registrar `FINALIZED`
    5. Se campos faltantes → exibir formulário de complementação
  - Tratar erros da API (timeout, rate limit, resposta inválida)
  - Exibir resultado da extração para o usuário com `st.json()` ou cards

---

## Epic 5 — Complementação Manual

> Objetivo: permitir que o usuário preencha campos que a IA não conseguiu extrair.

- [x] **5.1 — Detecção de campos faltantes**
  - Criar `app/utils/validators.py` com:
    - `get_missing_fields(extraction_result) → list[str]`
    - `is_complete(extraction_result) → bool`
    - Definir campos obrigatórios vs opcionais
    - Campos obrigatórios: `nome_colaborador`, `data_emissao`, `inicio_afastamento`, `quantidade_dias`
    - Campos desejáveis: `cpf`, `crm`, `nome_medico`, `cid`

- [x] **5.2 — Formulário de complementação**
  - Exibir na mesma página do resultado da IA:
    - Campos já extraídos: pré-preenchidos e editáveis
    - Campos faltantes: destacados em amarelo/vermelho
    - Usar `st.text_input`, `st.date_input`, `st.number_input` conforme o tipo
    - Botão "Confirmar e Salvar"
  - Ao confirmar:
    1. Merge dos dados (IA + manual)
    2. Salvar `medical_certificate` no banco
    3. Registrar evento `USER_COMPLEMENTED` (com detalhes de quais campos foram preenchidos manualmente)
    4. Registrar evento `FINALIZED`
    5. Exibir mensagem de sucesso com resumo

- [x] ~~5.3 — Cálculo de prazo de envio~~ **(fora de escopo — decisão de produto)**
  - A classificação on_time/retroactive é responsabilidade do sistema ADP, não do rosettAI.
  - `calculate_submission_status`, os badges de prazo e a coluna `submission_status` foram removidos do código e do schema.
  - O rosettAI mantém apenas a captura das datas brutas (`document_issue_date`, `issue_date`, `leave_start_date`, `leave_end_date`) via `app/utils/date_utils.py::parse_date_br`.

---

## Epic 6 — Histórico e Consultas

> Objetivo: permitir visualização dos atestados processados e queries analíticas.

- [x] **6.1 — Página de histórico**
  - Criar `app/pages/02_historico.py` com:
    - Tabela/dataframe com todos os documentos processados
    - Colunas: nome do colaborador, data emissão, dias afastamento, CID, status
    - Filtros: por status (pendente/completo), por período, por colaborador *(ainda não implementado — ver observação abaixo)*
    - Ordenação por data de upload (mais recente primeiro)
    - Clicar em uma linha → expandir detalhes completos

- [x] **6.2 — Visualização de detalhes**
  - Ao expandir um registro:
    - Exibir todos os campos do `medical_certificate`
    - Link para visualizar/baixar o documento original (URL do Storage)
    - Timeline de eventos de processamento (`processing_events`)
    - Badge visual para status

- [x] **6.3 — Queries analíticas SQL**
  - Criar `sql/analytics_queries.sql` com consultas prontas:
    - Total de atestados por período (mês/trimestre)
    - Ranking de CIDs mais frequentes
    - Média de dias de afastamento por CID
    - Colaboradores com mais atestados no período
    - Taxa de campos complementados manualmente (qualidade da IA)
    - Total de dias de absenteísmo por mês
  - Documentar cada query com comentários explicativos

---

## Epic 7 — Testes e Qualidade

> Objetivo: garantir que o sistema funciona corretamente antes da demo.

- [x] **7.1 — Testes unitários**
  - `tests/test_validators.py`:
    - Testar `get_missing_fields` com dados completos e incompletos
    - Testar `is_complete` com diferentes combinações
  - `tests/test_date_utils.py`:
    - Testar `parse_date_br` (formato BR, ISO, string vazia, inválida)
  - `tests/test_gemini_service.py`:
    - Mock da API Gemini
    - Testar parsing de JSON válido, com crases de markdown e campos nulos
    - Testar tratamento de JSON malformado (fallback)
    - Testar erro de rede/timeout da API (`GeminiExtractionError`)
    - Testar caminho sem `GEMINI_API_KEY` configurada (mock local)

- [x] **7.2 — Teste de integração end-to-end**
  - Testado o fluxo completo pela UI, contra Supabase/Gemini reais, com os
    dois atestados fictícios de `demo_assets/`:
    1. [x] Upload de arquivo → armazenamento confirmado no bucket `atestados`
    2. [x] Processamento IA → dados extraídos corretamente (caso completo: Ana Pereira, direto para sucesso)
    3. [x] Complementação → caso parcial (Fernando Rocha) caiu no formulário como esperado, campos preenchidos e salvos
    4. [x] Consulta no histórico → os dois registros apareceram corretamente
    5. [ ] Query SQL analítica → ainda não rodada manualmente no SQL Editor (baixo risco, é só conferir `sql/analytics_queries.sql`)
  - Esse teste revelou e corrigiu dois bugs reais: o modelo Gemini descontinuado
    (ver commit `30cf421`) e o parsing de `medical_certificates` em
    `02_historico.py`, que assumia lista mas o Supabase retorna objeto único
    (relação 1:1 via `UNIQUE(document_id)`).
  - Registros de teste criados durante a validação foram removidos do Supabase.

---

## Epic 8 — Polish e Preparação para Demo

> Objetivo: tornar o MVP apresentável e impressionante para o time de RH.

- [x] **8.1 — UI/UX Polish**
  - [x] Sidebar compartilhada com branding (`app/components.py::render_sidebar`)
  - [x] `st.set_page_config(page_title=..., layout="wide")` em todas as páginas (sem emoji)
  - [x] Mensagens de erro claras via `st.error` nas falhas de IA/Storage/banco (em vez de crash)
  - [x] Tooltips (`help=`) nos campos do formulário de complementação
  - [ ] Tema visual customizado além do `.streamlit/config.toml` atual — não priorizado neste MVP

- [x] **8.2 — Dados de demonstração realistas**
  - [x] Script `scripts/generate_demo_assets.py` gera 2 atestados fictícios (`demo_assets/`): um legível/completo, um parcialmente ilegível com dados faltantes
  - [x] `sql/insert_demo_data.sql` com 5 registros cobrindo os cenários do MVP
  - [ ] Popular o Supabase real com esses dados *(depende do projeto Supabase — ver 1.3)*

- [ ] **8.3 — Deploy final no Render**
  - [x] `render.yaml` (blueprint) pronto para importar no Render
  - [ ] Verificar que todas as variáveis de ambiente estão configuradas *(depende da conta Render)*
  - [ ] Fazer deploy da branch `main`
  - [ ] Testar URL pública com fluxo completo
  - [ ] Verificar performance (tempo de resposta da IA < 30s)
  - [ ] Preparar URL para compartilhar com o time de RH

- [x] **8.4 — Documentação final**
  - [x] Criar `docs/demo_guide.md` com roteiro da demonstração
  - [x] Garantir que o PRD está atualizado (decisão ADP, Render mantido)
  - [ ] Atualizar README com URL de produção *(depende do deploy em 8.3)*

---

## Ordem de Execução Sugerida

```
Epic 1 (Infraestrutura)
    ↓
Epic 2 (Banco de Dados)
    ↓
Epic 3 (Upload) ←→ Epic 4 (IA) — podem ser paralelos
    ↓
Epic 5 (Complementação)
    ↓
Epic 6 (Histórico)
    ↓
Epic 7 (Testes)
    ↓
Epic 8 (Polish + Demo)
```

---

## Critérios de Aceitação do MVP

O MVP está pronto para demonstração quando **todos** os itens abaixo forem verdadeiros:

- [x] Colaborador consegue enviar um atestado (PDF, JPG ou PNG)
- [x] Documento é armazenado no Supabase Storage
- [x] IA extrai informações do documento automaticamente
- [x] Sistema detecta e destaca campos faltantes
- [x] Colaborador consegue complementar dados manualmente
- [x] Dados são persistidos no PostgreSQL
- [x] Timestamps e eventos de auditoria são registrados
- [x] Histórico de atestados é consultável na interface
- [ ] Queries SQL analíticas retornam dados corretos *(scripts prontos em `sql/analytics_queries.sql`, falta rodar manualmente no SQL Editor)*
- [ ] Aplicação está acessível via URL pública (Render) *(depende do deploy — ver seção 3 do [TUTORIAL_PROXIMOS_PASSOS.md](docs/TUTORIAL_PROXIMOS_PASSOS.md))*
