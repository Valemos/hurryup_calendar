from application.user import User, DatabaseSavable

class EventPattern(DatabaseSavable):

    table_name = "\"EventPattern\""
    table_columns = {
        'id':           "SERIAL PRIMARY KEY",
        'user_id':      f"INTEGER REFERENCES {User.table_name}(id) ON DELETE CASCADE",
        'name':         "VARCHAR(64) NOT NULL",
        'description':  "TEXT"
    }

    def __init__(self, user, name, description='', events=None):
        super().__init__()

        if events is None:
            self.events = []
        else:
            self.events = events

        self.user = user
        self.user_id = user.id
        self.name = name
        self.description = description

    def add_event(self, event, database):
        self.events.append(event)
        database.update(self.user, event)
