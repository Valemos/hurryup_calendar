from datetime import datetime

from application.event_pattern import EventPattern
from application.user import User, DatabaseSavable

class EventParametric(DatabaseSavable):

    table_name = "eventparametric"
    table_columns = {
        'id':           "SERIAL PRIMARY KEY",
        'start_time':   "TIMESTAMP NOT NULL",
        'end_time':     "TIMESTAMP NOT NULL",
        'name':         "VARCHAR(64) NOT NULL",
        'description':  "TEXT",
        'user_id':      f"INTEGER REFERENCES {User.table_name} ON DELETE CASCADE",
        'patern_id':    f"INTEGER REFERENCES {EventPattern.table_name}(id) ON DELETE CASCADE"
    }

    def __init__(self,
                 start_time: datetime = datetime(1, 1, 1),
                 end_time: datetime = datetime(1, 1, 1),
                 name='',
                 description='',
                 user_id=-1,
                 pattern_id=None):

        super().__init__()
        self.start_time = start_time
        self.end_time = end_time
        self.name = name
        self.description = description
        self.user_id = user_id
        self.patern_id = pattern_id
