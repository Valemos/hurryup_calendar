from abc import ABC
from datetime import datetime, timedelta

from application.event_group import EventGroup, DatabaseSavable
from application.user import User


class Event(DatabaseSavable):

    table_name = "\"Event\""
    table_columns = {
        'id':               "SERIAL PRIMARY KEY",
        'user_id':          f"INTEGER REFERENCES {User.table_name}",
        'time_start':       "TIMESTAMP NOT NULL",
        'time_end':         "TIMESTAMP NOT NULL",
        'name':             "VARCHAR(64) NOT NULL",
        'description':      "TEXT",
        'event_group_id':   f"INTEGER REFERENCES {EventGroup.table_name}(id)",
        'done':             "BOOLEAN"
    }

    def __init__(self,
                 user_id,
                 time_start: datetime,
                 time_end: datetime,
                 name='', description='',
                 event_group_id=None,
                 done=False):
        super().__init__()
        self.user_id = user_id
        self.name = name
        self.time_start = time_start
        self.time_end = time_end
        self.description = description
        self.event_group_id = event_group_id
        self.done = done

    def move_by_period(self, delta: timedelta):
        self.time_start += delta
        self.time_end += delta


class EventParticipants(DatabaseSavable, ABC):

    table_name = "\"EventParticipants\""
    table_columns = {
        'event_id': f"INTEGER REFERENCES {Event.table_name}(id)",
        'user_id':  f"INTEGER REFERENCES {User.table_name}(id)"
    }
