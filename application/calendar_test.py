from datetime import datetime, date
from hashlib import md5

import pytest
from pytest_postgresql import factories

from application.calendar import Calendar, User, Event


postgresql_test_proc = factories.postgresql_proc(port=None)
postgresql_test = factories.postgresql('postgresql_test_proc')


def test_get_for_week(postgresql_test_proc, postgresql_test):
    calendar = Calendar()
    calendar.database_handler._main_connection = postgresql_test
    calendar.database_handler._main_cursor = calendar.database_handler._main_connection.cursor()

    test_user = User("Test", "test", "a@gmail.com", md5(b"1234567890").digest().hex())
    calendar.update_user(test_user)

    all_events = []
    for day in range(1, 15):
        all_events.append(Event(test_user.id,
                                datetime(2020, 11, day, 11, 00),
                                datetime(2020, 11, day, 12, 00),
                                f"Test event day:{day}"))

    for event in all_events:
        calendar.update_event(event)

    week_events = all_events[1:7]

    # friday
    friday = date(2020, 11, 6)

    # must return events from monday 2020.11.2 to sunday 2020.11.8
    assert all([a == b for a, b in zip(week_events, calendar.get_events_week(test_user, friday))])
