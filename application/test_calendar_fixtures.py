from datetime import datetime
from hashlib import md5

import pytest

from application.account_type import AccountType
from application.calendar import Calendar
from application.event import Event
from application.event_group import EventGroup
from application.user import User
from database.database_handler import DatabaseHandler


@pytest.fixture()
def db_handler_obj() -> DatabaseHandler:
    handler = DatabaseHandler(new_name="testcalendar")
    handler._recreate_all_tables()
    return handler


@pytest.fixture()
def user_obj(db_handler_obj):
    return db_handler_obj.update_user(
        User("Test", "test", "user@gmail.com",
             md5(b"1234567890").digest().hex()))

@pytest.fixture()
def admin_obj(db_handler_obj):
    return db_handler_obj.update_user(
        User(
            "TestAdmin", "admin", "admin@gmail.com",
            md5(b"1234567890").digest().hex(),
            AccountType.Admin))


@pytest.fixture()
def calendar(db_handler_obj, user_obj):
    return Calendar(user_obj, db_handler_obj)


@pytest.fixture()
def events(db_handler_obj, user_obj):
    all_events = []
    for day in range(1, 15):
        event = Event(datetime(2020, 11, day, 11, 00),
                      datetime(2020, 11, day, 12, 00),
                      f"Event {day}",
                      user_id=user_obj.id)
        db_handler_obj.update(event)
        all_events.append(event)
    return all_events


@pytest.fixture()
def event_group(db_handler_obj, user_obj):
    return db_handler_obj.update(EventGroup("Test group", user_id=user_obj.id))


@pytest.fixture()
def group_events(calendar, event_group, events):
    group_events = events[4:8]
    for event in group_events:
        calendar.add_event_to_group(event_group, event)
    return group_events