from typing import Optional
import uuid
import mimetypes
from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY

supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET_NAME = "atestados"


class StorageError(Exception):
    """Falha ao enviar ou ler um arquivo no Supabase Storage (rede, credenciais, bucket, etc.)."""


def upload_file(file_bytes: bytes, original_file_name: str) -> str:
    """Uploads a file to Supabase Storage and returns the public URL."""
    if not supabase:
        return f"https://mock-url.com/{original_file_name}" # Mock

    # Generate unique filename to avoid collisions
    ext = original_file_name.split('.')[-1] if '.' in original_file_name else ''
    unique_filename = f"{uuid.uuid4()}.{ext}"

    # Determine mime type
    mime_type, _ = mimetypes.guess_type(original_file_name)
    if not mime_type:
        mime_type = "application/octet-stream"

    try:
        # Upload to Supabase
        supabase.storage.from_(BUCKET_NAME).upload(
            unique_filename,
            file_bytes,
            file_options={"content-type": mime_type}
        )

        # Get public URL
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_filename)
    except Exception as exc:
        raise StorageError(f"Falha ao enviar o arquivo para o Storage: {exc}") from exc

    return public_url
