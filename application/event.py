from abc import ABC
from datetime import datetime, timedelta

from application.event_group import EventGroup, DatabaseSavable
from application.user import User


class Event(DatabaseSavable):

    table_name = "\"Event\""
    table_columns = {
        'id':           "SERIAL PRIMARY KEY",
        'time_start':   "TIMESTAMP NOT NULL",
        'time_end':     "TIMESTAMP NOT NULL",
        'name':         "VARCHAR(64) NOT NULL",
        'description':  "TEXT",
        'user_id':      f"INTEGER REFERENCES {User.table_name} ON DELETE CASCADE",
        'group_id':     f"INTEGER REFERENCES {EventGroup.table_name}(id)",
        'done':         "BOOLEAN"
    }

    def __init__(self,
                 time_start: datetime = datetime(0, 0, 0),
                 time_end: datetime = datetime(0, 0, 0),
                 name='',
                 description='',
                 user_id=-1,
                 group_id=None,
                 done=False,
                 participants=None):
        super().__init__()
        self.name = name
        self.time_start = time_start
        self.time_end = time_end
        self.description = description
        self.user_id = user_id
        self.participants = [] if participants is None else participants
        self.group_id = group_id
        self.done = done

    def move_by_period(self, delta: timedelta):
        self.time_start += delta
        self.time_end += delta

    def move_to_datetime(self, new_time: datetime):
        time_difference = self.time_start - new_time
        self.move_by_period(time_difference)
