import pytest
import unittest

from datetime import date

import application.test_calendar_fixtures


class TestCalendarFeatures(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init_calendar(self, calendar, user_obj, events, event_group, group_events):
        """Uses pytest fixture and runs before each test instead of TestCase.setUp"""
        self.calendar = calendar
        self.test_user = user_obj
        self.events_list = events
        self.test_group = event_group
        self.test_group_events = group_events

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
                self.assertListEqual(self.test_group_events, application.test_calendar_fixtures.events)
                break

    def test_get_all_users(self):
        pass

    def test_get_user_by_name(self):
        pass

    def test_update_user(self):
        pass

    def test_update_event(self):
        pass

    def test_delete_user(self):
        pass

    def test_delete_event(self):
        pass
