import pytest
from datetime import date
from app.utils.date_utils import parse_date_br

def test_parse_date_br():
    assert parse_date_br("15/01/2026") == date(2026, 1, 15)
    assert parse_date_br("2026-01-15") == date(2026, 1, 15)
    assert parse_date_br("") is None
    assert parse_date_br("data_invalida") is None
