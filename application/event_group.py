from application.user import User
from database.database_savable import DatabaseSavable

class EventGroup(DatabaseSavable):

    table_name = "\"EventGroup\""

    table_columns = {
        "id":           "SERIAL PRIMARY KEY",
        "user_id":      f"INTEGER REFERENCES {User.table_name}(id)",
        "name":         "VARCHAR(64) NOT NULL",
        "description":  "TEXT",
        "done":         "BOOLEAN"
    }

    def __init__(self, user, name, description='', events=None):
        super().__init__()
        if events is None:
            events = []

        self.user = user
        self.user_id = user.id
        self.name = name
        self.description = description
        self.done = False
        self.events = events
