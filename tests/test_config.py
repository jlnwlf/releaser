from datetime import date, datetime, timedelta, time

import pytest

from releaser.config import relative_time


@pytest.mark.parametrize("s,exp", [
    ("today", date.today()),
    ("tomorrow", date.today() + timedelta(days=1)),
    ("in 2 days", date.today() + timedelta(days=2)),
    ("in 2 days at 21:45", datetime.combine(
        date.today() + timedelta(days=2), time(21, 45))
     ),
    ("today at 21:45", datetime.combine(date.today(), time(21, 45))),
    ("today @ 21:45", datetime.combine(date.today(), time(21, 45))),
    ("21:45", datetime.combine(date.today(), time(21, 45))),
    ("3:13", datetime.combine(date.today(), time(3, 13))),
])
def test_parse_relative_date(s, exp):
    assert relative_time(s) == exp
