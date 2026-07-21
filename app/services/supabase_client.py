from typing import Optional

from supabase import Client, create_client

from app.config import SUPABASE_KEY, SUPABASE_SERVICE_KEY, SUPABASE_URL

# Este app roda só no servidor (a chave nunca é exposta a um navegador), então
# usamos a service_role key quando disponível: ela ignora RLS, que é o
# comportamento certo para um backend confiável. Cai para a anon key só para
# não quebrar quem ainda não configurou SUPABASE_SERVICE_KEY.
_key = SUPABASE_SERVICE_KEY or SUPABASE_KEY

supabase: Optional[Client] = None
if SUPABASE_URL and _key:
    supabase = create_client(SUPABASE_URL, _key)
