import pytest

from datetime import datetime, date
from hashlib import md5

from database.database_handler import DatabaseHandler
from application.calendar import Calendar, User, Event

@pytest.fixture()
def calendar():
    calendar = Calendar(DatabaseHandler(new_name="testcalendar"))
    calendar.database_handler._recreate_all_tables()
    return calendar


def test_get_for_week(calendar):

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

    week_events = all_events[1:8]

    # friday
    friday = date(2020, 11, 6)

    # must return events from monday 2020.11.2 to sunday 2020.11.8
    assert all([a.id == b.id for a, b in zip(week_events, calendar.get_events_week(test_user, friday))])
