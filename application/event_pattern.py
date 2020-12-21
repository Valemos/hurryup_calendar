from application.event_parametric import EventParametric
from application.user import User, DatabaseSavable

class EventPattern(DatabaseSavable):

    table_name = "\"EventPattern\""
    table_columns = {
        'id':           "SERIAL PRIMARY KEY",
        'name':         "VARCHAR(64) NOT NULL",
        'description':  "TEXT",
        'user_id':      f"INTEGER REFERENCES {User.table_name}(id) ON DELETE CASCADE"
    }

    def __init__(self, name='', description='', user_id=-1, events=None):
        super().__init__()

        self.user_id = user_id
        self.name = name
        self.description = description
        self.events = events if events is not None else []

    def add_event(self, event: EventParametric, database):
        event.user_id = self.user_id
        event.pattern_id = self.id
        database.update(event)
        self.events.append(event)
