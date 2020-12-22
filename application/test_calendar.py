import unittest

from application.test_calendar_fixtures import *


class TestCalendarFeatures(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init_calendar(self, calendar_user, user_obj, events, event_group, group_events, request_date):
        """Uses pytest fixture and runs before each test instead of TestCase.setUp"""
        self.calendar_user: CalendarUser = calendar_user
        self.test_user: User = user_obj
        self.test_events: list = events
        self.test_group: EventGroup = event_group
        self.test_group_events: list = group_events
        self.request_date = request_date

    def test_get_for_week(self):
        for event in self.test_events:
            self.calendar_user.update_event(event)

        week_events = self.test_events[1:8]
        friday = date(2020, 11, 6)
        # must return test_events from monday 2020.11.2 to sunday 2020.11.8
        self.assertCountEqual(week_events, self.calendar_user.get_events_current_week(friday))

    def test_events_for_month(self):
        for event in self.test_events:
            self.calendar_user.update_event(event)

        month_events = self.test_events[0:30]
        current_date = date(2020, 11, 6)
        # from 2020.11.1 to sunday 2020.11.30
        self.assertCountEqual(month_events, self.calendar_user.get_events_current_month(current_date))

    def test_get_all_event_groups(self):
        elements = self.calendar_user.get_event_groups()

        # find object group
        for group in elements:
            if group.name == self.test_group.name:
                # test group found
                self.assertListEqual(self.test_group_events, group.events)
                break

    def test_get_user_by_login(self):
        search_login = self.test_user.login

        self.calendar_user.get_user_by_login(search_login)

    def test_update_user(self):
        new_test_name = "NewTestName"
        self.calendar_user.user.name = new_test_name
        self.calendar_user.update_user()

        fetched_user = self.calendar_user.get_user_by_login(self.calendar_user.user.login)
        self.assertIsNotNone(fetched_user)
        self.assertEqual(new_test_name, fetched_user.name)

    def test_update_event(self):
        new_event_name = "NewTestEventName"

        today_events = self.calendar_user.get_events_day(self.request_date)
        self.assertIsNotNone(today_events)
        self.assertTrue(len(today_events) > 0)
        event = today_events[0]
        event.name = new_event_name
        self.calendar_user.update_event(event)

        new_today_events = self.calendar_user.get_events_day(self.request_date)
        self.assertEqual(event.name, new_today_events[0].name)


    def test_delete_current_user(self):
        self.calendar_user.delete_current_user()

        fetched_user = self.calendar_user.get_user_by_login(self.test_user.login)
        self.assertIsNone(fetched_user)

    def test_delete_event(self):
        start_events = self.calendar_user.get_events_current_week(self.request_date)
        event_to_delete = start_events[3]
        start_events.pop(3)
        self.calendar_user.delete_event(event_to_delete)

        new_events = self.calendar_user.get_events_current_week(self.request_date)
        self.assertCountEqual(start_events, new_events)
