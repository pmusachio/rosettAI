# Guia de Demonstração — rosettAI (MVP)

> Roteiro para apresentar o MVP ao time de RH. Assume que o deploy no Render já
> está no ar e que o Supabase foi populado com `sql/insert_demo_data.sql`
> (ver [TUTORIAL_PROXIMOS_PASSOS.md](TUTORIAL_PROXIMOS_PASSOS.md)).

## 1. Contexto (2 min)

Abrir explicando o problema, não a tecnologia:

- Hoje o analista de RH recebe atestados por e-mail, digita os dados manualmente e corre risco de erro de transcrição.
- O rosettAI recebe o mesmo documento, lê com IA e devolve os dados já estruturados — o analista só confirma ou completa o que faltar.
- Este é um MVP com dados **fictícios**: nenhum atestado real foi usado.

## 2. Passo a passo da demo (8–10 min)

1. Abrir a URL do rosettAI (página inicial) — mostrar o menu lateral (Upload / Histórico).
2. Ir em **Upload de Atestado** e enviar `demo_assets/atestado_completo_ana_pereira.png` (gerado por `scripts/generate_demo_assets.py`).
   - Mostrar o preview do arquivo antes de enviar.
   - Clicar em "Enviar para Processamento" e narrar o que está acontecendo (upload → IA → validação).
   - Como todos os campos obrigatórios foram extraídos, o fluxo vai direto para a tela de sucesso.
3. Repetir o upload com `demo_assets/atestado_parcial_fernando_rocha.png` (documento com médico/CRM/CID ilegíveis).
   - Mostrar a tela de complementação: campos já extraídos vêm preenchidos, os que faltaram ficam em branco para o analista completar.
   - Preencher os campos obrigatórios faltantes e salvar — destacar que o sistema não deixa salvar sem os campos obrigatórios (`*`).
4. Ir em **Histórico** e mostrar a tabela com os atestados já processados (inclui os dados de demonstração do `insert_demo_data.sql`).
   - Selecionar um registro e abrir os detalhes: dados extraídos, link para o documento original, timeline de eventos de auditoria (`UPLOAD_RECEIVED` → `AI_STARTED` → `AI_COMPLETED` → `USER_COMPLEMENTED` → `FINALIZED`).
5. (Opcional, se houver acesso ao Supabase SQL Editor) Rodar 1–2 queries de `sql/analytics_queries.sql` ao vivo — por exemplo, "CIDs mais frequentes" ou "dias de absenteísmo por mês" — para mostrar o valor analítico dos dados estruturados.

## 3. Talking points

- **Redução de digitação manual**: o analista revisa em vez de transcrever do zero.
- **Rastreabilidade**: todo atestado tem uma timeline de auditoria completa — quando chegou, quando a IA processou, se e quando foi complementado manualmente.
- **Dados prontos para análise**: assim que estruturados, os dados já suportam consultas SQL (CIDs mais comuns, dias de afastamento por mês, colaboradores com mais atestados) sem trabalho manual extra.
- **Fora de escopo por decisão consciente, não por limitação**: cálculo de prazo (dentro do prazo vs. retroativo) fica com o ADP, que já tem essa regra; login corporativo e integração com o Atesta CFM ficam para fases futuras.

## 4. Perguntas esperadas e respostas

**"A IA erra?"**
Sim, principalmente com documentos manuscritos ou de baixa qualidade — por isso existe a etapa de complementação manual. Nenhum atestado é salvo sem que os campos obrigatórios estejam preenchidos, seja pela IA ou manualmente.

**"E se eu enviar o atestado errado, dá pra apagar?"**
Neste MVP não há exclusão pela interface — é um ambiente de validação, não o sistema final. Ajustes podem ser feitos diretamente no banco pela equipe técnica.

**"Isso substitui o Atesta CFM?"**
Não. Essa integração está fora do escopo desta primeira versão (depende de acesso corporativo/CNPJ) e é uma evolução futura prevista no PRD.

**"Quem mais vai poder acessar isso?"**
Nesta fase, apenas o analista de RH responsável pelos uploads — o controle de acesso mais amplo (login, permissões por papel) é uma decisão consciente adiada para uma fase posterior, não uma lacuna esquecida.

**"Isso vai para produção onde?"**
Nesta fase o deploy é no Render. Uma eventual migração para Google Cloud (Cloud Run) e BigQuery só ocorre se a empresa decidir adquirir a solução — não faz parte do MVP atual.

**"Os dados dos atestados são seguros?"**
O código-fonte é público no GitHub, mas nenhuma credencial fica nele — chaves de API e acesso ao banco ficam fora do repositório e são configuradas apenas no ambiente de execução. Os documentos e dados extraídos (inclusive CPF) ficam no Supabase, acessível apenas com as credenciais do projeto.

## 5. Métricas de sucesso do MVP

Considerar o MVP validado quando, com dados reais (não sintéticos) de um piloto controlado:

- A maioria dos atestados tem os campos obrigatórios extraídos corretamente pela IA sem intervenção manual.
- O tempo entre upload e dado estruturado no banco é sensivelmente menor do que a digitação manual atual.
- O analista de RH consegue localizar qualquer atestado processado no Histórico sem precisar da equipe técnica.
- Nenhum erro de processamento (upload, IA ou banco) derruba a aplicação sem explicação — todo erro aparece como mensagem clara na tela.
