from datetime import datetime

from application.event_pattern import EventPattern
from application.user import User, DatabaseSavable

class EventParametric(DatabaseSavable):

    table_name = "\"EventParametric\""
    table_columns = {
        'id':           "SERIAL PRIMARY KEY",
        'user_id':      f"INTEGER REFERENCES {User.table_name} ON DELETE CASCADE",
        'start_time':   "TIMESTAMP NOT NULL",
        'end_time':     "TIMESTAMP NOT NULL",
        'description':  "TEXT",
        'patern_id':    f"INTEGER REFERENCES {EventPattern.table_name}(id) ON DELETE CASCADE"
    }

    def __init__(self, user: User, event_pattern: EventPattern, start_time: datetime, end_time: datetime, name, description=''):
        super().__init__()
        self.user = user
        self.user_id = user.id
        self.event_pattern = event_pattern
        self.patern_id = event_pattern.id
        self.start_time = start_time
        self.end_time = end_time

        self.name = name
        self.description = description
