from typing import Optional
from datetime import date, datetime

def parse_date_br(date_str: str) -> Optional[date]:
    """Parses a date string in format DD/MM/YYYY to date object."""
    if not date_str:
        return None
    try:
        # Assuming Gemini might return in different formats, but we prompt for DD/MM/YYYY
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        try:
            # Fallback ISO format
            return datetime.fromisoformat(date_str).date()
        except ValueError:
            return None
