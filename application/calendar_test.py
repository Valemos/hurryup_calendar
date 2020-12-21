import pytest
import unittest

from datetime import datetime, date
from hashlib import md5

from application.event_group import EventGroup
from database.database_handler import DatabaseHandler
from application.calendar import Calendar, User, Event



@pytest.fixture()
def db_handler_obj() -> DatabaseHandler:
    handler = DatabaseHandler(new_name="testcalendar")
    handler._recreate_all_tables()
    return handler

@pytest.fixture()
def user_obj(db_handler_obj):
    return db_handler_obj.update_user(User("Test", "test", "a@gmail.com", md5(b"1234567890").digest().hex()))

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
def event_group_obj(db_handler_obj, user_obj):
    return db_handler_obj.update(EventGroup("Test group", user_id=user_obj.id))

@pytest.fixture()
def event_group_elements(calendar, event_group_obj, events):
    group_events = events[4:8]
    for event in group_events:
        calendar.add_event_to_group(event_group_obj, event)
    return group_events


class TestCalendarFeatures(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init_calendar(self, calendar, user_obj, events, event_group_obj, event_group_elements):
        """Uses pytest fixture and runs before each test instead of TestCase.setUp"""
        self.calendar = calendar
        self.test_user = user_obj
        self.events_list = events
        self.test_group = event_group_obj
        self.test_group_events = event_group_elements

    def test_get_for_week(self):
        for event in self.events_list:
            self.calendar.update_event(event)

        week_events = self.events_list[1:8]
        friday = date(2020, 11, 6)
        # must return events_list from monday 2020.11.2 to sunday 2020.11.8
        self.assertCountEqual(week_events, self.calendar.get_events_current_week(friday))

    def test_events_for_month(self):
        for event in self.events_list:
            self.calendar.update_event(event)

        month_events = self.events_list[0:30]
        current_date = date(2020, 11, 6)
        # from 2020.11.1 to sunday 2020.11.30
        self.assertCountEqual(month_events, self.calendar.get_events_current_month(current_date))

    def test_get_all_event_groups(self):
        elements = self.calendar.get_event_groups()

        # find object group
        for group in elements:
            if group.name == self.test_group.name:
                # group found
                self.assertListEqual(self.test_group_events, group.events)
                break

    def test_get_all_users(self):
        pass

    def test_get_user_by_name(self):
        pass

    def test_get_all_events(self):
        pass

    def test_get_events_by_date(self):
        pass

    def test_update_user(self):
        pass

    def test_update_event(self):
        pass

    def test_delete_user(self):
        pass

    def test_delete_event(self):
        pass
