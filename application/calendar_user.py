from datetime import date, time, datetime, timedelta
import calendar

from database.database_handler import DatabaseHandler

from application.user import User
from application.event import Event
from application.event_group import EventGroup
from application.event_pattern import EventPattern
from application.event_parametric import EventParametric


class CalendarUser:

    def __init__(self, user: User, database_handler=None):

        # to set another user it can be accessed as calendar_user object attribute
        self.user = user
        self.database_handler: DatabaseHandler = database_handler if database_handler is not None else DatabaseHandler()

        # check connection to database here
        if not self.database_handler.check_connected():
            print("Application not connected to database")

    def get_events_day(self, request_date: date):
        today = datetime.combine(request_date, time(0, 0, 0))
        return self.database_handler.get_events_for_period(self.user, today, today + timedelta(days=1))

    def get_events_current_week(self, request_date: date):
        first_day = request_date - timedelta(days=request_date.weekday())
        first_day = datetime.combine(first_day, time(0, 0, 0))
        last_day = first_day + timedelta(days=7)
        return self.database_handler.get_events_for_period(self.user, first_day, last_day)

    @staticmethod
    def increment_month(input_date, months):
        month = input_date.month - 1 + months
        year = input_date.year + month // 12
        month = month % 12 + 1
        day = min(input_date.day, calendar.monthrange(year, month)[1])
        return datetime(year, month, day)

    def get_events_current_month(self, request_date: date):
        first_day = request_date - timedelta(days=request_date.day + 1)
        first_day = datetime.combine(first_day, time(0, 0, 0))
        last_day = self.increment_month(first_day, 1)
        last_day -= timedelta(days=1)
        return self.database_handler.get_events_for_period(self.user, first_day, last_day)

    def update_user(self):
        self.user.update_db(self.database_handler)

    def update_event(self, event: Event):
        event.user_id = self.user.id
        event.update_db(self.database_handler)

    def update_event_group(self, group: EventGroup):
        group.update_db(self.database_handler)

    def get_event_groups(self):
        return self.database_handler.get_event_groups(self.user)

    def add_event_to_group(self, group: EventGroup, event: Event):
        event.group_id = group.id
        group.events.append(event)
        self.database_handler.update_fields(event, ["group_id"])

    def get_event_patterns_with_events(self):
        return self.database_handler.get_event_patterns(self.user)

    def add_parametric_event(self, event_pattern: EventPattern, event: EventParametric):
        event_pattern.add_event(event, self.database_handler)

    def get_user_by_login(self, search_login):
        return self.database_handler.get_user_by_login(search_login)

    def delete_current_user(self):
        self.database_handler.delete_user(self.user)
        self.user = None

    def delete_event(self, event):
        self.database_handler.delete(event)
