import pytest
import unittest

from application.test_calendar_fixtures import *


class TestAdminCalendar(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init_test_objects(self, calendar_admin, user_obj, admin_obj, events, event_group, group_events):
        self.calendar_admin: CalendarAdmin = calendar_admin
        self.test_user = user_obj
        self.test_admin = admin_obj
        self.events_list = events
        self.test_group = event_group
        self.test_group_events = group_events

    def test_admin_calendar_created(self):
        self.assertRaises(CalendarAdmin.NotAdminUserException, CalendarAdmin, self.test_user)

    def test_admin_get_other_users(self):
        users = self.calendar_admin.get_all_users()

        self.assertIn(self.test_admin, users)
        self.assertIn(self.test_user, users)
