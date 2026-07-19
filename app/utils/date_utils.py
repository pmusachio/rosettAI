from typing import Optional
from datetime import date, datetime

def calculate_submission_status(issue_date: date, upload_date: date = None) -> str:
    """
    Calculates if the submission is on time or retroactive.
    Rules: up to 3 calendar days after issue = on_time
    Above 3 days = retroactive
    """
    if upload_date is None:
        upload_date = date.today()
        
    delta = upload_date - issue_date
    if delta.days <= 3:
        return "on_time"
    return "retroactive"

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
