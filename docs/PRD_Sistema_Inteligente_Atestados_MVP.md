# PRD - Sistema Inteligente de Processamento de Atestados Médicos (MVP)

## Status

-   Versão: 1.0
-   Documento: Product Requirements Document (PRD)
-   Objetivo: alinhamento entre Produto, Tecnologia, Dados e RH
-   Tipo: MVP / Proof of Concept

------------------------------------------------------------------------

# 1. Visão Geral

O projeto tem como objetivo criar uma aplicação capaz de receber
atestados médicos enviados por colaboradores, interpretar
automaticamente os documentos utilizando Inteligência Artificial,
estruturar as informações extraídas e armazená-las em uma base de dados
preparada para análises futuras.

A primeira versão não contempla integração com o Sistema Atesta CFM
devido à necessidade de acesso corporativo, CNPJ e dados reais
cadastrados. Essa etapa será considerada em uma evolução futura.

------------------------------------------------------------------------

# 2. Problema

O processo atual possui desafios:

-   documentos chegam em formatos diferentes;
-   informações precisam ser digitadas manualmente;
-   existe risco de erros de transcrição;
-   baixa rastreabilidade;
-   dificuldade para gerar indicadores de absenteísmo.

O objetivo é transformar documentos não estruturados em dados
estruturados automaticamente.

------------------------------------------------------------------------

# 3. Objetivo do MVP

Criar uma aplicação online onde o colaborador possa:

1.  enviar um atestado médico;
2.  armazenar o documento original;
3.  processar o documento com IA;
4.  extrair informações estruturadas;
5.  validar completude dos dados;
6.  preencher manualmente informações ausentes;
7.  salvar os dados no banco;
8.  disponibilizar informações para consultas SQL e dashboards.

------------------------------------------------------------------------

# 4. Escopo

## Incluído

-   Upload de PDF, JPG e PNG.
-   Armazenamento do documento original.
-   Extração usando Gemini multimodal.
-   Retorno estruturado em JSON.
-   Validação de campos obrigatórios.
-   Formulário de complementação.
-   Registro de timestamps.
-   Classificação de envio dentro do prazo ou retroativo.
-   Persistência em PostgreSQL.
-   Scripts SQL para testes e análises.

## Fora do escopo

-   Integração Atesta CFM.
-   Validação de fraude por alteração de imagem.
-   Login corporativo.
-   Integrações com sistemas RH.

------------------------------------------------------------------------

# 5. Fluxo do Usuário

    Colaborador
        |
        v
    Streamlit Upload
        |
        v
    Supabase Storage
        |
        v
    Gemini AI
        |
        v
    JSON Estruturado
        |
        +---- Dados completos
        |
        +---- Dados faltantes
                  |
                  v
            Formulário complementar
        |
        v
    Banco PostgreSQL

------------------------------------------------------------------------

# 6. Regras de Negócio

## Prazo de envio

O colaborador possui até 3 dias corridos após a data de emissão do
atestado.

Cálculo:

`data_upload - data_emissao`

Resultado:

-   Até 3 dias: envio normal.
-   Acima de 3 dias: retroativo para ajuste de absenteísmo.

O sistema não bloqueia envios retroativos.

------------------------------------------------------------------------

# 7. Extração de Dados

O Gemini deverá retornar:

``` json
{
 "nome_colaborador":"",
 "cpf":"",
 "nome_medico":"",
 "crm":"",
 "estabelecimento_saude":"",
 "cid":"",
 "data_emissao":"",
 "inicio_afastamento":"",
 "fim_afastamento":"",
 "quantidade_dias":"",
 "tipo_documento":""
}
```

------------------------------------------------------------------------

# 8. Modelo de Dados

## documents

Tabela responsável pelo controle do arquivo.

Campos:

-   id
-   file_name
-   file_url
-   uploaded_at
-   accepted_at
-   document_issue_date
-   processing_status
-   submission_status
-   created_at
-   updated_at

------------------------------------------------------------------------

## medical_certificates

Dados estruturados do documento.

Campos:

-   id
-   document_id
-   employee_name
-   employee_cpf
-   doctor_name
-   crm
-   health_facility
-   cid
-   issue_date
-   leave_start_date
-   leave_end_date
-   leave_days
-   document_type

------------------------------------------------------------------------

## processing_events

Auditoria do processamento.

Campos:

-   id
-   document_id
-   event_type
-   timestamp
-   details

Eventos:

-   UPLOAD_RECEIVED
-   AI_STARTED
-   AI_COMPLETED
-   USER_COMPLEMENTED
-   FINALIZED

------------------------------------------------------------------------

# 9. Arquitetura Técnica

    Streamlit
        |
    Render
        |
    Python Application
        |
    Gemini API
        |
    Supabase PostgreSQL
        |
    SQL / Dashboards

Tecnologias:

  Componente   Tecnologia
  ------------ ---------------------
  Interface    Streamlit
  Hospedagem   Render
  IA           Gemini API
  Banco        Supabase PostgreSQL
  Código       GitHub
  Linguagem    Python

------------------------------------------------------------------------

# 10. Scripts SQL

O projeto deve conter:

    sql/

    create_schema.sql

    insert_demo_data.sql

    analytics_queries.sql

Objetivos:

-   criação do banco;
-   carga de dados de teste;
-   consultas analíticas.

------------------------------------------------------------------------

# 11. Critérios de Aceitação

O MVP será aceito quando:

-   usuário conseguir enviar documentos;
-   documento for armazenado;
-   IA conseguir extrair informações;
-   sistema detectar campos faltantes;
-   usuário conseguir complementar dados;
-   dados forem persistidos;
-   timestamps forem registrados;
-   equipe técnica conseguir consultar via SQL.

------------------------------------------------------------------------

# 12. Dados de Teste

Serão utilizados documentos médicos para validação do protótipo.

Boas práticas:

-   não publicar documentos reais no GitHub;
-   anonimizar dados em apresentações;
-   utilizar arquivos fictícios em ambientes públicos.

------------------------------------------------------------------------

# 13. Backlog Inicial

## Epic 1 - Infraestrutura

Tasks:

-   criar repositório GitHub;
-   configurar Render;
-   configurar Supabase;
-   configurar variáveis ambiente.

## Epic 2 - Upload

Tasks:

-   interface Streamlit;
-   upload de arquivos;
-   armazenamento.

## Epic 3 - IA

Tasks:

-   integração Gemini;
-   criação de prompts;
-   validação JSON.

## Epic 4 - Banco

Tasks:

-   criação schema;
-   migrations;
-   CRUD.

## Epic 5 - Complementação

Tasks:

-   identificar campos faltantes;
-   criar formulário;
-   atualizar registros.

## Epic 6 - Analytics

Tasks:

-   queries SQL;
-   documentação dos dados.

------------------------------------------------------------------------

# 14. Evoluções Futuras

## Fase 2

Integração Atesta CFM:

-   autenticação;
-   consulta API;
-   validação dos dados.

## Fase 3

Integração corporativa:

-   login;
-   cadastro colaboradores;
-   sistemas RH.

## Fase 4

Analytics:

-   dashboards;
-   indicadores de absenteísmo;
-   análises gerenciais.
