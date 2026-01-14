import pytest
from datetime import datetime, timezone
from app.services.report_service import get_month_range


def test_get_month_range():
    start_dt, end_dt_exclusive = get_month_range("2026-01")
    assert start_dt == datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert end_dt_exclusive == datetime(2026, 2, 1, tzinfo=timezone.utc)
    assert start_dt != datetime(2026, 2, 1, tzinfo=timezone.utc)
    assert end_dt_exclusive != datetime(2026, 2, 28, tzinfo=timezone.utc)
    assert start_dt.month + 1 == end_dt_exclusive.month
    start_dt, end_dt_exclusive = get_month_range("2025-12")
    assert end_dt_exclusive.year == 2026 and end_dt_exclusive.month == 1 


