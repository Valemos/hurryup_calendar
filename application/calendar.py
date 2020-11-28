from datetime import date, time, datetime, timedelta

from database.database_handler import DatabaseHandler

from application.user import User
from application.event import Event
from application.event_group import EventGroup
from application.event_pattern import EventPattern
from application.event_parametric import EventParametric


class Calendar:

    def __init__(self):
        self.database_handler = DatabaseHandler()
        # check connection to database here

    def get_events_today(self, user: User, request_date: date):
        """
        Using request_date to get events starting from Monday to Sunday of this week

        :param user:
        :param request_date:
        :return:
        """

        # get first day of current week
        first_day = request_date - timedelta(days=request_date.weekday())
        return self.database_handler.get_events_for_period(user, first_day, first_day + timedelta(days=7))

    def get_events_week(self, user: User, request_date: date):
        """
        Using request_date to get events starting from Monday to Sunday of this week

        :param user:
        :param request_date:
        :return:
        """

        # get first day of current week
        first_day = request_date - timedelta(days=request_date.weekday())
        return self.database_handler.get_events_for_period(user, first_day, first_day + timedelta(days=7))

    def get_events_month(self, user: User, request_date: date):
        """
        Use request_date to get first day of month and get all events to last day of month

        :param user: User object, requested events
        :param request_date: date corresponds to some month
        :return:
        """
        pass

    def update_user(self, user: User):
        """
        Inserts or updates user in database
        :param user: User object to add
        """
        self.database_handler.update_user(user)

    def update_event(self, event: Event):
        """
        insert or update Event object to database

        :param event: Event object
        :return:
        """
        self.database_handler.update_user_object(event)

    def update_event_group(self, group: EventGroup):
        """
        inserts or updates EventGroup object

        :param group: EventGroup object
        """
        pass

    def get_event_groups(self, user: User):
        """
        Returns all event groups with events list
        :param user: user, requested to get all his groups
        :return: list of EventGroup objects
        """
        return self.database_handler.get_all_event_groups(user)

    def get_event_patterns(self, user: User):
        """
        retrieves all patterns with events from database
        :param user: user object, requested event patterns
        :return: list of event patterns
        """
        pass
    # event patterns

    def add_parametric_event(self, event_pattern: EventPattern, event: EventParametric):
        """
        Appends event to event_pattern in database
        :param event_pattern:
        :param event: EventParametric object to add to EventPattern
        """
        pass
