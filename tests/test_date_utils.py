import pytest
from datetime import date
from app.utils.date_utils import calculate_submission_status, parse_date_br

def test_calculate_submission_status_on_time():
    issue = date(2026, 1, 1)
    upload = date(2026, 1, 3) # 2 days diff
    assert calculate_submission_status(issue, upload) == "on_time"

def test_calculate_submission_status_retroactive():
    issue = date(2026, 1, 1)
    upload = date(2026, 1, 5) # 4 days diff
    assert calculate_submission_status(issue, upload) == "retroactive"
    
def test_parse_date_br():
    assert parse_date_br("15/01/2026") == date(2026, 1, 15)
    assert parse_date_br("2026-01-15") == date(2026, 1, 15)
    assert parse_date_br("") is None
    assert parse_date_br("data_invalida") is None
