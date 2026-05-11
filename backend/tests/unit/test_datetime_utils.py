from datetime import datetime, timezone

from utils.datetime_utils import format_datetime, utcnow


def test_utcnow_returns_timezone_aware():
    now = utcnow()
    assert now.tzinfo is not None
    assert now.tzinfo == timezone.utc


def test_utcnow_is_close_to_real_time():
    import time
    before = datetime.now(timezone.utc).timestamp()
    now = utcnow()
    after = datetime.now(timezone.utc).timestamp()
    assert before <= now.timestamp() <= after


def test_format_datetime_aware():
    dt = datetime(2024, 3, 15, 8, 30, 5, tzinfo=timezone.utc)
    assert format_datetime(dt) == "15/03/2024 08:30:05"


def test_format_datetime_naive_treated_as_utc():
    dt = datetime(2024, 1, 1, 0, 0, 0)
    assert format_datetime(dt) == "01/01/2024 00:00:00"


def test_format_datetime_pads_single_digits():
    dt = datetime(2024, 2, 5, 9, 7, 3, tzinfo=timezone.utc)
    assert format_datetime(dt) == "05/02/2024 09:07:03"
