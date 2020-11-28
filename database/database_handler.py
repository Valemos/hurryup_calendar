from datetime import datetime


class DatabaseHandler:

    def __init__(self):
        pass

    def get_events_for_period(self, user, start: datetime, end: datetime):
        """get all events in given date range as list"""
        pass
        
    def get_all_event_patterns(self, user):
        """return all event patterns"""
        pass

    def get_all_event_groups(self, user):
        """
        
        :param user: User object
        :return: list of EventGroup objects with their events
        """
        pass

    def get_events_for_group(self, user, group):
        # return all events by event group
        pass

    def update_user(self, user: User):
        """
        Updates user if it was already created
        Inserts user if it is new in table
        """
        pass

    def update_user_object(self, object_):
        """
        Updates entity if it was already created
        Inserts entity if it is new in table
        """
        pass
