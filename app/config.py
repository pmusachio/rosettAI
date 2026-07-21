import os
from dotenv import load_dotenv

load_dotenv()

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# A Google descontinua/restringe modelos com pouco aviso — configurável para
# não precisar de deploy toda vez que isso acontecer (ver README).
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY") # Optional, but good for backend tasks
