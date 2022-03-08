from datetime import date, datetime, timedelta, time

import pytest

from releaser.config import relative_time


@pytest.mark.parametrize("s,exp", [
    ("today", date.today()),
    ("tomorrow", date.today() + timedelta(days=1)),
    ("in 2 days", date.today() + timedelta(days=2)),
    ("in 2 days at 21:45", datetime.combine(
        date.today() + timedelta(days=2), time(21, 45)).astimezone()
     ),
    ("today at 21:45", datetime.combine(date.today(), time(21, 45)).astimezone()),
    ("today @ 21:45", datetime.combine(date.today(), time(21, 45)).astimezone()),
    ("21:45", datetime.combine(date.today(), time(21, 45)).astimezone()),
    ("3:13", datetime.combine(date.today(), time(3, 13)).astimezone()),
])
def test_parse_relative_date(s, exp):
    assert relative_time(s) == exp
