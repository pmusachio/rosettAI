# 📋 rosettAI — Backlog Detalhado (MVP)

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
  - Criar `requirements.txt` com dependências iniciais:
    - `streamlit>=1.45`
    - `google-genai>=1.14`
    - `supabase>=2.15`
    - `python-dotenv>=1.1`
    - `pydantic>=2.11`
    - `Pillow>=11.2`
    - `pytest>=8.3`
  - Criar `.env.example` com template das variáveis
  - Configurar `.venv` local e validar instalação

- [ ] **1.3 — Configurar projeto Supabase**
  - Criar projeto no Supabase
  - Criar bucket `atestados` no Supabase Storage (público ou com policy)
  - Obter credenciais: `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_KEY`
  - Testar conexão via script Python simples

- [ ] **1.4 — Configurar API Gemini**
  - Criar chave de API no Google AI Studio
  - Testar chamada básica com `google-genai`
  - Validar que o modelo `gemini-2.0-flash` aceita inputs multimodais (imagem + texto)

- [x] **1.5 — Configuração do Streamlit**
  - Criar `.streamlit/config.toml` com tema visual customizado (cores, fonte)
  - Criar `app/config.py` com carregamento de variáveis via `python-dotenv`
  - Criar `app/main.py` com layout base (sidebar, título, navegação)

- [ ] **1.6 — Configurar deploy no Render**
  - Criar `Procfile`: `web: streamlit run app/main.py --server.port=$PORT --server.address=0.0.0.0`
  - Configurar Web Service no Render apontando para o repo GitHub
  - Adicionar variáveis de ambiente no painel do Render
  - Validar deploy com página "Hello World"

---

## Epic 2 — Banco de Dados (Schema e CRUD)

> Objetivo: criar as tabelas, scripts SQL e camada de acesso a dados.

- [x] **2.1 — Script de criação do schema**
  - Criar `sql/create_schema.sql` com as 3 tabelas:
    - `documents` — controle de arquivos (campos: id UUID PK, file_name, file_url, uploaded_at, accepted_at, document_issue_date, processing_status, submission_status, created_at, updated_at)
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
  - Criar `sql/insert_demo_data.sql` com pelo menos 5 registros fictícios cobrindo:
    - Atestado completo (todos os campos)
    - Atestado com campos faltantes
    - Envio dentro do prazo
    - Envio retroativo
    - Diferentes CIDs e quantidades de dias
  - Validar inserção no Supabase

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

- [x] **5.3 — Cálculo de prazo de envio**
  - Criar `app/utils/date_utils.py` com:
    - `calculate_submission_status(issue_date, upload_date) → "on_time" | "retroactive"`
    - Regra: até 3 dias corridos após emissão = `on_time`
    - Acima de 3 dias = `retroactive`
  - Exibir badge visual no resultado:
    - 🟢 "Envio dentro do prazo" 
    - 🟡 "Envio retroativo — ajuste de absenteísmo necessário"
  - Salvar `submission_status` na tabela `documents`

---

## Epic 6 — Histórico e Consultas

> Objetivo: permitir visualização dos atestados processados e queries analíticas.

- [x] **6.1 — Página de histórico**
  - Criar `app/pages/02_historico.py` com:
    - Tabela/dataframe com todos os documentos processados
    - Colunas: nome do colaborador, data emissão, dias afastamento, CID, status, prazo
    - Filtros: por status (pendente/completo), por período, por colaborador
    - Ordenação por data de upload (mais recente primeiro)
    - Clicar em uma linha → expandir detalhes completos

- [x] **6.2 — Visualização de detalhes**
  - Ao expandir um registro:
    - Exibir todos os campos do `medical_certificate`
    - Link para visualizar/baixar o documento original (URL do Storage)
    - Timeline de eventos de processamento (`processing_events`)
    - Badges visuais para status e prazo

- [x] **6.3 — Queries analíticas SQL**
  - Criar `sql/analytics_queries.sql` com consultas prontas:
    - Total de atestados por período (mês/trimestre)
    - Ranking de CIDs mais frequentes
    - Média de dias de afastamento por CID
    - Proporção envios no prazo vs retroativos
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
    - Testar cálculo dentro do prazo (0, 1, 2, 3 dias)
    - Testar cálculo retroativo (4+ dias)
    - Testar edge cases (mesma data, datas inválidas)
  - `tests/test_gemini_service.py`:
    - Mock da API Gemini
    - Testar parsing de JSON válido
    - Testar tratamento de JSON malformado
    - Testar campos nulos

- [ ] **7.2 — Teste de integração end-to-end**
  - Testar fluxo completo com um atestado de teste:
    1. Upload de arquivo → armazenamento confirmado
    2. Processamento IA → dados extraídos corretamente
    3. Complementação (se necessário) → dados salvos
    4. Consulta no histórico → registro visível
    5. Query SQL → dados retornam corretamente
  - Documentar resultado em `docs/test_results.md`

---

## Epic 8 — Polish e Preparação para Demo

> Objetivo: tornar o MVP apresentável e impressionante para o time de RH.

- [ ] **8.1 — UI/UX Polish**
  - Adicionar logo/ícone do rosettAI na sidebar
  - Configurar tema visual consistente (cores, fontes)
  - Adicionar `st.set_page_config(page_title="rosettAI", page_icon="🪨", layout="wide")`
  - Melhorar mensagens de feedback (sucesso, erro, loading)
  - Adicionar tooltips e instruções nos campos do formulário
  - Garantir responsividade em diferentes tamanhos de tela

- [ ] **8.2 — Dados de demonstração realistas**
  - Criar 3-5 atestados médicos fictícios (imagens/PDFs) para demo
  - Garantir variedade: atestado legível, parcialmente legível, com dados faltantes
  - Não usar dados reais — criar documentos ficcionais mas visualmente realistas
  - Popular banco com dados de demo via `insert_demo_data.sql`

- [ ] **8.3 — Deploy final no Render**
  - Verificar que todas as variáveis de ambiente estão configuradas
  - Fazer deploy da branch `main`
  - Testar URL pública com fluxo completo
  - Verificar performance (tempo de resposta da IA < 30s)
  - Preparar URL para compartilhar com o time de RH

- [ ] **8.4 — Documentação final**
  - Atualizar README com URL de produção
  - Criar `docs/demo_guide.md` com roteiro da demonstração:
    - Passo a passo da demo
    - Talking points para o time de RH
    - Perguntas esperadas e respostas
    - Métricas de sucesso do MVP
  - Garantir que o PRD está atualizado

---

## 📅 Ordem de Execução Sugerida

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

## 🎯 Critérios de Aceitação do MVP

O MVP está pronto para demonstração quando **todos** os itens abaixo forem verdadeiros:

- [ ] Colaborador consegue enviar um atestado (PDF, JPG ou PNG)
- [ ] Documento é armazenado no Supabase Storage
- [ ] IA extrai informações do documento automaticamente
- [ ] Sistema detecta e destaca campos faltantes
- [ ] Colaborador consegue complementar dados manualmente
- [ ] Dados são persistidos no PostgreSQL
- [ ] Timestamps e eventos de auditoria são registrados
- [ ] Cálculo de prazo (normal vs retroativo) funciona
- [ ] Histórico de atestados é consultável na interface
- [ ] Queries SQL analíticas retornam dados corretos
- [ ] Aplicação está acessível via URL pública (Render)
