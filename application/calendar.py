from datetime import date, time, datetime, timedelta
from dateutil.relativedelta import relativedelta

from database.database_handler import DatabaseHandler

from application.user import User
from application.event import Event
from application.event_group import EventGroup
from application.event_pattern import EventPattern
from application.event_parametric import EventParametric


class Calendar:

    def __init__(self, user, database_handler=None):

        # to set another user it can be accessed as calendar object attribute
        self.user = user
        self.database_handler = database_handler if database_handler is not None else DatabaseHandler()

        # check connection to database here
        if not self.database_handler.check_connected():
            print("Application not connected to database")

    def get_events_today(self, request_date: date):
        """
        Using request_date to get events_list starting from 0:00 AM current date to 00:00 AM after this date

        :param user: user object
        :param request_date: date to get events list for it
        :return: list of events for current day
        """
        today = datetime.combine(request_date, time(0, 0, 0))
        return self.database_handler.get_events_for_period(self.user, today, today + timedelta(days=1))

    def get_events_week(self, request_date: date):
        """
        Using request_date to get events_list starting from Monday to Sunday of this week

        :param request_date: date corresponds to some week
        :return: list of events for current week
        """
        first_day = request_date - timedelta(days=request_date.weekday())
        first_day = datetime.combine(first_day, time(0, 0, 0))
        return self.database_handler.get_events_for_period(self.user, first_day, first_day + timedelta(days=7))

    def get_events_month(self, request_date: date):
        """
        Use request_date to get first day of month and get all events_list to last day of month

        :param request_date: date corresponds to some month
        :return: list of events for current month
        """
        first_day = request_date - timedelta(days=request_date.day + 1)
        first_day = datetime.combine(first_day, time(0, 0, 0))
        last_day = first_day + relativedelta(months=1)
        return self.database_handler.get_events_for_period(self.user, first_day, last_day - timedelta(days=1))

    def update_user(self):
        """
        Inserts or updates current user in database
        """
        self.user.update_db(self.database_handler)

    def update_event(self, event: Event):
        """
        insert or update Event object to database

        :param event: Event object
        """
        event.user_id = self.user.id
        event.update_db(self.database_handler)

    def update_event_group(self, group: EventGroup):
        """
        inserts or updates EventGroup object

        :param group: EventGroup object
        """
        group.update_db(self.database_handler)

    def get_event_groups(self):
        """
        Returns all event groups with events_list list
        :return: list of EventGroup objects
        """
        return self.database_handler.get_event_groups(self.user)

    def add_event_to_group(self, group: EventGroup, event: Event):
        """
        Updates group id inside event and updates database entry

        :param group: target event group
        :param event: event object of current user to add to group
        """
        event.group_id = group.id
        self.database_handler.update_fields(event, ["group_id"])

    def get_event_patterns(self):
        """
        retrieves all patterns with events_list from database
        :param user: user object, requested event patterns
        :return: list of event patterns
        """
        return self.database_handler.get_all_event_patterns(self.user)

    def add_parametric_event(self, event_pattern: EventPattern, event: EventParametric):
        """
        Inserts EventParametric to be associated with EventPattern inside event in database
        :param event_pattern: event pattern to add event to
        :param event: EventParametric object that contains required
        """
        event_pattern.add_event(event, self.database_handler)