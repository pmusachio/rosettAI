# Tutorial — Passos que dependem de você

Tudo que dava para automatizar (código, testes, dados de demo, configuração
de deploy) já foi feito. O que resta depende de contas/credenciais que só o
responsável pelo projeto pode criar. Siga na ordem — cada seção assume que a
anterior já foi concluída.

---

## 1. Criar o projeto no Supabase (~10 min)

Cobre a task **1.3** do [TASKS.md](../TASKS.md).

1. Acesse [supabase.com](https://supabase.com) e crie uma conta (ou faça login).
2. Clique em **New Project**. Escolha organização, nome (ex: `rosettai`), uma
   senha forte para o banco (guarde em um cofre de senhas — não vai para o
   `.env`) e a região mais próxima do Brasil disponível.
3. Aguarde o provisionamento (1–2 min).
4. Vá em **SQL Editor** → **New query**, cole o conteúdo de
   [sql/create_schema.sql](../sql/create_schema.sql) e execute (`Run`).
   Confirme em **Table Editor** que as tabelas `documents`,
   `medical_certificates` e `processing_events` foram criadas.
5. Em uma nova query, cole [sql/insert_demo_data.sql](../sql/insert_demo_data.sql)
   e execute — isso popula o banco com os 5 registros fictícios usados na
   demo (task **2.4**).
6. Crie o bucket de arquivos: **Storage** → **New bucket** → nome exatamente
   `atestados` (tem que bater com `BUCKET_NAME` em
   [app/services/storage_service.py](../app/services/storage_service.py)).
   Marque como público — nesta fase do MVP não há documentos reais e o PRD já
   aceita esse nível de exposição (ver a seção "Decisões técnicas" do
   [README](../README.md)).
7. Pegue as credenciais em **Project Settings → API**:
   - `Project URL` → `SUPABASE_URL`
   - `anon public` key → `SUPABASE_KEY`
   - `service_role` key → `SUPABASE_SERVICE_KEY` (mais privilegiada — trate
     como senha, nunca cole em chat/documento compartilhado)
8. No seu clone local, copie `.env.example` para `.env` (`cp .env.example .env`)
   e preencha essas três variáveis para poder testar localmente antes do deploy.

---

## 2. Criar a chave de API do Gemini (~5 min)

Cobre a task **1.4**.

1. Acesse [ai.google.dev](https://ai.google.dev) (Google AI Studio) e faça
   login com uma conta Google.
2. **Get API key** → **Create API key** (pode usar um projeto do Google Cloud
   existente ou deixar criar um novo automaticamente).
3. Copie a chave gerada para `GEMINI_API_KEY` no seu `.env`.
4. Teste local: com o `.env` completo, rode:
   ```bash
   source .venv/bin/activate
   streamlit run app/main.py
   ```
   Vá em **Upload de Atestado**, envie
   `demo_assets/atestado_completo_ana_pereira.png` e confirme que os dados
   extraídos são reais (nome "Ana Pereira", CID "R51" etc.) — se aparecer
   "João Mock", a chave não foi lida corretamente (confira o `.env`).
5. O free tier do Gemini tem limite de requisições por minuto; para o volume
   de um único analista de RH isso não deve ser um problema neste MVP.

---

## 3. Deploy no Render (~10–15 min)

Cobre as tasks **1.6** e **8.3**. Fica no Render nesta fase — Google
Cloud/Cloud Run só entra em cena se a empresa comprar a solução.

O [render.yaml](../render.yaml) já commitado no repo faz a maior parte do
trabalho de configuração por você (blueprint):

1. Acesse [render.com](https://render.com) e crie uma conta (dá para usar
   login com GitHub).
2. No dashboard: **New** → **Blueprint**.
3. Conecte sua conta do GitHub e selecione o repositório `rosettAI`.
4. O Render vai detectar o `render.yaml` e mostrar o serviço `rosettai`
   (plano free). As variáveis marcadas `sync: false`
   (`GEMINI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_KEY`)
   vão aparecer como campos para você preencher nessa tela — cole os mesmos
   valores do seu `.env`. Eles ficam só no painel do Render, nunca vão para o Git.
5. Clique em **Apply** / **Create Web Service**. O primeiro deploy roda
   `pip install -r requirements.txt` e depois o `Procfile`
   (`streamlit run app/main.py ...`).
6. Acompanhe a aba **Logs** até aparecer algo como "You can now view your
   Streamlit app in your browser" — o primeiro build pode levar alguns minutos.
7. Abra a URL pública gerada (formato `https://rosettai.onrender.com` ou
   similar) e valide o fluxo completo (upload → IA → histórico).
8. **Atenção:** no plano free o serviço "dorme" após um período sem uso e
   demora ~30–60s para acordar na primeira requisição depois disso — é
   esperado, mas avise o analista de RH para não achar que travou.

---

## 4. Rodar o teste end-to-end com credenciais reais

Cobre a task **7.2** — só é possível depois das seções 1–3.

1. Com tudo configurado (local ou na URL do Render), siga o roteiro da seção
   2 do [docs/demo_guide.md](demo_guide.md) usando os arquivos de
   `demo_assets/`.
2. Confirme cada etapa:
   - [ ] Upload de arquivo → aparece no bucket `atestados` do Supabase Storage
   - [ ] Processamento IA → dados extraídos aparecem corretamente na tela
   - [ ] Complementação (atestado parcial) → dados salvos após preencher os campos obrigatórios
   - [ ] Consulta no histórico → o registro aparece com os dados certos
   - [ ] Query SQL → rode uma query de [sql/analytics_queries.sql](../sql/analytics_queries.sql) no SQL Editor do Supabase e confirme que os números batem com o que você viu na interface
3. Depois de validar, marque a task 7.2 como concluída no [TASKS.md](../TASKS.md).

---

## 5. Fechar a documentação final

Cobre o restante da task **8.4**.

1. Depois do deploy validado (seção 3), edite a seção **Status do Projeto**
   do [README.md](../README.md), trocando "a definir após o deploy" pela URL
   real do Render.
2. Se quiser, decida se vale manter o app sempre "acordado" no Render (planos
   pagos) antes de compartilhar a URL de forma mais ampla com o RH.

---

## Extra: proteção de secrets em qualquer novo clone do repositório

O hook de `detect-secrets` já está instalado neste checkout, mas é local ao
`.git/hooks` — não se propaga sozinho para outro clone/máquina. Sempre que
alguém (você ou outra pessoa) clonar o repositório de novo:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

Isso garante que uma tentativa de commit com uma chave de API real seja
bloqueada antes de chegar ao GitHub (o repositório é público).

---

## Checklist geral

- [ ] Projeto Supabase criado, schema aplicado, bucket `atestados` criado
- [ ] Dados de demonstração inseridos no Supabase
- [ ] Chave Gemini criada e testada localmente
- [ ] Deploy no Render via `render.yaml`, variáveis de ambiente preenchidas
- [ ] Fluxo completo validado na URL pública
- [ ] README atualizado com a URL de produção
- [ ] `pre-commit install` rodado em cada clone novo do repositório
