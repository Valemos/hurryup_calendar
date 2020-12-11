from datetime import date, time, datetime, timedelta
from dateutil.relativedelta import relativedelta

from database.database_handler import DatabaseHandler

from application.user import User
from application.event import Event
from application.event_group import EventGroup
from application.event_pattern import EventPattern
from application.event_parametric import EventParametric


class Calendar:

    def __init__(self, database_handler=None):
        self.database_handler = database_handler if database_handler is not None else DatabaseHandler()

        # check connection to database here
        if not self.database_handler.check_connected():
            print("Application not connected to database")

    def get_events_today(self, user: User, request_date: date):
        """
        Using request_date to get events_list starting from 0:00 AM today to 00:00 AM tomorrow

        :param user: user object
        :param request_date: date to get events_list
        :return: events_list list
        """

        today = datetime.combine(request_date, time(0, 0, 0))
        return self.database_handler.get_events_for_period(user, today, today + timedelta(days=1))

    def get_events_week(self, user: User, request_date: date):
        """
        Using request_date to get events_list starting from Monday to Sunday of this week

        :param user:
        :param request_date:
        :return:
        """

        # get first day of current week
        first_day = request_date - timedelta(days=request_date.weekday())
        first_day = datetime.combine(first_day, time(0, 0, 0))
        return self.database_handler.get_events_for_period(user, first_day, first_day + timedelta(days=7))

    def get_events_month(self, user: User, request_date: date):
        """
        Use request_date to get first day of month and get all events_list to last day of month

        :param user: User object, requested events_list
        :param request_date: date corresponds to some month
        :return:
        """
        first_day = request_date - timedelta(days=request_date.day + 1)
        first_day = datetime.combine(first_day, time(0, 0, 0))
        last_day = first_day + relativedelta(months=1)
        return self.database_handler.get_events_for_period(user, first_day, last_day - timedelta(days=1))

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
        self.database_handler.update(event)

    def update_event_group(self, group: EventGroup):
        """
        inserts or updates EventGroup object

        :param group: EventGroup object
        """
        self.database_handler.update(group)

    def get_event_groups(self, user: User):
        """
        Returns all event groups with events_list list
        :param user: user, requested to get all his groups
        :return: list of EventGroup objects
        """
        return self.database_handler.get_event_groups(user)

    def add_event_to_group(self, group: EventGroup, event: Event):
        """
        Updates group id inside event and updates database entry

        :param group: target event group
        :param event: event object of current user to add to group
        """
        event.group_id = group.id
        self.database_handler.update_fields(event, ["group_id"])

    def get_event_patterns(self, user: User):
        """
        retrieves all patterns with events_list from database
        :param user: user object, requested event patterns
        :return: list of event patterns
        """
        return self.database_handler.get_all_event_patterns(user)

    def add_parametric_event(self, event: EventParametric):
        """
        Inserts EventParametric to be associated with EventPattern inside event in database
        :param event: EventParametric object to add to EventPattern in database
        """
        self.database_handler.update(event)